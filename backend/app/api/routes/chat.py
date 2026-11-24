"""
Chat API routes for AI-powered paper analysis and persistent conversation management
"""
import json
import asyncio
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
import logging

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationListResponse,
    ChatHistoryMessage,
)
from app.core.config import get_settings
from app.core.dependencies import get_sentence_model, get_llm_instance
from app.db.session import get_db, get_session_factory
from app.services.chat_service import ChatService, GeminiDailyQuotaExhaustedError, is_daily_quota_error
from app.services.conversation_service import ConversationService

router = APIRouter()
logger = logging.getLogger("research_rover")


def is_retry_turn(messages: list, clean_message: str) -> bool:
    """
    Check if the incoming user message is a retry or regeneration of the most
    recent user turn. Searches backwards for the latest user message in the conversation.
    Returns True if the most recent user turn matches clean_message, preventing duplicate
    user message insertion across multiple consecutive retries or after failed assistant turns.
    Returns False if there are no prior user messages or if the most recent user turn was a
    different question, ensuring older unrelated questions are not accidentally matched.
    """
    for msg in reversed(messages):
        role = getattr(msg, "role", None) or (msg.get("role") if isinstance(msg, dict) else None)
        content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
        if role == "user":
            return content == clean_message
    return False


# ─── Conversation Session Management Endpoints ───────────────────────────────

@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    request: ConversationCreate,
    session: AsyncSession = Depends(get_db)
):
    """
    Create a new persistent conversation session.
    Dataset is optional; None represents General Chat.
    """
    try:
        convo = await ConversationService.create_conversation(
            session=session,
            title=request.title,
            dataset_filename=request.dataset_filename
        )
        response = await ConversationService.get_conversation_response(session, convo.id)
        if not response:
            raise HTTPException(status_code=500, detail="Failed to load created conversation")
        return response
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    dataset_filename: Optional[str] = Query(None, description="Filter by dataset (or '__general__' for unattached)"),
    limit: int = Query(50, ge=1, le=100, description="Page limit"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_db)
):
    """
    List conversation summaries with message counts, optional dataset filtering,
    and chronological ordering by updated_at DESC.
    """
    try:
        items, total = await ConversationService.list_conversations(
            session=session,
            dataset_filename=dataset_filename,
            limit=limit,
            offset=offset
        )
        return ConversationListResponse(
            conversations=items,
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    session: AsyncSession = Depends(get_db)
):
    """
    Retrieve a conversation session and all its messages.
    """
    try:
        response = await ConversationService.get_conversation_response(session, conversation_id)
        if not response:
            raise HTTPException(status_code=404, detail=f"Conversation '{conversation_id}' not found")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation '{conversation_id}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/conversations/{conversation_id}", response_model=ConversationResponse)
async def rename_conversation(
    conversation_id: str,
    request: ConversationUpdate,
    session: AsyncSession = Depends(get_db)
):
    """
    Rename an existing conversation title.
    """
    try:
        convo = await ConversationService.update_conversation_title(
            session=session,
            conversation_id=conversation_id,
            new_title=request.title
        )
        if not convo:
            raise HTTPException(status_code=404, detail=f"Conversation '{conversation_id}' not found")
        response = await ConversationService.get_conversation_response(session, convo.id)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error renaming conversation '{conversation_id}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    session: AsyncSession = Depends(get_db)
):
    """
    Delete a conversation session and all its messages (cascade delete).
    """
    try:
        deleted = await ConversationService.delete_conversation(session, conversation_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Conversation '{conversation_id}' not found")
        return {"message": "Conversation deleted successfully", "id": conversation_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation '{conversation_id}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─── Chat Generation Endpoints (Stateless & Persistent) ──────────────────────

async def _process_chat_request(
    filename: Optional[str],
    request: ChatRequest,
    settings,
    sentence_model,
    llm,
    session: AsyncSession
) -> ChatResponse:
    """Internal helper unifying chat generation and persistence logic"""
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message parameter is required and cannot be empty")
    
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM instance is not initialized or configured")

    clean_message = request.message.strip()
    effective_filename = filename.strip() if filename and filename.strip() else (
        request.filename.strip() if request.filename and request.filename.strip() else None
    )

    conversation = None
    effective_history = request.history

    # If conversation_id is supplied, validate existence and dataset match
    if request.conversation_id:
        conversation = await ConversationService.get_conversation(session, request.conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation '{request.conversation_id}' not found"
            )

        if not ConversationService.validate_dataset_match(conversation, effective_filename):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Dataset mismatch: Conversation '{conversation.id}' is bound to dataset "
                    f"'{conversation.dataset_filename}', which does not match requested dataset '{effective_filename}'."
                )
            )

        # Idempotently record user turn by backward-searching for the latest user turn
        is_retry = is_retry_turn(conversation.messages or [], clean_message)
        if not is_retry:
            await ConversationService.add_message(
                session=session,
                conversation_id=conversation.id,
                role="user",
                content=clean_message
            )

        # If frontend didn't supply explicit history, extract recent 6 turns from database messages
        if not effective_history and conversation.messages:
            history_messages = []
            for m in conversation.messages[-7:-1]:
                if not m.is_error:
                    history_messages.append(ChatHistoryMessage(role=m.role, content=m.content))
            effective_history = history_messages

    # Execute existing Phase 1/2 RAG + Gemini generation pipeline
    chat_service = ChatService(settings, sentence_model, llm)
    response = await chat_service.generate_response(
        effective_filename,
        clean_message,
        history=effective_history
    )

    # If bound to a persistent conversation, persist assistant turn
    if conversation:
        response_text = response.response or ""
        is_error = (
            response_text.startswith("I encountered an error")
            or response_text.startswith("**Generation error:**")
            or response_text.startswith("LLM generation failed:")
        )

        assistant_msg = await ConversationService.add_message(
            session=session,
            conversation_id=conversation.id,
            role="assistant",
            content=response_text,
            is_error=is_error,
            sources=response.sources
        )

        response.conversation_id = conversation.id
        response.message_id = assistant_msg.id

    return response


def format_sse(event: str, data: Dict[str, Any]) -> str:
    """Format an SSE message conforming to spec: event: <event>\ndata: <json>\n\n"""
    json_data = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {json_data}\n\n"


@router.post("/stream")
async def chat_stream(
    request: Request,
    chat_request: ChatRequest,
    filename: Optional[str] = Query(None, description="Optional dataset filename query override"),
    settings = Depends(get_settings),
    sentence_model = Depends(get_sentence_model),
    llm = Depends(get_llm_instance),
):
    """
    Stream AI chat responses in real-time using Server-Sent Events (SSE).
    Uses short-lived database sessions before and after streaming to avoid
    holding SQLite locks across long-running LLM generation.
    """
    if not chat_request.message or not chat_request.message.strip():
        raise HTTPException(status_code=400, detail="Message parameter is required and cannot be empty")

    if llm is None:
        raise HTTPException(status_code=503, detail="LLM instance is not initialized or configured")

    clean_message = chat_request.message.strip()
    effective_filename = (
        filename.strip() if filename and filename.strip() else (
            chat_request.filename.strip() if chat_request.filename and chat_request.filename.strip() else None
        )
    )
    conversation_id = chat_request.conversation_id
    effective_history = chat_request.history

    session_factory = get_session_factory(settings_instance=settings)

    # ─── Scoped Session 1: Validate Conversation & Record User Turn ─────────────
    if conversation_id:
        async with session_factory() as session:
            conversation = await ConversationService.get_conversation(session, conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=404,
                    detail=f"Conversation '{conversation_id}' not found"
                )

            if not ConversationService.validate_dataset_match(conversation, effective_filename):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Dataset mismatch: Conversation '{conversation.id}' is bound to dataset "
                        f"'{conversation.dataset_filename}', which does not match requested dataset '{effective_filename}'."
                    )
                )

            # Idempotently record user turn by backward-searching for the latest user turn
            is_retry = is_retry_turn(conversation.messages or [], clean_message)
            if not is_retry:
                await ConversationService.add_message(
                    session=session,
                    conversation_id=conversation.id,
                    role="user",
                    content=clean_message
                )

            # If frontend didn't supply explicit history, extract recent turns from database
            if not effective_history and conversation.messages:
                history_messages = []
                for m in conversation.messages[-7:-1]:
                    if not m.is_error:
                        history_messages.append(ChatHistoryMessage(role=m.role, content=m.content))
                effective_history = history_messages

    # ─── Scoped Session 1 Closed: Proceed to Streaming Generator ────────────────

    async def event_generator():
        accumulated_text = []
        accumulated_sources = []
        is_cancelled = False
        error_occurred = False
        error_payload = None

        async def is_client_disconnected():
            return await request.is_disconnected()

        chat_service = ChatService(settings, sentence_model, llm)

        try:
            async for event in chat_service.generate_response_stream(
                filename=effective_filename,
                query=clean_message,
                history=effective_history,
                is_client_disconnected=is_client_disconnected
            ):
                event_type = event.get("event")
                event_data = event.get("data", {})

                if event_type == "delta":
                    text_chunk = event_data.get("text", "")
                    accumulated_text.append(text_chunk)
                elif event_type == "citations":
                    accumulated_sources = event_data.get("sources", [])
                elif event_type == "error":
                    error_occurred = True
                    error_payload = event_data

                yield format_sse(event_type, event_data)

                # Check if client disconnected after yielding
                if await request.is_disconnected():
                    logger.info("Client disconnect detected during streaming")
                    is_cancelled = True
                    break

        except asyncio.CancelledError:
            logger.info("Streaming request was cancelled by client")
            is_cancelled = True
        except Exception as exc:
            logger.error(f"Error during streaming event generation: {exc}")
            error_occurred = True
            err_msg = str(exc)
            err_code = "GENERATION_ERROR"
            err_lower = err_msg.lower()
            if is_daily_quota_error(exc) or "daily" in err_lower and "quota" in err_lower:
                err_code = "RATE_LIMIT"
                err_msg = "The Gemini AI rate limit was reached. Please wait a few moments and try again."
            elif "429" in err_lower or "resource_exhausted" in err_lower or "quota" in err_lower or "rate limit" in err_lower:
                err_code = "RATE_LIMIT"
                err_msg = "The Gemini AI rate limit was reached. Please wait a few moments and try again."
            elif "503" in err_lower or "unavailable" in err_lower or "overloaded" in err_lower:
                err_code = "SERVICE_UNAVAILABLE"
                err_msg = "The Gemini AI service is currently overloaded. Please try again shortly."

            error_payload = {"error": err_msg, "code": err_code}
            yield format_sse("error", error_payload)

        # ─── Scoped Session 2: Assistant Turn Persistence ───────────────────────
        full_text = "".join(accumulated_text).strip()

        if conversation_id:
            async def _persist_assistant_turn():
                try:
                    async with session_factory() as session:
                        if is_cancelled:
                            stopped_content = (
                                f"{full_text}\n\n*[Generation stopped by user]*"
                                if full_text
                                else "*[Generation stopped by user]*"
                            )
                            saved = await ConversationService.add_message(
                                session=session,
                                conversation_id=conversation_id,
                                role="assistant",
                                content=stopped_content,
                                is_error=False,
                                sources=accumulated_sources
                            )
                            logger.info(f"Successfully persisted cancelled assistant turn for conversation {conversation_id}")
                            return saved
                        elif error_occurred:
                            err_text = error_payload.get("error", "AI generation failed.") if error_payload else "AI generation failed."
                            return await ConversationService.add_message(
                                session=session,
                                conversation_id=conversation_id,
                                role="assistant",
                                content=f"**Generation error:** {err_text}",
                                is_error=True,
                                sources=accumulated_sources
                            )
                        else:
                            return await ConversationService.add_message(
                                session=session,
                                conversation_id=conversation_id,
                                role="assistant",
                                content=full_text or "No response generated.",
                                is_error=False,
                                sources=accumulated_sources
                            )
                except Exception as persist_err:
                    logger.error(f"Failed to persist assistant message in database: {persist_err}")
                    return None

            # Run in a separate task so client disconnect cancellation doesn't abort DB write
            persist_task = asyncio.create_task(_persist_assistant_turn())
            if is_cancelled:
                try:
                    await asyncio.shield(persist_task)
                except asyncio.CancelledError:
                    pass
            else:
                try:
                    saved_msg = await persist_task
                    if not error_occurred and saved_msg:
                        # Emit 'done' event ONLY after assistant message is committed to database
                        yield format_sse("done", {
                            "message_id": saved_msg.id,
                            "conversation_id": conversation_id,
                            "status": "completed"
                        })
                    elif not saved_msg and not error_occurred:
                        yield format_sse("error", {"error": "Failed to save conversation message", "code": "PERSISTENCE_ERROR"})
                except Exception as persist_err:
                    logger.error(f"Failed during persist completion: {persist_err}")
                    yield format_sse("error", {"error": "Failed to save conversation message", "code": "PERSISTENCE_ERROR"})
        else:
            # Stateless chat (no conversation_id)
            if not is_cancelled and not error_occurred:
                yield format_sse("done", {
                    "message_id": None,
                    "conversation_id": None,
                    "status": "completed"
                })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.post("/{filename}", response_model=ChatResponse)
async def chat_with_papers(
    filename: str,
    request: ChatRequest,
    settings = Depends(get_settings),
    sentence_model = Depends(get_sentence_model),
    llm = Depends(get_llm_instance),
    session: AsyncSession = Depends(get_db)
):
    """
    Chat with AI about papers in the specified CSV file.
    Supports optional persistent conversation_id in request body.
    """
    try:
        return await _process_chat_request(
            filename=filename,
            request=request,
            settings=settings,
            sentence_model=sentence_model,
            llm=llm,
            session=session
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=ChatResponse)
@router.post("/", response_model=ChatResponse, include_in_schema=False)
async def chat_with_papers_body(
    request: ChatRequest,
    settings = Depends(get_settings),
    sentence_model = Depends(get_sentence_model),
    llm = Depends(get_llm_instance),
    session: AsyncSession = Depends(get_db)
):
    """
    Chat with AI about papers (endpoint with filename in body).
    Supports optional persistent conversation_id in request body.
    """
    try:
        return await _process_chat_request(
            filename=request.filename,
            request=request,
            settings=settings,
            sentence_model=sentence_model,
            llm=llm,
            session=session
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
