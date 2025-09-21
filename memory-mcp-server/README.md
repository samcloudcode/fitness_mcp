# Memory MCP Server

An MCP (Model Context Protocol) server that provides persistent memory storage with full-text search capabilities using Supabase Postgres.

## Features

The server provides three core MCP tools:

- **save_memory** - Store memories with user_id, content, and optional topic
- **get_memory** - Retrieve a specific memory by ID
- **search_memories** - Full-text search with user_id and topic filtering

## Quick Start

### 1. Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Supabase account (free tier works)

### 2. Setup

```bash
# Clone and enter directory
cd memory-mcp-server

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your Supabase database URL
# Get this from: https://supabase.com/dashboard/project/YOUR_PROJECT/settings/database
```

### 3. Database Setup

If using existing Supabase project:
```bash
# Apply the migration using Supabase CLI
supabase link --project-ref YOUR_PROJECT_REF
supabase db push
```

Or manually run `migrations/001_create_memories.sql` in Supabase SQL Editor.

### 4. Run the Server

```bash
# Start the MCP server
uv run python -m src.mcp_server
```

## MCP Tools API

### save_memory
```json
{
  "user_id": "user123",
  "content": "Important information to remember",
  "topic": "work"  // optional
}
```

### get_memory
```json
{
  "memory_id": "b079d674-73ea-4f4a-97bc-8463050da37e"
}
```

### search_memories
```json
{
  "user_id": "user123",
  "query": "important",  // optional - uses full-text search
  "topic": "work"        // optional - filter by topic
}
```

## Testing

```bash
# Run integration tests
uv run python test_server.py
```

## Configuration

The server uses PostgreSQL with full-text search. Connection options:

- **Pooled** (recommended): `aws-1-us-east-1.pooler.supabase.com:6543`
- **Direct**: `db.YOUR_PROJECT.supabase.co:5432`

See `.env.example` for connection string format.

## Deployment

### Fly.io

```bash
fly launch
fly secrets set DATABASE_URL="your-database-url"
fly deploy
```

### Docker

```bash
docker build -t memory-mcp .
docker run -e DATABASE_URL="your-database-url" memory-mcp
```

## Project Structure

- `src/` - Core server implementation
- `migrations/` - Database schema
- `supabase/` - Supabase CLI config
- `.env.example` - Environment template

## License

MIT