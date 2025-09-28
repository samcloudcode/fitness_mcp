from fastmcp import FastMCP
from typing import Optional
from contextlib import contextmanager
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from sqlalchemy import text

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

# Configure Logfire before other imports
import logfire
from logfire import ConsoleOptions

# Configure Logfire for the MCP server
logfire.configure(
    send_to_logfire=os.getenv('LOGFIRE_SEND_TO_LOGFIRE', 'false').lower() == 'true',
    environment=os.getenv('ENVIRONMENT', 'development'),
    console=ConsoleOptions(min_log_level='info'),
    min_level='info',
    distributed_tracing=False,  # MCP server typically runs standalone
)

# Enable SQLAlchemy auto-instrumentation
logfire.install_auto_tracing(
    modules=['src.memory.crud', 'src.memory.db'],
    min_duration=0.01  # Track operations taking 10ms or more
)

# Instrument SQLAlchemy
logfire.instrument_sqlalchemy()

from src.memory import crud
from src.memory.db import SessionLocal, engine

mcp = FastMCP("Memory Server")

# Warm up the connection pool at startup
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        logfire.info(
            'database connection pool initialized',
            pool_size=engine.pool.size(),
            checked_out=engine.pool.checkedout(),
            overflow=engine.pool.overflow(),
            total=engine.pool.checkedin()
        )
except Exception as e:
    logfire.error('failed to initialize database pool', error=str(e))
    raise

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
    with logfire.span('save memory', user_id=user_id, topic=topic, content_length=len(content)):
        try:
            with get_session() as session:
                result = crud.save_memory(session, user_id, content, topic)
                logfire.info(
                    'memory saved successfully',
                    memory_id=result['id'],
                    user_id=user_id,
                    topic=topic,
                    content_length=len(content)
                )
                return result
        except Exception as err:
            logfire.exception('failed to save memory', user_id=user_id, topic=topic)
            raise

@mcp.tool
def get_memory(memory_id: str) -> Optional[dict]:
    """Retrieve a specific memory by its ID."""
    with logfire.span('get memory', memory_id=memory_id):
        try:
            with get_session() as session:
                result = crud.get_memory(session, memory_id)
                if result:
                    logfire.info(
                        'memory retrieved successfully',
                        memory_id=memory_id,
                        user_id=result['user_id'],
                        has_topic=result['topic'] is not None
                    )
                else:
                    logfire.warning('memory not found', memory_id=memory_id)
                return result
        except Exception as err:
            logfire.exception('failed to get memory', memory_id=memory_id)
            raise

@mcp.tool
def search_memories(
    user_id: str,
    query: Optional[str] = None,
    topic: Optional[str] = None
) -> list[dict]:
    """Search memories using full-text search and filters."""
    with logfire.span('search memories', user_id=user_id, query=query, topic=topic):
        try:
            with get_session() as session:
                results = crud.search_memories(session, user_id, query, topic)
                logfire.info(
                    'memory search completed',
                    user_id=user_id,
                    query=query,
                    topic=topic,
                    result_count=len(results),
                    has_query=query is not None,
                    has_topic_filter=topic is not None
                )
                return results
        except Exception as err:
            logfire.exception('failed to search memories', user_id=user_id, query=query, topic=topic)
            raise

def main():
    """Main entry point for the MCP server"""
    # Log startup and initialization
    with logfire.span('mcp server startup'):
        logfire.info('starting memory mcp server', tools=['save_memory', 'get_memory', 'search_memories'])
        logfire.info('logfire configured', environment=os.getenv('ENVIRONMENT', 'development'))
        logfire.info('database connection initialized')

    # Run the server (this blocks until shutdown)
    try:
        logfire.info('mcp server ready and listening')
        mcp.run()  # Defaults to stdio transport
    except Exception as err:
        logfire.exception('mcp server error during execution')
        raise

if __name__ == "__main__":
    main()