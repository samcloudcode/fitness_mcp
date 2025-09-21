from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.sql import func
from typing import Optional
from db import Memory
import uuid

def save_memory(session: Session, user_id: str, content: str,
                topic: Optional[str] = None) -> dict:
    """Create and save a new memory."""
    memory = Memory(
        user_id=user_id,
        content=content,
        topic=topic
    )
    session.add(memory)
    session.commit()
    session.refresh(memory)

    return {
        "id": str(memory.id),
        "user_id": memory.user_id,
        "content": memory.content,
        "topic": memory.topic,
        "created_at": memory.created_at.isoformat(),
        "updated_at": memory.updated_at.isoformat() if memory.updated_at else None
    }

def get_memory(session: Session, memory_id: str) -> Optional[dict]:
    """Retrieve a memory by ID."""
    try:
        memory_uuid = uuid.UUID(memory_id)
    except ValueError:
        return None

    memory = session.get(Memory, memory_uuid)
    if not memory:
        return None

    return {
        "id": str(memory.id),
        "user_id": memory.user_id,
        "content": memory.content,
        "topic": memory.topic,
        "created_at": memory.created_at.isoformat(),
        "updated_at": memory.updated_at.isoformat() if memory.updated_at else None
    }

def search_memories(session: Session, user_id: str,
                   query: Optional[str] = None,
                   topic: Optional[str] = None) -> list[dict]:
    """Search memories with FTS and filters."""
    stmt = select(Memory).where(Memory.user_id == user_id)

    if query:
        # Use PostgreSQL full-text search
        stmt = stmt.where(
            func.to_tsvector('english', Memory.content).bool_op('@@')(
                func.plainto_tsquery('english', query)
            )
        )

    if topic:
        stmt = stmt.where(Memory.topic == topic)

    stmt = stmt.order_by(Memory.created_at.desc()).limit(100)

    results = session.execute(stmt).scalars().all()

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