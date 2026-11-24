"""
Service for persistent AI Chat conversation management
"""
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Conversation, Message
from app.models.schemas import (
    ConversationListItem,
    ConversationResponse,
    MessageResponse,
)

logger = logging.getLogger("research_rover")


class ConversationService:
    """Service handling conversation and message persistence operations"""

    @staticmethod
    def _parse_sources(sources_json: Optional[str]) -> List[Dict[str, Any]]:
        """Safely deserialize sources JSON string into list of dicts"""
        if not sources_json:
            return []
        try:
            parsed = json.loads(sources_json)
            return parsed if isinstance(parsed, list) else []
        except Exception as e:
            logger.warning(f"Failed to parse sources_json: {e}")
            return []

    @classmethod
    def _message_to_response(cls, msg: Message) -> MessageResponse:
        """Convert Message ORM model to Pydantic MessageResponse"""
        return MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            is_error=msg.is_error,
            sources=cls._parse_sources(msg.sources_json),
            created_at=msg.created_at,
        )

    @classmethod
    async def create_conversation(
        cls,
        session: AsyncSession,
        title: Optional[str] = None,
        dataset_filename: Optional[str] = None,
    ) -> Conversation:
        """Create a new conversation session"""
        clean_dataset = dataset_filename.strip() if dataset_filename and dataset_filename.strip() else None
        clean_title = title.strip() if title and title.strip() else "New Conversation"

        conversation = Conversation(
            title=clean_title,
            dataset_filename=clean_dataset,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        logger.info(f"Created conversation {conversation.id} for dataset '{clean_dataset}'")
        return conversation

    @classmethod
    async def get_conversation(
        cls,
        session: AsyncSession,
        conversation_id: str,
    ) -> Optional[Conversation]:
        """Retrieve conversation with all messages preloaded"""
        stmt = (
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def get_conversation_response(
        cls,
        session: AsyncSession,
        conversation_id: str,
    ) -> Optional[ConversationResponse]:
        """Retrieve conversation and map directly to Pydantic response"""
        conversation = await cls.get_conversation(session, conversation_id)
        if not conversation:
            return None

        messages_response = [cls._message_to_response(m) for m in conversation.messages]
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            dataset_filename=conversation.dataset_filename,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=messages_response,
        )

    @classmethod
    async def list_conversations(
        cls,
        session: AsyncSession,
        dataset_filename: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[ConversationListItem], int]:
        """
        List conversations with message count, optional dataset filtering, and pagination.
        Ordered by most recent activity (updated_at DESC).
        """
        # Base query for conversation objects
        base_query = select(Conversation)

        if dataset_filename is not None:
            clean_filter = dataset_filename.strip()
            if clean_filter == "__general__" or clean_filter.lower() == "null":
                base_query = base_query.where(Conversation.dataset_filename.is_(None))
            elif clean_filter:
                base_query = base_query.where(Conversation.dataset_filename == clean_filter)

        # Count total matching
        count_stmt = select(func.count()).select_from(base_query.subquery())
        total_res = await session.execute(count_stmt)
        total = total_res.scalar_one()

        # Paginated fetch with message count
        query = (
            base_query.options(selectinload(Conversation.messages))
            .order_by(desc(Conversation.updated_at))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        conversations = result.scalars().all()

        items = [
            ConversationListItem(
                id=c.id,
                title=c.title,
                dataset_filename=c.dataset_filename,
                message_count=len(c.messages),
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in conversations
        ]

        return items, total

    @classmethod
    async def update_conversation_title(
        cls,
        session: AsyncSession,
        conversation_id: str,
        new_title: str,
    ) -> Optional[Conversation]:
        """Rename conversation title"""
        conversation = await cls.get_conversation(session, conversation_id)
        if not conversation:
            return None

        conversation.title = new_title.strip()
        conversation.updated_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(conversation)
        logger.info(f"Renamed conversation {conversation_id} to '{conversation.title}'")
        return conversation

    @classmethod
    async def delete_conversation(
        cls,
        session: AsyncSession,
        conversation_id: str,
    ) -> bool:
        """Delete conversation and cascade deletion to all messages"""
        conversation = await cls.get_conversation(session, conversation_id)
        if not conversation:
            return False

        await session.delete(conversation)
        await session.commit()
        logger.info(f"Deleted conversation {conversation_id}")
        return True

    @classmethod
    async def add_message(
        cls,
        session: AsyncSession,
        conversation_id: str,
        role: str,
        content: str,
        is_error: bool = False,
        sources: Optional[List[Dict[str, Any]]] = None,
    ) -> Message:
        """
        Add a message to a conversation.
        If the conversation still has the default title and this is the first user turn,
        auto-generates a title from the query.
        """
        conversation = await cls.get_conversation(session, conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID '{conversation_id}' not found.")

        sources_json = json.dumps(sources) if sources else None

        message = Message(
            conversation=conversation,
            role=role,
            content=content,
            is_error=is_error,
            sources_json=sources_json,
            created_at=datetime.now(timezone.utc),
        )
        session.add(message)
        if message not in conversation.messages:
            conversation.messages.append(message)

        # Auto-generate title on first user turn if still default
        if role == "user" and (conversation.title == "New Conversation" or not conversation.title):
            clean_prompt = " ".join(content.strip().split())
            if clean_prompt:
                # Truncate at word boundary under 45 chars
                if len(clean_prompt) > 45:
                    truncated = clean_prompt[:45].rsplit(" ", 1)[0]
                    conversation.title = truncated if truncated else clean_prompt[:45]
                else:
                    conversation.title = clean_prompt

        conversation.updated_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(message)
        return message

    @staticmethod
    def validate_dataset_match(conversation: Conversation, requested_dataset: Optional[str]) -> bool:
        """
        Check that the conversation's bound dataset matches the request.
        None or empty strings are treated as General Chat.
        """
        expected = conversation.dataset_filename or None
        actual = (requested_dataset.strip() if requested_dataset and requested_dataset.strip() else None)
        return expected == actual
