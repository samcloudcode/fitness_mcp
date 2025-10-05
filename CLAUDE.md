# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a fitness tracking MCP (Model Context Protocol) server built with FastMCP and PostgreSQL. The server provides a comprehensive system for managing fitness goals, training plans, workouts, and knowledge through a unified entry-based architecture with full-text search capabilities.

### Core Concepts

**Unified Entry Model**: All data (goals, plans, workouts, metrics, notes, etc.) is stored in a single `entries` table. Entries fall into two categories:
- **Durable Items** (with `key`): Goals, plans, preferences, knowledge, principles - identified by `(user_id, kind, key)` unique constraint. Updates via upsert.
- **Events** (no `key`): Workouts, metrics, notes - timestamped occurrences identified by UUID. Creates new entry each time.

**Planning Hierarchy**: The system supports temporal planning from strategies (long-term/short-term) → plans (3-6 weeks) → plan-steps (weekly) → workout events (sessions), all linked via `parent_key`.

**Temporal Context (Plans)**: Plans with `start_date` and `duration_weeks` in attrs get automatic temporal context in overview:
- `current_week`: Which week of plan (computed from today - start_date)
- `total_weeks`: Total duration
- `weeks_remaining`: How many weeks left
- `progress_pct`: Progress percentage (0-100)
- `temporal_status`: 'pending', 'active', or 'completed'

**Progress Tracking (Goals)**: Goals with `baseline` and `target` in attrs enable progress tracking. Baseline includes starting value and date. Current progress derived from recent workout/metric logs.

**Contraindication Patterns**: Knowledge entries with `contraindication` tag + attrs for `affected_exercises` and `safe_alternatives` enable injury-aware exercise selection.

**Observability**: Integrated Logfire instrumentation for SQLAlchemy operations, configurable via environment variables (`LOGFIRE_SEND_TO_LOGFIRE`, `ENVIRONMENT`).

## Development Commands

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_mcp_tools.py

# Run tests with verbose output
uv run pytest -v

# Run tests matching a pattern
uv run pytest -k "test_upsert"
```

### Running the Server
```bash
# Start the MCP server (stdio transport)
uv run python -m src.mcp_server

# Or use the script entry point
uv run memory-server

# Test server responds (5 second timeout)
timeout 5s uv run python -m src.mcp_server
```

### Database Setup
```bash
# Apply migrations in order
psql $DATABASE_URL < migrations/001_create_memories.sql
psql $DATABASE_URL < migrations/002_create_entries.sql

# Check database connection
uv run python -c "from src.memory.db import engine; from sqlalchemy import text; engine.connect().execute(text('SELECT 1'))"
```

### Dependency Management
```bash
# Sync dependencies
uv sync

# Add new dependencies
uv add <package-name>

# Add dev dependencies
uv add --dev <package-name>
```

## Architecture

### Key Design Patterns

**UPSERT Pattern**: All durable items use PostgreSQL's `ON CONFLICT DO UPDATE` via `(user_id, kind, key)` unique constraint. This ensures:
- Same key = update existing item (don't duplicate)
- New key = insert new item
- Atomic operations with automatic `updated_at` timestamp

**Event Immutability**: Events (workouts, metrics, notes) have no `key` and are identified by UUID. Updates via `update_event()` and `delete_event()` tools using the UUID.

**Full-Text Search**: PostgreSQL FTS using generated tsvector column on `(key + content)` with GIN index. Searches use `plainto_tsquery` for user-friendly query parsing.

**Connection Pooling**: Optimized for Supabase pooler:
- Small local pool (pool_size=2, max_overflow=3) since Supabase handles pooling
- TCP keepalives configured for connection stability
- 30-second statement timeout
- No pool recycling (Supabase manages connection lifecycle)

### Core Components

**MCP Server** ([src/mcp_server.py](src/mcp_server.py)):
- 16 FastMCP tools for fitness tracking (upsert_item, log_event, get_overview, search_entries, etc.)
- Context managers (`get_session()`) for database session lifecycle
- User ID resolution from environment variables (`FITNESS_USER_ID` or `DEFAULT_USER_ID`)
- Date/datetime parsing with ISO 8601 format handling
- Logfire instrumentation with auto-tracing for CRUD operations

**CRUD Operations** ([src/memory/crud.py](src/memory/crud.py)):
- `upsert_item()`: PostgreSQL upsert for durable items using `ON CONFLICT`
- `bulk_upsert_items()`: Batch upsert with single statement
- `log_event()`: Insert events without keys (creates new entry each time)
- `update_event()` / `delete_event()`: Event modifications by UUID
- `get_overview()`: Structured aggregation of user data by kind with status grouping
- `search_entries()`: Full-text search across all entries
- Helper functions: `_clean_entry()` (output formatting), `_group_by_status()` (status grouping)

**Database Models** ([src/memory/db.py](src/memory/db.py)):
- `Entry` model: Unified table for all data types (goals, plans, workouts, metrics, etc.)
- Key columns: `id` (UUID), `user_id`, `kind`, `key` (nullable), `content`, `status`, `priority`, `tags`, `occurred_at`, `due_date`, `attrs` (JSONB)
- Indexes: GIN FTS index, compound index on `(user_id, kind, parent_key)`, `(user_id, occurred_at)` for events
- Unique constraint: `(user_id, kind, key)` for item identity
- Server-side defaults: `gen_random_uuid()` for id, `{}` for attrs JSONB

### Data Flow

```
User Request
    ↓
FastMCP Tool (src/mcp_server.py:76-789)
    ↓
get_session() context manager
    ↓
CRUD function (src/memory/crud.py)
    ↓
SQLAlchemy ORM → PostgreSQL
    ↓
Logfire span tracking (auto-instrumentation)
    ↓
Result serialization & return
```

### Important Implementation Details

**Attribute Handling**: `attrs` is JSONB accepting any valid JSON structure (arrays, nested objects). The MCP client may validate attrs more strictly than the backend - if validation fails, retry without attrs and inform the user.

**Status Values**: No enum constraint - common values are `active`, `archived`, `achieved`, `paused`, `open` (for issues). Overview excludes `archived` items.

**Timestamp Handling**:
- `occurred_at`: For events (workouts, metrics, notes) - when the event happened
- `due_date`: For items with deadlines (goals, plan-steps)
- `created_at` / `updated_at`: Automatic timestamps for all entries

**Parent-Child Relationships**: `parent_key` links entries hierarchically:
- Plan-steps reference plans: `parent_key='squat-progression'`
- Workouts reference plans: `parent_key='squat-progression'`
- Strategies reference each other: short-term → long-term
- Overview nests plan-steps under their parent plans

**Kind Values**: No enforced enum - core kinds are `goal`, `plan`, `plan-step`, `strategy`, `preference`, `knowledge`, `principle`, `current`, `workout`, `workout-plan`, `metric`, `note`, `issue`. New kinds can be added without schema changes.

**User Isolation**: All queries filter by `user_id` from environment variable. Multi-tenant by design but typically single-user in practice.

### Testing Architecture

**Test Structure** ([tests/](tests/)):
- `conftest.py`: Pytest fixtures for session/engine management
- `test_entries_crud.py`: CRUD operation tests
- `test_event_updates.py`: Event update/delete tests
- `test_mcp_tools.py`: End-to-end MCP tool tests

**Key Test Patterns**:
- Use fixtures for database session setup/teardown
- Test both item (with key) and event (without key) paths
- Verify upsert behavior (insert vs update)
- Test search and filtering with various parameters

## Environment Variables

Required:
- `DATABASE_URL`: PostgreSQL connection string (auto-converted from `postgresql://` to `postgresql+psycopg://`)
- `FITNESS_USER_ID` or `DEFAULT_USER_ID`: User identifier for data isolation

Optional:
- `LOGFIRE_SEND_TO_LOGFIRE`: Enable Logfire remote logging (default: `false`)
- `ENVIRONMENT`: Environment name for Logfire (default: `development`)

## Fitness Coach Instructions

[FITNESS_COACH_INSTRUCTIONS.md](FITNESS_COACH_INSTRUCTIONS.md) contains comprehensive guidance for LLMs using this MCP server. Key points:

**Critical Patterns**:
- Always call `get_overview()` at session start for context
- Use `upsert_item()` for durable data (never duplicate same key)
- Use `log_event()` for timestamped events (creates new each time)
- Archive items (`status='archived'`) instead of deleting (preserves history)
- Include comprehensive attrs in workout logs (exercises, RPE, notes)

**Common Mistakes to Avoid**:
- Using backticks for strings (use `'goal'` not `` `goal` ``)
- Stringifying attrs (`attrs='{"key": "value"}'` instead of `attrs={'key': 'value'}`)
- Creating duplicate items instead of updating existing ones
- Deleting items when archiving would be better

**Tool Selection**:
- `upsert_item()`: Goals, plans, preferences, knowledge (anything with a memorable key)
- `log_event()`: Workouts, metrics, notes (timestamped occurrences)
- `update_event()`: Fix logged events after the fact (add RPE, correct mistakes)
- `archive_items()`: Bulk archiving of items by kind/status/tags
- `search_entries()`: Find entries by content when key unknown
- `get_overview()`: Structured view of all active data (excludes archived, issues)
