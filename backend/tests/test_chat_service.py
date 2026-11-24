"""
Unit tests for ChatService and AI Chat endpoints in Research Rover.
Uses mocked LLM and sentence model to test conversation history,
retrieval citation previews, and fallback responses without downloading heavy weights.
"""

import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import os
import sys
import tempfile
import json
import shutil
import numpy as np
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import faiss
from app.services.chat_service import ChatService
from app.models.schemas import ChatRequest, ChatResponse, ChatHistoryMessage
from app.core.config import Settings, get_settings
from app.core.dependencies import get_sentence_model, get_llm_instance
from app.db.session import get_db
from app.api.routes.chat import router as chat_router


class MockLLMResponse:
    """Mock Gemini response object"""
    def __init__(self, text: str):
        self.text = text


class TestChatService(unittest.IsolatedAsyncioTestCase):
    """Test ChatService business logic and RAG prompt assembly."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.settings = Settings(DATA_FOLDER=self.temp_dir)
        self.mock_sentence_model = MagicMock()
        self.mock_llm = MagicMock()
        self.chat_service = ChatService(self.settings, self.mock_sentence_model, self.mock_llm)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_chat_without_dataset_fallback(self):
        """When no dataset is selected, ChatService should return a general response with notice."""
        self.mock_llm.generate_content.return_value = MockLLMResponse("General AI knowledge answer.")
        
        response = await self.chat_service.generate_response(
            filename=None,
            query="What is deep learning?",
            history=[ChatHistoryMessage(role="user", content="Hi")]
        )
        
        self.assertIsInstance(response, ChatResponse)
        self.assertIn("[Notice: No dataset selected", response.response)
        self.assertIn("General AI knowledge answer.", response.response)
        self.assertEqual(response.sources, [])
        self.assertEqual(response.query, "What is deep learning?")

    async def test_chat_unindexed_dataset_fallback(self):
        """When dataset CSV exists but embeddings index has not been generated, provide unindexed notice."""
        self.mock_llm.generate_content.return_value = MockLLMResponse("General answer for unindexed corpus.")
        
        response = await self.chat_service.generate_response(
            filename="unindexed_papers.csv",
            query="Summarize methodologies",
            history=[]
        )
        
        self.assertIsInstance(response, ChatResponse)
        self.assertIn("[Notice: Semantic search index has not been generated", response.response)
        self.assertIn("General answer for unindexed corpus.", response.response)
        self.assertEqual(response.sources, [])

    def test_citation_preview_uses_actual_chunk_text(self):
        """Citation previews must contain actual chunk text, NOT paper titles."""
        search_results = [
            {
                "chunk_id": 1,
                "paperTitle": "Transformer Models in Healthcare",
                "title": "Transformer Models in Healthcare",
                "text": "We evaluated vision transformers on 50,000 chest radiographs and observed 94.2% accuracy.",
                "doi": "10.1016/j.jbi.2023.104400",
                "source": "PubMed",
                "yearPublished": 2023,
                "distance": 0.15,
            },
            {
                "chunk_id": 2,
                "paperTitle": "Graph Neural Networks for Drug Repurposing",
                "title": "Graph Neural Networks for Drug Repurposing",
                "text": "Our GNN framework identified 12 candidate inhibitors with sub-micromolar binding affinities.",
                "doi": "10.1038/s41598-024-00123-x",
                "source": "OpenAlex",
                "yearPublished": 2024,
                "distance": 0.22,
            }
        ]
        paper_titles = [r["paperTitle"] for r in search_results]
        download_urls = ["https://doi.org/10.1016/j.jbi.2023.104400", "https://doi.org/10.1038/s41598-024-00123-x"]
        
        sources = self.chat_service._create_sources_from_results(search_results, paper_titles, download_urls)
        
        self.assertEqual(len(sources), 2)
        
        # Verify first source citation details
        s1 = sources[0]
        self.assertEqual(s1["id"], 1)
        self.assertEqual(s1["title"], "Transformer Models in Healthcare")
        self.assertEqual(s1["doi"], "10.1016/j.jbi.2023.104400")
        self.assertEqual(s1["source"], "PubMed")
        self.assertEqual(s1["year"], 2023)
        # Content preview must NOT be the title, it must contain actual chunk text!
        self.assertNotEqual(s1["content_preview"], s1["title"])
        self.assertIn("We evaluated vision transformers on 50,000 chest radiographs", s1["content_preview"])
        
        # Verify second source citation details
        s2 = sources[1]
        self.assertEqual(s2["id"], 2)
        self.assertEqual(s2["title"], "Graph Neural Networks for Drug Repurposing")
        self.assertIn("Our GNN framework identified 12 candidate inhibitors", s2["content_preview"])

    async def test_query_decomposition_with_history(self):
        """Query decomposition should accept history and prompt LLM with contextual awareness."""
        captured_prompts = []
        def capture_prompt(prompt):
            captured_prompts.append(prompt)
            return MockLLMResponse("What dataset was used in Transformer Models in Healthcare?\nEvaluation benchmarks for medical transformers")
        
        self.mock_llm.generate_content.side_effect = capture_prompt
        
        history = [
            ChatHistoryMessage(role="user", content="Which paper discusses transformer models?"),
            ChatHistoryMessage(role="assistant", content="Paper [1] 'Transformer Models in Healthcare' covers this.")
        ]
        
        sub_queries = await self.chat_service._decompose_query("What dataset did they use?", history=history)
        
        self.assertEqual(len(sub_queries), 2)
        self.assertEqual(sub_queries[0], "What dataset was used in Transformer Models in Healthcare?")
        # Verify conversation history was passed inside the decomposition prompt
        self.assertTrue(len(captured_prompts) > 0)
        self.assertIn("Recent Conversation History:", captured_prompts[0])
        self.assertIn("Which paper discusses transformer models?", captured_prompts[0])

    async def test_generate_ai_response_includes_history_in_prompt(self):
        """Response generation prompt must include the recent conversation history."""
        captured_prompts = []
        def capture_prompt(prompt):
            captured_prompts.append(prompt)
            return MockLLMResponse("The authors used the MIMIC-CXR dataset.[1]")
        
        self.mock_llm.generate_content.side_effect = capture_prompt
        
        history = [
            {"role": "user", "content": "Tell me about vision transformers."},
            {"role": "assistant", "content": "They achieve strong results in medical imaging.[1]"}
        ]
        
        context_docs = "[1] [Source Title: Medical ViT]\nWe tested on MIMIC-CXR dataset."
        
        response = await self.chat_service._generate_ai_response_original(
            query="What dataset was used?",
            llm_context_string=context_docs,
            history=history
        )
        
        self.assertEqual(response, "The authors used the MIMIC-CXR dataset.[1]")
        self.assertTrue(len(captured_prompts) > 0)
        self.assertIn("Recent Conversation History:", captured_prompts[0])
        self.assertIn("Tell me about vision transformers.", captured_prompts[0])
        self.assertIn("Question:", captured_prompts[0])

    async def test_corrupt_faiss_index_fallback(self):
        """When FAISS index or metadata file is corrupted/unreadable, ChatService falls back gracefully."""
        # Create invalid/corrupted files in temp_dir
        base_name = "corrupt_dataset"
        faiss_path = os.path.join(self.temp_dir, f"{base_name}_paper_chunks_hdbscan.index")
        meta_path = os.path.join(self.temp_dir, f"{base_name}_paper_chunk_metadata_hdbscan.json")
        
        with open(faiss_path, "wb") as f:
            f.write(b"NOT_A_VALID_FAISS_INDEX_BINARY_DATA")
        with open(meta_path, "w") as f:
            f.write("{invalid_json: true,")  # Malformed JSON
            
        self.mock_llm.generate_content.return_value = MockLLMResponse("General fallback response.")

        response = await self.chat_service.generate_response(
            filename=f"{base_name}.csv",
            query="Explain methodologies",
            history=[]
        )

        self.assertIsInstance(response, ChatResponse)
        self.assertIn("appears corrupted or unreadable", response.response)
        self.assertIn("Recreate embeddings", response.response)
        self.assertIn("General fallback response.", response.response)

    async def test_gemini_retry_on_transient_429(self):
        """When Gemini throws a transient 429 error, ChatService retries and recovers."""
        calls = []
        def side_effect(prompt):
            calls.append(prompt)
            if len(calls) == 1:
                raise Exception("429 ResourceExhausted: Quota exceeded")
            return MockLLMResponse("Successfully generated answer on retry.")

        self.mock_llm.generate_content.side_effect = side_effect

        response_text = await self.chat_service._call_gemini_with_retry("Test prompt", max_retries=2)

        self.assertEqual(len(calls), 2)
        self.assertEqual(response_text, "Successfully generated answer on retry.")

    async def test_gemini_auth_error_fails_fast(self):
        """When an invalid API key is encountered, ChatService fails fast without retrying."""
        calls = []
        def side_effect(prompt):
            calls.append(prompt)
            raise Exception("API_KEY_INVALID: API key not valid. Please pass a valid API key.")

        self.mock_llm.generate_content.side_effect = side_effect

        with self.assertRaises(RuntimeError) as ctx:
            await self.chat_service._call_gemini_with_retry("Test prompt", max_retries=2)

        self.assertEqual(len(calls), 1)  # Only 1 call made, no retries!
        self.assertIn("Gemini API authentication failed", str(ctx.exception))


class TestChatApiEndpoints(unittest.IsolatedAsyncioTestCase):
    """Test FastAPI HTTP chat endpoints with conversation history using isolated router."""

    async def asyncSetUp(self):
        self.mock_llm = MagicMock()
        self.mock_sentence = MagicMock()
        self.mock_session = AsyncMock()

        self.temp_dir = tempfile.mkdtemp()
        self.settings = Settings(DATA_FOLDER=self.temp_dir)

        self.test_app = FastAPI()
        self.test_app.include_router(chat_router, prefix="/api/v1/chat")

        # Dependency overrides
        async def override_get_db():
            yield self.mock_session

        async def override_get_settings():
            return self.settings

        async def override_get_sentence_model():
            return self.mock_sentence

        async def override_get_llm_instance():
            return self.mock_llm

        self.test_app.dependency_overrides[get_db] = override_get_db
        self.test_app.dependency_overrides[get_settings] = override_get_settings
        self.test_app.dependency_overrides[get_sentence_model] = override_get_sentence_model
        self.test_app.dependency_overrides[get_llm_instance] = override_get_llm_instance

        self.client = AsyncClient(
            transport=ASGITransport(app=self.test_app),
            base_url="http://test"
        )

    async def asyncTearDown(self):
        await self.client.aclose()
        if hasattr(self, "test_app"):
            self.test_app.dependency_overrides.clear()
        if hasattr(self, "temp_dir") and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_post_chat_root_with_history(self):
        """POST /api/v1/chat/ should accept history and return ChatResponse."""
        self.mock_llm.generate_content.return_value = MockLLMResponse("General response answering question.")
        
        payload = {
            "message": "Explain that further",
            "filename": None,
            "history": [
                {"role": "user", "content": "What is attention?"},
                {"role": "assistant", "content": "Attention is a mechanism."}
            ]
        }
        response = await self.client.post("/api/v1/chat/", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("sources", data)
        self.assertEqual(data["query"], "Explain that further")
        self.assertIn("General response answering question.", data["response"])

    async def test_post_chat_empty_message_validation(self):
        """POST /api/v1/chat/ should reject empty messages with 422 validation error."""
        response = await self.client.post("/api/v1/chat/", json={"message": ""})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
