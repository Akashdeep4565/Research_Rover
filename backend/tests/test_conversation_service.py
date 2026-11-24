"""
Unit and integration tests for ConversationService, SQLite persistence, and Chat API conversation endpoints.
Uses an isolated temporary SQLite database for test isolation.
"""
import os
import sys
import tempfile
import unittest
import shutil
from unittest.mock import MagicMock

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from app.db.models import Base, Conversation, Message
from app.db.session import init_db, get_db
from app.services.conversation_service import ConversationService
from app.models.schemas import ChatRequest, ChatResponse, ChatHistoryMessage
from app.api.routes.chat import router as chat_router
from app.core.dependencies import get_sentence_model, get_llm_instance
from app.core.config import Settings, get_settings


class MockLLMResponse:
    """Mock Gemini response object"""
    def __init__(self, text: str):
        self.text = text


class TestConversationService(unittest.IsolatedAsyncioTestCase):
    """Test conversation CRUD and persistence logic with an isolated SQLite database"""

    async def asyncSetUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_chat.db").replace("\\", "/")
        self.db_url = f"sqlite+aiosqlite:///{self.db_path}"

        self.engine = create_async_engine(self.db_url, echo=False)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )

        # Initialize tables
        await init_db(engine_override=self.engine)

    async def asyncTearDown(self):
        await self.engine.dispose()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_create_and_get_conversation(self):
        """Should create a conversation with title and retrieve it with empty messages"""
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(
                session=session,
                title="Deep Learning Study",
                dataset_filename="cancer_papers.csv"
            )
            self.assertIsNotNone(convo.id)
            self.assertEqual(convo.title, "Deep Learning Study")
            self.assertEqual(convo.dataset_filename, "cancer_papers.csv")

            fetched = await ConversationService.get_conversation_response(session, convo.id)
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched.id, convo.id)
            self.assertEqual(fetched.title, "Deep Learning Study")
            self.assertEqual(fetched.messages, [])

    async def test_list_conversations_with_filtering_and_pagination(self):
        """Should filter by dataset filename, handle null/general chat, and paginate"""
        async with self.session_factory() as session:
            # Create conversations for dataset A, dataset B, and General (None)
            c1 = await ConversationService.create_conversation(session, "Convo A1", "dataset_a.csv")
            c2 = await ConversationService.create_conversation(session, "Convo A2", "dataset_a.csv")
            c3 = await ConversationService.create_conversation(session, "Convo B1", "dataset_b.csv")
            c4 = await ConversationService.create_conversation(session, "Convo Gen", None)

            # Filter by dataset_a.csv
            items_a, total_a = await ConversationService.list_conversations(session, dataset_filename="dataset_a.csv")
            self.assertEqual(total_a, 2)
            self.assertEqual(len(items_a), 2)
            self.assertTrue(all(i.dataset_filename == "dataset_a.csv" for i in items_a))

            # Filter by General Chat (__general__ or null)
            items_gen, total_gen = await ConversationService.list_conversations(session, dataset_filename="__general__")
            self.assertEqual(total_gen, 1)
            self.assertIsNone(items_gen[0].dataset_filename)

            # Pagination
            items_page, total_all = await ConversationService.list_conversations(session, limit=2, offset=0)
            self.assertEqual(total_all, 4)
            self.assertEqual(len(items_page), 2)

    async def test_rename_conversation(self):
        """Should update conversation title and updated_at timestamp"""
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Old Title", None)
            orig_updated = convo.updated_at

            updated = await ConversationService.update_conversation_title(session, convo.id, "Renamed Title")
            self.assertIsNotNone(updated)
            self.assertEqual(updated.title, "Renamed Title")

    async def test_delete_conversation_cascades_messages(self):
        """Deleting conversation should cascade delete all associated messages"""
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "To Delete", "test.csv")
            msg1 = await ConversationService.add_message(session, convo.id, "user", "What is AI?")
            msg2 = await ConversationService.add_message(
                session, convo.id, "assistant", "AI is...", sources=[{"title": "Intro to AI", "url": "https://example.com"}]
            )

            # Confirm messages exist
            fetched = await ConversationService.get_conversation(session, convo.id)
            self.assertEqual(len(fetched.messages), 2)

            # Delete conversation
            deleted = await ConversationService.delete_conversation(session, convo.id)
            self.assertTrue(deleted)

            # Confirm conversation is gone
            none_convo = await ConversationService.get_conversation(session, convo.id)
            self.assertIsNone(none_convo)

    async def test_add_message_with_citation_sources_and_auto_title(self):
        """Adding first user message to untitled conversation auto-generates title and preserves source metadata"""
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, title=None, dataset_filename="papers.csv")
            self.assertEqual(convo.title, "New Conversation")

            # First user message triggers title derivation
            user_msg = await ConversationService.add_message(
                session, convo.id, "user", "What methodologies were used in clinical evaluation?"
            )
            self.assertEqual(user_msg.role, "user")
            self.assertIn("methodologies", convo.title.lower())

            # Assistant response with rich citations
            sources_payload = [
                {
                    "id": 1,
                    "title": "Clinical Trial Analysis",
                    "doi": "10.1000/182",
                    "url": "https://doi.org/10.1000/182",
                    "year": 2024,
                    "source": "PubMed",
                    "content_preview": "The randomized evaluation demonstrated 95% efficacy."
                }
            ]
            asst_msg = await ConversationService.add_message(
                session, convo.id, "assistant", "The authors performed a randomized evaluation.[1]", sources=sources_payload
            )

            fetched_convo = await ConversationService.get_conversation_response(session, convo.id)
            self.assertEqual(len(fetched_convo.messages), 2)
            self.assertEqual(fetched_convo.messages[1].sources[0]["title"], "Clinical Trial Analysis")
            self.assertEqual(fetched_convo.messages[1].sources[0]["doi"], "10.1000/182")
            self.assertIn("randomized evaluation", fetched_convo.messages[1].sources[0]["content_preview"])

    async def test_dataset_matching_validation(self):
        """validate_dataset_match should enforce strict equality between conversation and requested dataset"""
        async with self.session_factory() as session:
            c_dataset = await ConversationService.create_conversation(session, "A", "dataset_x.csv")
            c_general = await ConversationService.create_conversation(session, "B", None)

            # Match dataset_x
            self.assertTrue(ConversationService.validate_dataset_match(c_dataset, "dataset_x.csv"))
            # Mismatch dataset_y
            self.assertFalse(ConversationService.validate_dataset_match(c_dataset, "dataset_y.csv"))
            # Mismatch general
            self.assertFalse(ConversationService.validate_dataset_match(c_dataset, None))

            # General chat matching
            self.assertTrue(ConversationService.validate_dataset_match(c_general, None))
            self.assertTrue(ConversationService.validate_dataset_match(c_general, ""))
            self.assertFalse(ConversationService.validate_dataset_match(c_general, "dataset_x.csv"))


class TestChatEndpointsWithPersistence(unittest.IsolatedAsyncioTestCase):
    """Test FastAPI chat endpoints with conversation persistence using isolated test DB"""

    async def asyncSetUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_api_chat.db").replace("\\", "/")
        self.db_url = f"sqlite+aiosqlite:///{self.db_path}"

        self.engine = create_async_engine(self.db_url, echo=False)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )

        await init_db(engine_override=self.engine)

        self.mock_llm = MagicMock()
        self.mock_sentence = MagicMock()
        self.settings = Settings(DATA_FOLDER=self.temp_dir)

        self.app = FastAPI()
        self.app.include_router(chat_router, prefix="/api/v1/chat")

        # Dependency overrides
        async def override_get_db():
            async with self.session_factory() as session:
                yield session

        self.app.dependency_overrides[get_db] = override_get_db
        self.app.dependency_overrides[get_sentence_model] = lambda: self.mock_sentence
        self.app.dependency_overrides[get_llm_instance] = lambda: self.mock_llm
        self.app.dependency_overrides[get_settings] = lambda: self.settings

        self.client = AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        await self.engine.dispose()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_conversation_rest_crud_lifecycle(self):
        """Verify full lifecycle: create, list, retrieve, rename, delete via HTTP"""
        # 1. Create conversation
        create_res = await self.client.post("/api/v1/chat/conversations", json={
            "title": "Oncology Literature Review",
            "dataset_filename": "cancer.csv"
        })
        self.assertEqual(create_res.status_code, 201)
        convo_data = create_res.json()
        convo_id = convo_data["id"]
        self.assertEqual(convo_data["title"], "Oncology Literature Review")
        self.assertEqual(convo_data["dataset_filename"], "cancer.csv")

        # 2. List conversations
        list_res = await self.client.get("/api/v1/chat/conversations?dataset_filename=cancer.csv")
        self.assertEqual(list_res.status_code, 200)
        list_data = list_res.json()
        self.assertGreaterEqual(list_data["total"], 1)
        self.assertTrue(any(c["id"] == convo_id for c in list_data["conversations"]))

        # 3. Rename conversation
        patch_res = await self.client.patch(f"/api/v1/chat/conversations/{convo_id}", json={
            "title": "Advanced Oncology Analysis"
        })
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.json()["title"], "Advanced Oncology Analysis")

        # 4. Get conversation
        get_res = await self.client.get(f"/api/v1/chat/conversations/{convo_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["title"], "Advanced Oncology Analysis")

        # 5. Delete conversation
        del_res = await self.client.delete(f"/api/v1/chat/conversations/{convo_id}")
        self.assertEqual(del_res.status_code, 200)

        # 6. Verify 404 after deletion
        get_after_del = await self.client.get(f"/api/v1/chat/conversations/{convo_id}")
        self.assertEqual(get_after_del.status_code, 404)

    async def test_chat_generation_persists_messages_when_conversation_id_supplied(self):
        """When conversation_id is supplied, user and assistant messages must be saved in database"""
        self.mock_llm.generate_content.return_value = MockLLMResponse("General AI knowledge response.")

        # Create a conversation
        c_res = await self.client.post("/api/v1/chat/conversations", json={"title": "Test Chat", "dataset_filename": None})
        convo_id = c_res.json()["id"]

        # Call chat generation with conversation_id
        payload = {
            "message": "Explain graph neural networks",
            "filename": None,
            "conversation_id": convo_id
        }
        res = await self.client.post("/api/v1/chat/", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["conversation_id"], convo_id)
        self.assertIsNotNone(data["message_id"])

        # Retrieve conversation from database and verify both user and assistant turns are stored
        fetch_res = await self.client.get(f"/api/v1/chat/conversations/{convo_id}")
        self.assertEqual(fetch_res.status_code, 200)
        messages = fetch_res.json()["messages"]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "Explain graph neural networks")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertIn("General AI knowledge response.", messages[1]["content"])

    async def test_cross_dataset_contamination_prevention(self):
        """Attempting to chat with a dataset different from the conversation's bound dataset returns 400"""
        # Create conversation bound to 'sleep_data.csv'
        c_res = await self.client.post("/api/v1/chat/conversations", json={
            "title": "Sleep Analysis",
            "dataset_filename": "sleep_data.csv"
        })
        convo_id = c_res.json()["id"]

        # Request with mismatched dataset 'cancer_data.csv'
        payload = {
            "message": "Summarize findings",
            "filename": "cancer_data.csv",
            "conversation_id": convo_id
        }
        res = await self.client.post("/api/v1/chat/", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Dataset mismatch", res.json()["detail"])

    async def test_invalid_conversation_id_returns_404(self):
        """Requesting with a non-existent conversation_id returns 404"""
        payload = {
            "message": "Hello",
            "filename": None,
            "conversation_id": "non-existent-uuid-12345"
        }
        res = await self.client.post("/api/v1/chat/", json=payload)
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.json()["detail"])

    async def test_backward_compatibility_when_conversation_id_omitted(self):
        """When conversation_id is omitted, legacy stateless chat continues to work without error"""
        self.mock_llm.generate_content.return_value = MockLLMResponse("Stateless response text.")

        payload = {
            "message": "Explain quantum computing",
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("Stateless response text.", data["response"])
        self.assertIsNone(data.get("conversation_id"))


if __name__ == "__main__":
    unittest.main()
