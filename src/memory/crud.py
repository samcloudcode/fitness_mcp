from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.sql import func
from typing import Optional
from .db import Memory
import uuid
import logfire
from pydantic import BaseModel
from datetime import datetime

# Pydantic models for structured logging
class MemoryCreateLog(BaseModel):
    user_id: str
    content_length: int
    topic: Optional[str] = None

class MemoryResultLog(BaseModel):
    memory_id: str
    user_id: str
    topic: Optional[str] = None
    created_at: datetime

class SearchResultLog(BaseModel):
    user_id: str
    query: Optional[str] = None
    topic: Optional[str] = None
    result_count: int
    has_fts_query: bool
    has_topic_filter: bool

def save_memory(session: Session, user_id: str, content: str,
                topic: Optional[str] = None) -> dict:
    """Create and save a new memory."""
    with logfire.span('create memory record', user_id=user_id, content_length=len(content)):
        try:
            # Log the creation attempt
            create_log = MemoryCreateLog(
                user_id=user_id,
                content_length=len(content),
                topic=topic
            )
            logfire.info('creating memory record', create_attempt=create_log)

            memory = Memory(
                user_id=user_id,
                content=content,
                topic=topic
            )
            session.add(memory)

            with logfire.span('commit memory transaction'):
                session.commit()
                session.refresh(memory)

            # Log successful creation
            result_log = MemoryResultLog(
                memory_id=str(memory.id),
                user_id=memory.user_id,
                topic=memory.topic,
                created_at=memory.created_at
            )
            logfire.info('memory record created', result=result_log)

            return {
                "id": str(memory.id),
                "user_id": memory.user_id,
                "content": memory.content,
                "topic": memory.topic,
                "created_at": memory.created_at.isoformat(),
                "updated_at": memory.updated_at.isoformat() if memory.updated_at else None
            }
        except Exception as err:
            logfire.exception('failed to create memory record', user_id=user_id, content_length=len(content))
            raise

def get_memory(session: Session, memory_id: str) -> Optional[dict]:
    """Retrieve a memory by ID."""
    with logfire.span('retrieve memory by id', memory_id=memory_id):
        try:
            # Validate UUID format
            with logfire.span('validate memory id'):
                try:
                    memory_uuid = uuid.UUID(memory_id)
                    logfire.info('memory id validated', memory_id=memory_id)
                except ValueError:
                    logfire.warning('invalid memory id format', memory_id=memory_id)
                    return None

            # Query the database
            with logfire.span('query memory from database'):
                memory = session.get(Memory, memory_uuid)

            if not memory:
                logfire.info('memory not found in database', memory_id=memory_id)
                return None

            # Log successful retrieval
            result_log = MemoryResultLog(
                memory_id=str(memory.id),
                user_id=memory.user_id,
                topic=memory.topic,
                created_at=memory.created_at
            )
            logfire.info('memory retrieved from database', result=result_log)

            return {
                "id": str(memory.id),
                "user_id": memory.user_id,
                "content": memory.content,
                "topic": memory.topic,
                "created_at": memory.created_at.isoformat(),
                "updated_at": memory.updated_at.isoformat() if memory.updated_at else None
            }
        except Exception as err:
            logfire.exception('failed to retrieve memory', memory_id=memory_id)
            raise

def search_memories(session: Session, user_id: str,
                   query: Optional[str] = None,
                   topic: Optional[str] = None) -> list[dict]:
    """Search memories with FTS and filters."""
    with logfire.span('search memories in database', user_id=user_id, has_query=query is not None, has_topic=topic is not None):
        try:
            # Build the query
            with logfire.span('build search query'):
                stmt = select(Memory).where(Memory.user_id == user_id)

                if query:
                    logfire.info('adding full-text search filter', query=query)
                    # Use PostgreSQL full-text search
                    stmt = stmt.where(
                        func.to_tsvector('english', Memory.content).bool_op('@@')(
                            func.plainto_tsquery('english', query)
                        )
                    )

                if topic:
                    logfire.info('adding topic filter', topic=topic)
                    stmt = stmt.where(Memory.topic == topic)

                stmt = stmt.order_by(Memory.created_at.desc()).limit(100)

            # Execute the search
            with logfire.span('execute search query'):
                results = session.execute(stmt).scalars().all()

            # Log search results
            search_log = SearchResultLog(
                user_id=user_id,
                query=query,
                topic=topic,
                result_count=len(results),
                has_fts_query=query is not None,
                has_topic_filter=topic is not None
            )
            logfire.info('search query executed', search_result=search_log)

            return [
                {
                    "id": str(memory.id),
                    "user_id": memory.user_id,
                    "content": memory.content,
                    "topic": memory.topic,
                    "created_at": memory.created_at.isoformat(),
                    "updated_at": memory.updated_at.isoformat() if memory.updated_at else None
                }
                for memory in results
            ]
        except Exception as err:
            logfire.exception('failed to search memories', user_id=user_id, query=query, topic=topic)
            raise