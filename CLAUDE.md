# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for memory storage with full-text search capabilities using PostgreSQL. The server implements three core tools via FastMCP:
- `save_memory`: Store memories with user ID, content, and optional topic
- `get_memory`: Retrieve a specific memory by ID
- `search_memories`: Search memories using PostgreSQL full-text search

## Development Commands

### Running Tests
```bash
# Run the test script directly
uv run python tests/test_memory_server.py

# Run pytest (if test files are added)
uv run pytest
```

### Running the Server
```bash
# Start the MCP server
uv run python -m src.mcp_server

# Or use the script entry point
uv run memory-server
```

### Database Setup
```bash
# Apply database migrations
psql $DATABASE_URL < migrations/001_create_memories.sql
```

### Dependency Management
```bash
# Install/sync dependencies
uv sync

# Add new dependencies
uv add <package-name>
```

## Architecture

### Core Components

1. **MCP Server** (`src/mcp_server.py`): FastMCP server implementing the three memory tools with context managers for database sessions

2. **Database Models** (`src/memory/db.py`): SQLAlchemy ORM model for the Memory table with PostgreSQL full-text search support via generated tsvector columns

3. **CRUD Operations** (`src/memory/crud.py`): Database operations handling memory creation, retrieval, and search with FTS queries using `plainto_tsquery`

4. **Database Configuration**:
   - Uses SQLAlchemy 2.x with psycopg3 (binary)
   - Connection pooling configured with pool_size=5, max_overflow=10
   - Automatic URL conversion from postgresql:// to postgresql+psycopg://

### Key Implementation Details

- **Full-Text Search**: PostgreSQL FTS using generated tsvector columns and GIN indexes for efficient text search
- **UUID Generation**: Server-side UUID generation using `gen_random_uuid()` for consistency
- **Session Management**: All database operations use context managers to ensure proper cleanup
- **Environment Variables**: Requires `DATABASE_URL` environment variable (loaded from `.env`)
- **Transport**: Uses stdio transport (default for FastMCP), not HTTP

## Database Schema

The `memories` table includes:
- UUID primary key with server-side generation
- user_id (indexed) for multi-tenant support
- content and optional topic fields
- Generated tsvector column for FTS on content + topic
- Automatic updated_at trigger
- Prepared embedding column for future pgvector integration