from fastmcp import FastMCP
from typing import Optional
from contextlib import contextmanager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from . import crud
from .db import SessionLocal

mcp = FastMCP("Memory Server")

@contextmanager
def get_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@mcp.tool
def save_memory(user_id: str, content: str, topic: Optional[str] = None) -> dict:
    """Save a memory for a user with optional topic categorization."""
    with get_session() as session:
        return crud.save_memory(session, user_id, content, topic)

@mcp.tool
def get_memory(memory_id: str) -> Optional[dict]:
    """Retrieve a specific memory by its ID."""
    with get_session() as session:
        return crud.get_memory(session, memory_id)

@mcp.tool
def search_memories(
    user_id: str,
    query: Optional[str] = None,
    topic: Optional[str] = None
) -> list[dict]:
    """Search memories using full-text search and filters."""
    with get_session() as session:
        return crud.search_memories(session, user_id, query, topic)

def main():
    """Main entry point for the MCP server"""
    mcp.run()  # Defaults to stdio transport

if __name__ == "__main__":
    main()