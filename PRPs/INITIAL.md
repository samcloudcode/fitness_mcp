## FEATURE:

Build an MCP memory server using SQLAlchemy ORM (sync) with Supabase Postgres and Fly.io deployment. The server provides three core tools via MCP protocol (stdio only):
- `save_memory`: Store memories with user_id, content, and optional topic
- `get_memory`: Retrieve a specific memory by ID
- `search_memories`: Search memories using full-text search, filtered by user_id, query, and/or topic

Stack:
- Python 3.11+
- SQLAlchemy 2.x ORM (sync mode) with psycopg3 (binary)
- Supabase Postgres with FTS (full-text search)
- FastMCP for MCP protocol implementation
- Fly.io hosting (single small VM)
- Single DATABASE_URL secret

Architecture:
- Clean separation: `db.py` (models), `crud.py` (database operations), `mcp_server.py` (MCP tools)
- Simple Supabase CLI SQL migrations (no Alembic)
- UUID primary keys with `gen_random_uuid()`
- Built-in FTS via generated tsvector column
- Future-ready for pgvector semantic search

## EXAMPLES:

No existing examples provided. Implementation should follow the provided specification exactly as written.

## DOCUMENTATION:

- Use context tools to review latest documentation as needed during development
- Key resources: SQLAlchemy 2.x ORM docs, FastMCP/MCP docs, Supabase CLI docs, Fly.io deployment guides

## OTHER CONSIDERATIONS:

- Keep it simple and elegant - no over-engineering
- Stick to sync SQLAlchemy for simplicity (can migrate to async later if needed)
- One secret (DATABASE_URL), one migration path, three tools
- Repository structure must match the specified layout exactly
- Use Supabase CLI for migrations, not Alembic
- Deploy via Fly.io with the provided Dockerfile and fly.toml configuration