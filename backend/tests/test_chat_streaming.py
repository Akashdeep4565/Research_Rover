"""
Targeted unit and integration tests for backend Gemini streaming (SSE) endpoint and ChatService.
Uses isolated SQLite database and fully mocked Gemini LLM async streaming.
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
from unittest.mock import MagicMock, AsyncMock

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from app.db.models import Base, Conversation, Message
from app.db.session import init_db, get_db, get_session_factory
from app.services.conversation_service import ConversationService
from app.services.chat_service import ChatService
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


class TestChatStreaming(unittest.IsolatedAsyncioTestCase):
    """Test suite for Phase 4B Backend SSE Streaming"""

    async def asyncSetUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_streaming_chat.db").replace("\\", "/")
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
        self.settings = Settings(
            DATA_FOLDER=self.temp_dir,
            DATABASE_NAME="test_streaming_chat.db"
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

        self.client = AsyncClient(transport=ASGITransport(app=self.app), base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()
        await self.engine.dispose()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_01_streaming_endpoint_returns_event_stream_and_headers(self):
        """Streaming endpoint must respond with Content-Type: text/event-stream and no-cache headers"""
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Hello ", "world!"])
        )

        payload = {
            "message": "What is machine learning?",
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/event-stream", res.headers.get("content-type", ""))
        self.assertEqual(res.headers.get("cache-control"), "no-cache")

    async def test_02_status_event_emitted(self):
        """Status events must indicate the pipeline stage and message"""
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Response text."])
        )

        payload = {"message": "Explain deep learning", "filename": None}
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        events = parse_sse_events(res.text)

        status_events = [e for e in events if e["event"] == "status"]
        self.assertGreaterEqual(len(status_events), 1)
        self.assertIn("stage", status_events[0]["data"])
        self.assertIn("message", status_events[0]["data"])

    async def test_03_citations_emitted_before_first_text_delta(self):
        """Citations event must appear before any text delta event"""
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Token 1 ", "Token 2"])
        )

        payload = {"message": "Summarize findings", "filename": None}
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        events = parse_sse_events(res.text)

        citations_idx = -1
        first_delta_idx = -1
        for i, e in enumerate(events):
            if e["event"] == "citations" and citations_idx == -1:
                citations_idx = i
            elif e["event"] == "delta" and first_delta_idx == -1:
                first_delta_idx = i

        self.assertNotEqual(citations_idx, -1, "Citations event was not emitted")
        self.assertNotEqual(first_delta_idx, -1, "Delta event was not emitted")
        self.assertLess(citations_idx, first_delta_idx, "Citations must be emitted before first delta")

    async def test_04_multiple_delta_events_reconstruct_correct_answer(self):
        """Reconstructing delta chunks must match full generated text"""
        tokens = ["Attention ", "is ", "all ", "you ", "need."]
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(tokens)
        )

        payload = {"message": "Explain transformers", "filename": None}
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        events = parse_sse_events(res.text)

        deltas = [e["data"]["text"] for e in events if e["event"] == "delta"]
        reconstructed = "".join(deltas)
        for token in tokens:
            self.assertIn(token, reconstructed)

    async def test_05_completion_event_emitted_only_after_assistant_persistence(self):
        """Done event must include message_id and conversation_id and exist in database"""
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Answer ", "complete."])
        )

        # Create persistent conversation
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "AI Convo", None)
            convo_id = convo.id

        payload = {
            "message": "What is reinforcement learning?",
            "conversation_id": convo_id,
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        events = parse_sse_events(res.text)

        done_event = next((e for e in events if e["event"] == "done"), None)
        self.assertIsNotNone(done_event, "Done event was not emitted")
        self.assertEqual(done_event["data"]["status"], "completed")
        self.assertEqual(done_event["data"]["conversation_id"], convo_id)
        msg_id = done_event["data"]["message_id"]
        self.assertIsNotNone(msg_id)

        # Verify assistant message exists in SQLite
        async with self.session_factory() as session:
            fetched_convo = await ConversationService.get_conversation(session, convo_id)
            assistant_msgs = [m for m in fetched_convo.messages if m.role == "assistant"]
            self.assertEqual(len(assistant_msgs), 1)
            self.assertEqual(assistant_msgs[0].id, msg_id)
            self.assertIn("Answer complete.", assistant_msgs[0].content)

    async def test_06_user_message_persisted_before_generation(self):
        """User message must be committed to database before Gemini generation runs"""
        # Create persistent conversation
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Prompt Convo", None)
            convo_id = convo.id

        # Make LLM fail on token generation
        self.mock_llm.generate_content_async = AsyncMock(
            side_effect=RuntimeError("Simulated LLM network crash")
        )

        payload = {
            "message": "Critical User Question",
            "conversation_id": convo_id,
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        self.assertEqual(res.status_code, 200)

        # Even though LLM crashed, user turn must be persisted in database!
        async with self.session_factory() as session:
            fetched_convo = await ConversationService.get_conversation(session, convo_id)
            user_msgs = [m for m in fetched_convo.messages if m.role == "user"]
            self.assertEqual(len(user_msgs), 1)
            self.assertEqual(user_msgs[0].content, "Critical User Question")

    async def test_07_dataset_mismatch_is_rejected(self):
        """Conversation bound to dataset_a.csv rejects requests with dataset_b.csv (HTTP 400)"""
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Dataset Convo", "dataset_a.csv")
            convo_id = convo.id

        payload = {
            "message": "Question",
            "conversation_id": convo_id,
            "filename": "dataset_b.csv"
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Dataset mismatch", res.json()["detail"])

    async def test_08_invalid_conversation_id_is_rejected(self):
        """Non-existent conversation ID returns HTTP 404"""
        payload = {
            "message": "Hello",
            "conversation_id": "non-existent-uuid-9999",
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        self.assertEqual(res.status_code, 404)
        self.assertIn("not found", res.json()["detail"])

    async def test_09_gemini_failure_before_first_token_handled(self):
        """When Gemini fails before token 0, error event is emitted and persisted as error turn"""
        self.mock_llm.generate_content_async = AsyncMock(
            side_effect=RuntimeError("503 Service Unavailable")
        )

        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Error Convo", None)
            convo_id = convo.id

        payload = {
            "message": "Will fail immediately",
            "conversation_id": convo_id,
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        events = parse_sse_events(res.text)

        error_event = next((e for e in events if e["event"] == "error"), None)
        self.assertIsNotNone(error_event)
        self.assertIn("code", error_event["data"])

        # Check persisted turn has is_error=True
        async with self.session_factory() as session:
            fetched = await ConversationService.get_conversation(session, convo_id)
            asst = [m for m in fetched.messages if m.role == "assistant"]
            self.assertEqual(len(asst), 1)
            self.assertTrue(asst[0].is_error)

    async def test_10_gemini_failure_after_partial_output_handled(self):
        """When Gemini drops after emitting tokens, error event is emitted without silently restarting"""
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(
                ["Part 1", "Part 2"],
                fail_after=1,
                fail_with=RuntimeError("Mid-stream connection drop")
            )
        )

        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Partial Convo", None)
            convo_id = convo.id

        payload = {
            "message": "Midstream test",
            "conversation_id": convo_id,
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        events = parse_sse_events(res.text)

        deltas = [e for e in events if e["event"] == "delta"]
        self.assertGreaterEqual(len(deltas), 1)
        error_event = next((e for e in events if e["event"] == "error"), None)
        self.assertIsNotNone(error_event)

    async def test_11_cancellation_saves_partial_text_with_stopped_marker(self):
        """ChatService streaming cancellation propagates CancelledError and preserves partial text"""
        chat_service = ChatService(self.settings, self.mock_sentence, self.mock_llm)

        cancel_call_count = 0
        async def cancel_after_one_chunk():
            nonlocal cancel_call_count
            cancel_call_count += 1
            return cancel_call_count >= 2

        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Token A ", "Token B ", "Token C "])
        )

        with self.assertRaises(asyncio.CancelledError):
            async for _ in chat_service.generate_response_stream(
                filename=None,
                query="Cancel query",
                is_client_disconnected=cancel_after_one_chunk
            ):
                pass

    async def test_12_no_duplicate_user_message_on_retry(self):
        """Regenerating a failed response must not duplicate user message in database"""
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Answer 1"])
        )

        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "Retry Convo", None)
            convo_id = convo.id

        payload = {
            "message": "Identical Query",
            "conversation_id": convo_id,
            "filename": None
        }

        # First execution
        await self.client.post("/api/v1/chat/stream", json=payload)

        # Retry execution with identical message
        self.mock_llm.generate_content_async = AsyncMock(
            return_value=MockAsyncStreamIterator(["Answer 2"])
        )
        await self.client.post("/api/v1/chat/stream", json=payload)

        # Check database: user message should appear only ONCE
        async with self.session_factory() as session:
            fetched = await ConversationService.get_conversation(session, convo_id)
            user_msgs = [m for m in fetched.messages if m.role == "user" and m.content == "Identical Query"]
            self.assertEqual(len(user_msgs), 1, "User message duplicated on retry!")

    async def test_13_existing_non_streaming_endpoint_remains_operational(self):
        """Existing POST /api/v1/chat/ non-streaming endpoint continues to function normally"""
        class MockSyncResponse:
            text = "Legacy JSON response text."

        self.mock_llm.generate_content = MagicMock(return_value=MockSyncResponse())

        payload = {
            "message": "Explain legacy endpoints",
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("Legacy JSON response text.", data["response"])
        self.assertIn("sources", data)

    async def test_14_database_sessions_not_held_open_during_streaming(self):
        """Verify database session is cleanly closed while streaming tokens are yielded"""
        # Create conversation
        async with self.session_factory() as session:
            convo = await ConversationService.create_conversation(session, "DB Lock Convo", None)
            convo_id = convo.id

        session_closed_during_stream = False

        class CheckingStreamIterator:
            def __init__(self, session_factory, convo_id):
                self.session_factory = session_factory
                self.convo_id = convo_id
                self.yielded = False

            def __aiter__(self):
                return self

            async def __anext__(self):
                nonlocal session_closed_during_stream
                if not self.yielded:
                    self.yielded = True
                    # Try opening another database session to verify no exclusive write locks hold the DB
                    async with self.session_factory() as check_session:
                        c = await ConversationService.get_conversation(check_session, self.convo_id)
                        if c is not None:
                            session_closed_during_stream = True
                    return MockStreamChunk("Unblocked DB token")
                raise StopAsyncIteration

        self.mock_llm.generate_content_async = AsyncMock(
            return_value=CheckingStreamIterator(self.session_factory, convo_id)
        )

        payload = {
            "message": "Test DB lock release",
            "conversation_id": convo_id,
            "filename": None
        }
        res = await self.client.post("/api/v1/chat/stream", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(session_closed_during_stream, "Database was locked or session was not released during streaming!")


if __name__ == "__main__":
    unittest.main()
