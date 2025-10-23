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

**Naming Conventions**: Strict key naming and content structure rules ensure data consistency. See [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md) for complete reference.

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
source .env && psql "$DATABASE_URL" < migrations/003_simplify_schema.sql  # Simplifies to 9 columns

# Optional: Clean up naming conventions and duplicates
source .env && psql "$DATABASE_URL" < migrations/004_cleanup_naming_conventions.sql

# Check database connection
uv run python -c "from src.memory.db import engine; from sqlalchemy import text; engine.connect().execute(text('SELECT 1'))"

# Check schema
source .env && psql "$DATABASE_URL" -c "SELECT column_name, data_type FROM information_schema.columns WHERE schemaname = 'public' AND table_name = 'entries';"
```

### Database Querying with psql

**IMPORTANT:** The database uses Supabase which requires explicit schema qualification. Always use `public.entries` instead of just `entries`.

```bash
# Count all active entries
source .env && psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM public.entries WHERE status = 'active';"

# View all active entries by kind
source .env && psql "$DATABASE_URL" -c "SELECT kind, COUNT(*) as count FROM public.entries WHERE status = 'active' GROUP BY kind ORDER BY kind;"

# Check for duplicate keys (should be 0)
source .env && psql "$DATABASE_URL" -c "SELECT kind, key, COUNT(*) FROM public.entries WHERE status = 'active' AND key IS NOT NULL GROUP BY kind, key HAVING COUNT(*) > 1;"

# View recent workouts (events have NULL key)
source .env && psql "$DATABASE_URL" -c "SELECT occurred_at, LEFT(content, 80) FROM public.entries WHERE kind = 'workout' AND status = 'active' ORDER BY occurred_at DESC LIMIT 10;"

# Backup data to CSV
source .env && psql "$DATABASE_URL" -c "\copy (SELECT * FROM public.entries) TO 'backup_$(date +%Y%m%d_%H%M%S).csv' CSV HEADER"

# Delete test data (keep only user_id = '1')
source .env && psql "$DATABASE_URL" -c "DELETE FROM public.entries WHERE user_id <> '1';"

# List all unique users
source .env && psql "$DATABASE_URL" -c "SELECT DISTINCT user_id FROM public.entries ORDER BY user_id;"
```

**Common Gotchas:**
- ❌ `FROM entries` → Use `FROM public.entries` (schema required)
- ❌ `WHERE user_id != '1'` → Use `WHERE user_id <> '1'` (avoid `!` in psql)
- ❌ `table_name = 'entries'` → Use `schemaname = 'public' AND table_name = 'entries'`

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
# Put EVERYTHING in content field - include "why" context!
upsert(kind='goal', key='bench-225',
       content='Bench 225x5 by March (currently 185x5). Priority: High. Why: Foundation for rugby performance.')

# 2. LOG - Timestamped events
# Full workout details in content, one line
log(kind='workout', content='Lower: Squats 5x5 @ 225lbs RPE 7, RDL 3x8 @ 185')

# 3. OVERVIEW - Scan everything (truncated)
overview()  # Returns all ACTIVE items (archived excluded), verbose content truncated to 100 chars

# 4. GET - Pull full details
get(items=[{'kind': 'knowledge', 'key': 'knee-health-alignment'}])  # Specific items
get(kind='workout', limit=14)  # Last 2 weeks of workouts (safety first!)

# 5. SEARCH - Find by content
search('knee pain', kind='knowledge')

# 6. ARCHIVE - Soft delete
archive(kind='goal', key='old-goal')  # Specific item
archive(kind='preference')  # Bulk archive all active preferences
```

### Planning Hierarchy (4 Levels)

**Everything in content with "why" context:**

```python
# 1. GOALS - Target states with priorities
upsert(
    kind='goal',
    key='bench-225',
    content='Bench 225x5 by June (currently 185x5). Priority: High. Why: Foundation for rugby - need upper body strength for scrums.'
)

# 2. PROGRAM - Overall strategy (single living document)
upsert(
    kind='program',
    key='current-program',
    content='Oct-Dec: Strength primary 4x/week (bench-225, squat-315), running secondary 3x/week (20-25mpw). Why: Rugby season April needs strength peak. Daily hip mobility - consistency > intensity for mobility gains.'
)

# 3. WEEK - This week's schedule
upsert(
    kind='week',
    key='2025-week-43',
    content='Mon: Upper. Tue: Easy run. Wed: Lower. Thu: OFF (travel). Fri: Tempo. Sat: Full body. Sun: Long run. Why: Travel Thu means 6 sessions not 7, compensate Sat volume.'
)

# 4. SESSION - Today's planned workout
upsert(
    kind='session',
    key='2025-10-22-strength',
    content='6am Upper: Bench 4x10 @ 185 (volume for bench-225), OHP 3x12 @ 115 (shoulder health), rows 3x12. Why: Hypertrophy phase. OHP light due to shoulder tweak.'
)
```

Natural language, fully searchable, no structured data complexity.

### Common Workflows

**Goal Tracking:**
```python
# Create goal with priority and rationale
upsert(
    kind='goal',
    key='bench-225',
    content='Bench 225x5 by March (currently 185x5). Priority: High. Why: Strength foundation for sport performance.'
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

**Overview Truncation Pattern**: `get_overview()` returns ALL active items but truncates verbose content to 100 chars (knowledge, principles, preferences, workouts). This enables efficient context scanning without loading full entries. Use `get()` to fetch complete content for specific items. Goals/program/week/session/current show full content (should be concise).

**Pull-Based Context Composition**: LLMs should scan truncated overview, then pull full details only for relevant items using `get()` or `search()`. Multiple small queries >> one giant dump.

**Content Brevity Guidelines**: Store concise summaries with "why" context:
- Goals: 20-50 words with priority and rationale ("Bench 225x5 by June. Priority: High. Why: Rugby performance.")
- Program: 80-150 words explaining strategy across all goals
- Week: 50-100 words with daily schedule and adjustments
- Session: 40-80 words with exercises and rationale
- Knowledge: 30-60 words, user-specific observations only (not general science LLMs already know)
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

**Kind Values**: No enforced enum - core kinds are:
- **With keys (items)**: `goal`, `program`, `week`, `session`, `knowledge`, `preference`, `principle`, `current`, `strategy`
- **Without keys (events)**: `workout`, `metric`, `note`
- **Deprecated**: `plan`, `plan-step`, `workout-plan` (replaced by `program`, `week`, `session`)

New kinds can be added without schema changes.

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
- **User wants workout**: `overview()` → `get(kind='knowledge')` → `get(kind='workout', limit=14)` → `get(items=[{'kind': 'program', 'key': 'current-program'}])` → **Propose (don't save)** → Get approval → `log()`
- **User provides info**: Save immediately with `upsert()` or `log()`
- **User asks question**: `overview()` → `get()` full details → Answer
- **Program/week/session updates**: Update immediately when agreed with `upsert()`
