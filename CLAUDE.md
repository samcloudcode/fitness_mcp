# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simplified fitness tracking MCP server following Claude Code's philosophy: **minimal tool surface (6 tools), maximum flexibility**. Built with FastMCP and PostgreSQL, using a unified entry-based architecture where all data goes in the content field as natural text.

### 🎯 6 Core Tools (Down from 17)

1. **`upsert`** - Create/update items with identity (has key)
2. **`log`** - Record timestamped events (no key) or update by ID
3. **`overview`** - Lightweight scan of all data (truncated)
4. **`get`** - Pull full details by keys or filters
5. **`search`** - Find by content when key unknown
6. **`archive`** - Soft delete (set status='archived')

### Core Concepts

**Two Data Patterns**:
- **Items** (has `key`): Durable things you update - goals, plans, knowledge. Same key = replace.
- **Events** (no `key`): Timestamped occurrences - workouts, metrics, notes. Always creates new.

**Simplified Schema** (9 columns, down from 14):
- Removed: `priority`, `tags`, `parent_key`, `due_date`, `attrs` (everything goes in content now)
- Binary status: Only `active` or `archived` (enforced via check constraint)
- Everything goes in content field as natural text
- **Overview excludes archived entries** for clean working context

**Everything in Content**: All data goes in the content field as natural text. Want to track plan progress? Put "Week 3 of 8" in content. Want tags? Put "Tags: injury-prevention, squat" in content. Simple and searchable.

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
# Start the simplified MCP server (6 tools)
uv run python -m src.mcp_server_simple

# Or use the script entry point
uv run memory-server

# Test server responds (5 second timeout)
timeout 5s uv run python -m src.mcp_server_simple

# Run the old 17-tool version if needed
uv run python -m src.mcp_server
```

### Database Setup
```bash
# Apply migrations in order
source .env && psql "$DATABASE_URL" < migrations/001_create_memories.sql
source .env && psql "$DATABASE_URL" < migrations/002_create_entries.sql
source .env && psql "$DATABASE_URL" < migrations/003_simplify_schema.sql  # NEW: Simplifies to 10 columns

# Check database connection
uv run python -c "from src.memory.db import engine; from sqlalchemy import text; engine.connect().execute(text('SELECT 1'))"

# Check schema after migration
source .env && psql "$DATABASE_URL" -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'entries';"
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

## Simplified Tool Usage Examples

### Quick Start - The 6 Tools

```python
# 1. UPSERT - Items with identity
# Put EVERYTHING in content field - keep it simple!
upsert(kind='goal', key='bench-225', content='Bench 225lbs x5 by March. Started at 185 in Sept.')

# 2. LOG - Timestamped events
# Full workout details in content, one line
log(kind='workout', content='Lower: Squats 5x5 @ 225lbs RPE 7, RDL 3x8 @ 185')

# 3. OVERVIEW - Scan everything (truncated)
overview()  # Returns all ACTIVE items (archived excluded), verbose content truncated to 100 chars

# 4. GET - Pull full details
get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])  # Specific items
get(kind='workout', limit=14)  # Last 2 weeks of workouts (safety first!)

# 5. SEARCH - Find by content
search('knee pain', kind='knowledge')

# 6. ARCHIVE - Soft delete
archive(kind='goal', key='old-goal')  # Specific item
archive(kind='preference')  # Bulk archive all active preferences
```

### The "Everything in Content" Principle

**Pure simplicity** - everything goes in the `content` field as natural text:

```python
# ✅ Everything in content as natural text
upsert(
    kind='knowledge',
    key='knee-issue',
    content='Knee pain from narrow stance squats. Wider stance + "spread floor" cue fixed it. Started Sept 2024. Tags: injury-prevention, squat-form'
)

# ✅ Plans with dates and progress in content
upsert(
    kind='plan',
    key='squat-8wk',
    content='Linear squat progression: 275→315lbs (+5/wk). 8 weeks starting Jan 1. Week 3 of 8. Deload week 4.'
)

# ✅ Workouts with all details in one line
log(
    kind='workout',
    content='Lower (52min): Squats 5x5 @ 245 RPE 7, RDL 3x8 @ 185 RPE 6'
)
```

Natural language, fully searchable, no structured data complexity.

### Common Workflows

**Goal Tracking:**
```python
# Create goal with progress in content
upsert(
    kind='goal',
    key='bench-225',
    content='Bench 225lbs x5 by March. Started at 185 in Sept.'
)

# Log progress
log(kind='workout', content='Bench 3x5 @ 205lbs RPE 7')

# Check status
overview()  # See all goals
```

**Knowledge Management:**
```python
# Store knowledge with tags in content
upsert(
    kind='knowledge',
    key='knee-health',
    content='Keep knees tracking over toes, avoid narrow stance. Tags: injury-prevention, squat-form'
)

# Find relevant info
search('knee pain')  # When you don't know the key
get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])  # When you know the key
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
- 17 FastMCP tools for fitness tracking (upsert_item, log_event, get_overview, get_items_detail, search_entries, etc.)
- Context managers (`get_session()`) for database session lifecycle
- User ID resolution from environment variables (`FITNESS_USER_ID` or `DEFAULT_USER_ID`)
- Date/datetime parsing with ISO 8601 format handling
- Logfire instrumentation with auto-tracing for CRUD operations

**CRUD Operations** ([src/memory/crud.py](src/memory/crud.py)):
- `upsert_item()`: PostgreSQL upsert for durable items using `ON CONFLICT`
- `bulk_upsert_items()`: Batch upsert with single statement
- `log_event()`: Insert events without keys (creates new entry each time)
- `update_event()` / `delete_event()`: Event modifications by UUID
- `get_overview()`: Returns ALL items with truncated content (100 chars) for efficient scanning
- `get_items_by_keys()`: Fetch full content for specific items by (kind, key) tuples
- `search_entries()`: Full-text search across all entries
- Helper functions: `_clean_entry()` (output formatting with optional truncation), `_group_by_status()` (status grouping)

**Database Models** ([src/memory/db.py](src/memory/db.py)):
- `Entry` model: Unified table for all data types (goals, plans, workouts, metrics, etc.)
- Key columns (9 total): `id` (UUID), `user_id`, `kind`, `key` (nullable), `content`, `status`, `occurred_at`, `created_at`, `updated_at`
- Indexes: GIN FTS index on (key + content), compound index on `(user_id, kind)`, `(user_id, occurred_at)` for events
- Unique constraint: `(user_id, kind, key)` for item identity
- Server-side defaults: `gen_random_uuid()` for id, `now()` for created_at

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

**Overview Truncation Pattern**: `get_overview()` returns ALL active items but truncates verbose content to 100 chars (knowledge, principles, preferences, workouts). This enables efficient context scanning without loading full entries. Use `get()` to fetch complete content for specific items. Goals/plans/current show full content (should be concise).

**Pull-Based Context Composition**: LLMs should scan truncated overview, then pull full details only for relevant items using `get()` or `search()`. Multiple small queries >> one giant dump.

**Content Brevity Guidelines**: Store concise summaries, not textbooks:
- Goals: 10-30 words ("Bench 225lbs x5 by March. Started at 185 in Sept.")
- Knowledge: 20-50 words, user-specific observations only (not general science LLMs already know)
- Plans: 30-60 words with dates and progression details
- Workouts: One line with all details ("Lower: Squats 5x5 @ 245 RPE 7, RDL 3x8 @ 185")
- See [FITNESS_COACH_INSTRUCTIONS_SIMPLE.md](FITNESS_COACH_INSTRUCTIONS_SIMPLE.md) for detailed guidelines

**Status Values**: Enforced binary constraint - only `active` or `archived` allowed. Overview **excludes** `archived` items for clean working context.

**Timestamp Handling**:
- `occurred_at`: For events (workouts, metrics, notes) - when the event happened
- `created_at` / `updated_at`: Automatic timestamps for all entries
- Due dates, deadlines: Put directly in content ("Due: 2025-12-31")

**Relationships**: Express in content as natural text:
- "Part of squat-progression plan"
- "Week 3 of 8-week cycle"
- "Relates to knee-health knowledge entry"

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

[FITNESS_COACH_INSTRUCTIONS_SIMPLE.md](FITNESS_COACH_INSTRUCTIONS_SIMPLE.md) contains comprehensive guidance for LLMs using this MCP server. Key points:

**Critical Patterns**:
- **Two-Phase Rule**: Propose workouts/plans first, save ONLY after user approval
  - Exception: User provides completed info ("I just did squats") → save immediately
- Always call `overview()` at session start - returns ALL active items (archived excluded)
- Verbose content truncated to 100 chars - use `get()` to pull full details
- Use `upsert()` for durable data (same key = update, never duplicates)
- Use `log()` for timestamped events (creates new each time)
- Archive items instead of deleting (preserves history)

**Data Fetching Rules (Safety First)**:
- **Before programming workouts**: ALWAYS fetch ALL knowledge (injuries/limitations)
- **Recent training context**: Fetch 2 weeks of workouts (`limit=14`, usually 6-12 sessions)
- **Active programs**: Fetch all plans to understand current training phase
- Better to over-fetch safety info than miss critical limitations

**Content Brevity & "Everything in Content" Principle**:
- Goals: 10-30 words ("Bench 225lbs x5 by March. Started at 185 in Sept.")
- Knowledge: 20-50 words, user-specific observations only
- Plans: 30-60 words with dates and progression details
- Workouts: One line ("Lower: Squats 5x5 @ 245 RPE 7, RDL 3x8 @ 185")
- **Put everything in content field** - use attrs only for programmatic access (rare)

**Common Mistakes to Avoid**:
- **Saving before approval**: Propose workouts/plans first, save ONLY after user agrees
- Over-structuring data in attrs instead of natural text in content
- Creating duplicate items instead of updating existing ones (same key = update)
- Storing textbook knowledge instead of user-specific observations (20-50 words max)
- Missing safety checks: ALWAYS fetch all knowledge before programming workouts

**Workflow Examples**:
- **User wants workout**: `overview()` → `get(kind='knowledge')` → `get(kind='workout', limit=14)` → `get(kind='plan')` → **Propose (don't save)** → Get approval → `log()`
- **User provides info**: Save immediately with `upsert()` or `log()`
- **User asks question**: `overview()` → `get()` full details → Answer
- **Plans change**: Update immediately when agreed with `upsert()`
