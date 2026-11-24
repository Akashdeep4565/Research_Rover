"""
Focused tests for Gemini Quota Handling, Fast-Fail, and Retry Idempotency.
Uses isolated SQLite database and fully mocked Gemini LLM calls.
Never makes real network calls or calls real LLM APIs.
"""
import os
import sys
import json
import tempfile
import unittest
import shutil
import asyncio
from typing import List, Optional
from unittest.mock import MagicMock, AsyncMock, patch

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from app.db.models import Base, Conversation, Message
from app.db.session import init_db, get_db, get_session_factory
from app.services.conversation_service import ConversationService
from app.services.chat_service import (
    ChatService,
    GeminiDailyQuotaExhaustedError,
    is_daily_quota_error,
)
from app.models.schemas import ChatRequest, ChatResponse, ChatHistoryMessage
from app.api.routes.chat import router as chat_router
from app.core.dependencies import get_sentence_model, get_llm_instance
from app.core.config import Settings, get_settings


class MockStreamChunk:
    def __init__(self, text: str):
        self.text = text


class MockAsyncStreamIterator:
    """Async iterator simulating chunked Gemini token delivery"""
    def __init__(self, chunks: List[str], fail_after: Optional[int] = None, fail_with: Optional[Exception] = None):
        self.chunks = chunks
        self.fail_after = fail_after
        self.fail_with = fail_with or RuntimeError("Simulated Gemini error")
        self.index = 0
        self.closed = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.fail_after is not None and self.index == self.fail_after:
            raise self.fail_with
        if self.index < len(self.chunks):
            chunk_val = self.chunks[self.index]
            self.index += 1
            return MockStreamChunk(chunk_val)
        raise StopAsyncIteration

    async def aclose(self):
        self.closed = True


def parse_sse_events(raw_body: str) -> List[dict]:
    """Parse raw SSE text into a structured list of event objects"""
    events = []
    blocks = raw_body.strip().split("\n\n")
    for block in blocks:
        if not block.strip():
            continue
        event_name = None
        data = None
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith("event:"):
                event_name = line[len("event:"):].strip()
            elif line.startswith("data:"):
                data_str = line[len("data:"):].strip()
                try:
                    data = json.loads(data_str)
                except Exception:
                    data = data_str
        if event_name:
            events.append({"event": event_name, "data": data})
    return events


class TestQuotaAndRetries(unittest.IsolatedAsyncioTestCase):
    """Targeted tests for Gemini Quota Fast-Fail, Query Fallback, and Retry Idempotency"""

    async def asyncSetUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_quota.db").replace("\\", "/")
        self.db_url = f"sqlite+aiosqlite:///{self.db_path}"

        self.engine = create_async_engine(self.db_url, echo=False)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

        await init_db(engine_override=self.engine)

        self.mock_llm = MagicMock()
        self.mock_sentence = MagicMock()
        self.settings = Settings(
            DATA_FOLDER=self.temp_dir,
            DATABASE_NAME="test_quota.db",
        )

        self.app = FastAPI()
        self.app.include_router(chat_router, prefix="/api/v1/chat")

        async def override_get_db():
            async with self.session_factory() as session:
                yield session

        self.app.dependency_overrides[get_db] = override_get_db
        self.app.dependency_overrides[get_sentence_model] = lambda: self.mock_sentence
        self.app.dependency_overrides[get_llm_instance] = lambda: self.mock_llm
        self.app.dependency_overrides[get_settings] = lambda: self.settings

    async def asyncTearDown(self):
        await self.engine.dispose()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # ─────────────────────────────────────────────────────────────────────────
    # FIX 1 TESTS: Daily Quota Fast-Fail
    # ─────────────────────────────────────────────────────────────────────────

    async def test_01_daily_quota_error_fails_immediately(self):
        """Daily quota error (GenerateRequestsPerDayPerModel-FreeTier) fails immediately without retry"""
        daily_err = RuntimeError(
            "429 Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, "
            "limit: 20, model: gemini-3.6-flash, description: Generate content requests per day limit exceeded on Free Tier. "
            "quota_id: GenerateRequestsPerDayPerModel-FreeTier"
        )
        self.mock_llm.generate_content.side_effect = daily_err
        self.mock_llm.generate_content_async = AsyncMock(side_effect=daily_err)

        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        # Test _call_gemini_with_retry raises GeminiDailyQuotaExhaustedError immediately
        with self.assertRaises(GeminiDailyQuotaExhaustedError):
            await chat_service._call_gemini_with_retry("test prompt", max_retries=2)

        # generate_content should have been called exactly once (no retries)
        self.assertEqual(self.mock_llm.generate_content.call_count, 1)

        # Test _stream_gemini_with_retry raises GeminiDailyQuotaExhaustedError immediately
        with self.assertRaises(GeminiDailyQuotaExhaustedError):
            async for _ in chat_service._stream_gemini_with_retry("test streaming prompt", max_retries=2):
                pass

        # generate_content_async should have been called exactly once (no retries)
        self.assertEqual(self.mock_llm.generate_content_async.call_count, 1)

    async def test_02_no_retry_sleep_occurs_for_daily_quota_exhaustion(self):
        """No asyncio.sleep occurs when encountering daily quota exhaustion"""
        daily_err = RuntimeError(
            "429 ResourceExhausted: requests per day limit reached for Free Tier"
        )
        self.mock_llm.generate_content.side_effect = daily_err
        self.mock_llm.generate_content_async = AsyncMock(side_effect=daily_err)

        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            with self.assertRaises(GeminiDailyQuotaExhaustedError):
                await chat_service._call_gemini_with_retry("prompt", max_retries=2)
            mock_sleep.assert_not_called()

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            with self.assertRaises(GeminiDailyQuotaExhaustedError):
                async for _ in chat_service._stream_gemini_with_retry("prompt", max_retries=2):
                    pass
            mock_sleep.assert_not_called()

    async def test_03_transient_429_errors_still_use_bounded_retry_policy(self):
        """Transient 429 rate limit (per minute / momentary spike) still retries up to max_retries"""
        transient_err = RuntimeError("429 Too Many Requests: Rate limit exceeded. Please wait 1s.")
        self.mock_llm.generate_content.side_effect = transient_err
        self.mock_llm.generate_content_async = AsyncMock(side_effect=transient_err)

        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            # Non-streaming call retries max_retries=2 times (3 total attempts)
            resp = await chat_service._call_gemini_with_retry("prompt", max_retries=2)
            self.assertEqual(self.mock_llm.generate_content.call_count, 3)
            self.assertEqual(mock_sleep.call_count, 2)
            self.assertIn("rate limit was reached", resp)

        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            # Streaming call retries max_retries=2 times (3 total attempts) before raising
            with self.assertRaises(RuntimeError):
                async for _ in chat_service._stream_gemini_with_retry("prompt", max_retries=2):
                    pass
            self.assertEqual(self.mock_llm.generate_content_async.call_count, 3)
            self.assertEqual(mock_sleep.call_count, 2)

    async def test_04_streaming_daily_quota_exhaustion_emits_correct_sse_error(self):
        """POST /api/v1/chat/stream emits SSE error event with RATE_LIMIT code when daily quota exhausted"""
        daily_err = RuntimeError(
            "429 ResourceExhausted: GenerateRequestsPerDayPerModel-FreeTier limit exceeded"
        )
        self.mock_llm.generate_content_async = AsyncMock(side_effect=daily_err)

        transport = ASGITransport(app=self.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {
                "message": "Explain quantum entanglement",
                "filename": None,
            }
            res = await client.post("/api/v1/chat/stream", json=payload)
            self.assertEqual(res.status_code, 200)

            events = parse_sse_events(res.text)
            error_event = next((e for e in events if e["event"] == "error"), None)
            self.assertIsNotNone(error_event, "Expected an error event in stream")
            self.assertIn("rate limit", error_event["data"]["error"].lower())
            self.assertEqual(error_event["data"]["code"], "RATE_LIMIT")

    # ─────────────────────────────────────────────────────────────────────────
    # FIX 2 TESTS: Query Decomposition Fallback
    # ─────────────────────────────────────────────────────────────────────────

    async def test_05_query_decomposition_failure_falls_back_to_original_query(self):
        """When Gemini query decomposition fails or returns error string, falls back to [query]"""
        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        # Case A: Gemini raises exception (e.g. daily quota error)
        self.mock_llm.generate_content.side_effect = GeminiDailyQuotaExhaustedError("Daily quota exhausted")
        queries = await chat_service._decompose_query("What are the side effects of immunotherapy?")
        self.assertEqual(queries, ["What are the side effects of immunotherapy?"])

        # Case B: Gemini returns rate-limit / error apology string
        mock_resp = MagicMock()
        mock_resp.text = "The Gemini AI rate limit was reached. Please wait a few seconds before trying again."
        self.mock_llm.generate_content.side_effect = None
        self.mock_llm.generate_content.return_value = mock_resp

        queries2 = await chat_service._decompose_query("How does CAR-T therapy work?")
        self.assertEqual(queries2, ["How does CAR-T therapy work?"])
        # Ensure the error text was NOT treated as a sub-query
        self.assertNotIn("rate limit", queries2[0].lower())

    async def test_06_faiss_retrieval_still_executes_after_decomposition_failure(self):
        """FAISS retrieval executes with fallback query even when decomposition fails"""
        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        # Create temporary FAISS index and metadata
        import faiss
        import numpy as np

        dim = 128
        index = faiss.IndexFlatL2(dim)
        vecs = np.random.rand(3, dim).astype("float32")
        index.add(vecs)
        index_file = os.path.join(self.temp_dir, "test_paper_paper_chunks_hdbscan.index")
        faiss.write_index(index, index_file)

        meta_file = os.path.join(self.temp_dir, "test_paper_paper_chunk_metadata_hdbscan.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump([
                {"text": "Immunotherapy is a breakthrough cancer treatment.", "doi": "10.1234/immuno1", "chunk_id": "c1"},
                {"text": "Checkpoint inhibitors enhance T-cell activity.", "doi": "10.1234/immuno2", "chunk_id": "c2"},
                {"text": "CAR-T cells are engineered for targeted lysis.", "doi": "10.1234/immuno3", "chunk_id": "c3"},
            ], f)

        # Sentence model mock returns a 128-dim embedding
        self.mock_sentence.encode.return_value = np.random.rand(1, dim).astype("float32")

        # LLM fails decomposition with rate limit
        self.mock_llm.generate_content.side_effect = RuntimeError("429 rate limit exceeded")
        # LLM streaming also mocked to yield a response
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Grounded ", "answer."])
        )

        events = []
        async for event in chat_service.generate_response_stream(
            filename="test_paper.csv",
            query="What are the mechanisms of immunotherapy?"
        ):
            events.append(event)

        # Citations event should be present and populated from FAISS search
        citations_event = next((e for e in events if e["event"] == "citations"), None)
        self.assertIsNotNone(citations_event, "Expected citations event even when decomposition fails")
        self.assertGreater(len(citations_event["data"]["sources"]), 0)

        # Status event should show generating
        status_events = [e for e in events if e["event"] == "status"]
        self.assertTrue(any(s["data"]["stage"] == "generating" for s in status_events))

    async def test_09_successful_query_decomposition_remains_unchanged(self):
        """When Gemini returns clean sub-queries, successful decomposition splits lines properly"""
        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        mock_resp = MagicMock()
        mock_resp.text = "What is the efficacy of immunotherapy in ovarian cancer?\nBiomarkers predicting response to checkpoint inhibitors"
        self.mock_llm.generate_content.side_effect = None
        self.mock_llm.generate_content.return_value = mock_resp

        queries = await chat_service._decompose_query("Tell me about ovarian cancer immunotherapy response and biomarkers")
        self.assertEqual(len(queries), 2)
        self.assertEqual(queries[0], "What is the efficacy of immunotherapy in ovarian cancer?")
        self.assertEqual(queries[1], "Biomarkers predicting response to checkpoint inhibitors")


    # ─────────────────────────────────────────────────────────────────────────
    # FIX 3 TESTS: Retry Idempotency
    # ─────────────────────────────────────────────────────────────────────────

    async def test_07_retry_after_failed_assistant_response_does_not_duplicate_user_message(self):
        """Retrying a question after an assistant failure turn does not duplicate the user turn in DB"""
        # Create persistent conversation
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Retry Test", None)
            convo_id = convo.id

        transport = ASGITransport(app=self.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # First attempt: Gemini fails
            self.mock_llm.generate_content_async = AsyncMock(
                side_effect=RuntimeError("503 Service Unavailable")
            )
            payload = {
                "message": "What is transformer attention?",
                "conversation_id": convo_id,
                "filename": None,
            }
            res1 = await client.post("/api/v1/chat/stream", json=payload)
            self.assertEqual(res1.status_code, 200)

            # Check messages in DB: 1 user turn, 1 error assistant turn
            async with self.session_factory() as session:
                convo1 = await ConversationService.get_conversation(session, convo_id)
                self.assertEqual(len(convo1.messages), 2)
                self.assertEqual(convo1.messages[0].role, "user")
                self.assertEqual(convo1.messages[0].content, "What is transformer attention?")
                self.assertEqual(convo1.messages[1].role, "assistant")
                self.assertTrue(convo1.messages[1].is_error)

            # Second attempt (Retry): Gemini succeeds
            self.mock_llm.generate_content_async = AsyncMock(
                return_value=MockAsyncStreamIterator(["Self-attention ", "calculates query-key weights."])
            )
            res2 = await client.post("/api/v1/chat/stream", json=payload)
            self.assertEqual(res2.status_code, 200)

            # Check messages in DB: still exactly 1 user turn! Followed by assistant turns
            async with self.session_factory() as session:
                convo2 = await ConversationService.get_conversation(session, convo_id)
                user_msgs = [m for m in convo2.messages if m.role == "user"]
                self.assertEqual(len(user_msgs), 1, "Expected exactly 1 user message, no duplicates on retry")
                self.assertEqual(user_msgs[0].content, "What is transformer attention?")
                # Total messages: 1 user, 1 failed assistant, 1 succeeded assistant
                self.assertEqual(len(convo2.messages), 3)
                self.assertFalse(convo2.messages[2].is_error)

    async def test_08_multiple_consecutive_failed_retries_remain_idempotent(self):
        """Even after 4 consecutive failed retries, only 1 user turn exists in the database"""
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Multi-Retry Test", None)
            convo_id = convo.id

        transport = ASGITransport(app=self.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {
                "message": "Explain diffusion probabilistic models",
                "conversation_id": convo_id,
                "filename": None,
            }

            # 4 consecutive failed retries (e.g. rate limit / daily quota hits)
            self.mock_llm.generate_content_async = AsyncMock(
                side_effect=RuntimeError("429 rate limit exceeded")
            )
            with patch("asyncio.sleep", new_callable=AsyncMock):
                for attempt in range(4):
                    res = await client.post("/api/v1/chat/stream", json=payload)
                    self.assertEqual(res.status_code, 200)

            # Check database: exactly 1 user message, 4 assistant error messages
            async with self.session_factory() as session:
                convo = await ConversationService.get_conversation(session, convo_id)
                user_msgs = [m for m in convo.messages if m.role == "user"]
                asst_msgs = [m for m in convo.messages if m.role == "assistant"]
                self.assertEqual(len(user_msgs), 1, "Only 1 user message should exist across 4 failed retries")
                self.assertEqual(len(asst_msgs), 4, "Expected 4 recorded assistant error turns")

            # Now submit a DIFFERENT question: should record a NEW user turn
            new_payload = {
                "message": "Explain reinforcement learning from human feedback",
                "conversation_id": convo_id,
                "filename": None,
            }
            self.mock_llm.generate_content_async = AsyncMock(
                return_value=MockAsyncStreamIterator(["RLHF ", "aligns LLMs."])
            )
            res_new = await client.post("/api/v1/chat/stream", json=new_payload)
            self.assertEqual(res_new.status_code, 200)

            async with self.session_factory() as session:
                convo_after = await ConversationService.get_conversation(session, convo_id)
                user_msgs_after = [m for m in convo_after.messages if m.role == "user"]
                self.assertEqual(len(user_msgs_after), 2, "Expected 2 distinct user questions")
                self.assertEqual(user_msgs_after[0].content, "Explain diffusion probabilistic models")
                self.assertEqual(user_msgs_after[1].content, "Explain reinforcement learning from human feedback")

    async def test_10_existing_non_streaming_and_streaming_chat_remain_compatible(self):
        """Both non-streaming POST /api/v1/chat and streaming POST /api/v1/chat/stream remain compatible"""
        mock_resp = MagicMock()
        mock_resp.text = "Non-streaming answer about neural networks."
        self.mock_llm.generate_content.return_value = mock_resp
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Streaming ", "answer."])
        )

        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Compat Test", None)
            convo_id = convo.id

        transport = ASGITransport(app=self.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 1. Non-streaming call
            non_stream_res = await client.post("/api/v1/chat", json={
                "message": "What is a neural network?",
                "conversation_id": convo_id,
                "filename": None,
            })
            self.assertEqual(non_stream_res.status_code, 200)
            data = non_stream_res.json()
            self.assertIn("Non-streaming answer", data["response"])
            self.assertEqual(data["conversation_id"], convo_id)

            # 2. Streaming call in the same conversation
            stream_res = await client.post("/api/v1/chat/stream", json={
                "message": "How is backpropagation performed?",
                "conversation_id": convo_id,
                "filename": None,
            })
            self.assertEqual(stream_res.status_code, 200)
            events = parse_sse_events(stream_res.text)
            deltas = [e["data"]["text"] for e in events if e["event"] == "delta"]
            self.assertIn("Streaming answer.", "".join(deltas))
            done = next((e for e in events if e["event"] == "done"), None)
            self.assertIsNotNone(done)

            # 3. Check persistent history in DB: 2 user messages, 2 assistant messages
            async with self.session_factory() as session:
                final_convo = await ConversationService.get_conversation(session, convo_id)
                self.assertEqual(len(final_convo.messages), 4)
                self.assertEqual(final_convo.messages[0].content, "What is a neural network?")
                self.assertEqual(final_convo.messages[2].content, "How is backpropagation performed?")


if __name__ == "__main__":
    unittest.main()
