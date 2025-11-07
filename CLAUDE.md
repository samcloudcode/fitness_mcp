# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository combines two complementary components:

1. **MCP Server** - A simplified fitness tracking server following Claude Code's philosophy: **minimal tool surface (4 tools), maximum flexibility**. Built with FastMCP and PostgreSQL, using a unified entry-based architecture where all data goes in the content field as natural text.

2. **Anthropic Skills Folder** - A collection of Claude Code skills (in `.claude/skills/`) that provide structured fitness coaching instructions. These skills can be exported and reused in other repositories or shared with other users.

### 🎯 4 Core Tools (Down from 17)

1. **`upsert`** - Create/update ALL entries (use key for items, empty key for metrics/notes)
2. **`overview`** - Lightweight scan of all data (truncated)
3. **`get`** - Pull full details by keys or filters
4. **`archive`** - Soft delete (set status='archived')

### Core Concepts

**Two Data Patterns**:
- **Items** (has `key`): Durable things you update - goals, program, week, plan, knowledge, preference, log (workout logs). Same key = replace.
- **Events** (no `key`): Timestamped occurrences - metrics, notes. Always creates new (use empty key '').

**Simplified Schema** (9 columns, down from 14):
- Removed: `priority`, `tags`, `parent_key`, `due_date`, `attrs` (everything goes in content now)
- Binary status: Only `active` or `archived` (enforced via check constraint)
- Everything goes in content field as natural text
- **Overview excludes archived entries** for clean working context

**Everything in Content**: All data goes in the content field as natural text. Want to track plan progress? Put "Week 3 of 8" in content. Want tags? Put "Tags: injury-prevention, squat" in content. Simple and searchable.

**Observability**: Integrated Logfire instrumentation for SQLAlchemy operations, configurable via environment variables (`LOGFIRE_SEND_TO_LOGFIRE`, `ENVIRONMENT`).

**Naming Conventions**: Strict key naming and content structure rules ensure data consistency. See [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md) for complete reference.

### Skills Structure

The `.claude/skills/` folder contains exportable skill modules that provide fitness coaching capabilities:

- **`fitness-coach-essentials/`** - Core coaching logic and MCP tool usage patterns
- **`fitness-coach-programming/`** - Workout programming and exercise science knowledge
- **`fitness-coach-interaction/`** - User interaction patterns and conversational guidelines

**Exporting Skills**: These skills can be copied to other repositories or shared with users who want fitness coaching capabilities in their own Claude Code environments. Each skill is self-contained with its own `skill.md` instruction file.

**Using Skills**: Skills are automatically loaded when working in this repository. They provide context-aware guidance to Claude Code for fitness coaching tasks.

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
# Start the simplified MCP server (4 tools)
uv run python -m src.mcp_server

# Or use the script entry point
uv run memory-server

# Test server responds (4 second timeout)
timeout 5s uv run python -m src.mcp_server
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

# View recent logs (events have NULL key)
source .env && psql "$DATABASE_URL" -c "SELECT occurred_at, LEFT(content, 80) FROM public.entries WHERE kind = 'log' AND status = 'active' ORDER BY occurred_at DESC LIMIT 10;"

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

### Quick Start - The 4 Tools

```python
# 1. UPSERT - Create/update ALL entries
# Items with keys (goals, logs, knowledge, etc):
upsert(kind='goal', key='bench-225',
       content='Bench 225x5 by March (currently 185x5). Priority: High. Why: Foundation for rugby performance.')

# Workout logs with date keys:
upsert(kind='log', key='2025-10-29-lower', content='Lower: Squats 5x5 @ 225lbs RPE 7, RDL 3x8 @ 185')

# Metrics/notes (empty key = no key):
upsert(kind='metric', key='', content='Weight: 71kg')
upsert(kind='note', key='', content='Knee felt tight during warmup')

# 2. OVERVIEW - Context-aware scanning (truncated to 200 words)
overview()  # All active items (default)
overview(context='planning')  # Planning mode: goals, program, week, plan, preferences, knowledge, logs (2 weeks)
overview(context='upcoming')  # Upcoming mode: goals, week, plan, logs (1 week)
overview(context='knowledge')  # Knowledge mode: goals, program, preferences, knowledge
overview(context='history')  # History mode: goals, all logs, all metrics (progress review)

# 3. GET - Pull full details
get(items=[{'kind': 'knowledge', 'key': 'knee-health-alignment'}])  # Specific items
get(kind='log', limit=14)  # Last 2 weeks of logs (safety first!)

# 4. ARCHIVE - Soft delete
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

# 4. PLAN - Today's planned workout
upsert(
    kind='plan',
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

# Log workout progress (use upsert with date key for workout logs)
upsert(kind='log', key='2025-10-29-upper', content='Bench 3x5 @ 205lbs RPE 7')

# Check status
overview()  # See all goals and context
overview(context='planning')  # See everything needed for planning workouts
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
get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])  # When you know the key
```

## Architecture

### Key Design Patterns

**UPSERT Pattern**: All durable items use PostgreSQL's `ON CONFLICT DO UPDATE` via `(user_id, kind, key)` unique constraint. This ensures:
- Same key = update existing item (don't duplicate)
- New key = insert new item
- Atomic operations with automatic `updated_at` timestamp

**Event Immutability**: Events (metrics, notes) have no `key` and are identified by UUID. Workout logs should use `upsert()` with date-based keys for the one-log-per-workout pattern.

**Full-Text Search**: PostgreSQL FTS using generated tsvector column on `(key + content)` with GIN index. Searches use `plainto_tsquery` for user-friendly query parsing.

**Connection Pooling**: Optimized for Supabase pooler:
- Small local pool (pool_size=2, max_overflow=3) since Supabase handles pooling
- TCP keepalives configured for connection stability
- 30-second statement timeout
- No pool recycling (Supabase manages connection lifecycle)

### Core Components

**MCP Server** ([src/mcp_server.py](src/mcp_server.py)):
- 4 FastMCP tools for fitness tracking: `upsert`, `overview`, `get`, `archive`
- Context managers (`get_session()`) for database session lifecycle
- User ID resolution from environment variables (`FITNESS_USER_ID` or `DEFAULT_USER_ID`)
- Date/datetime parsing with ISO 8601 format handling
- Logfire instrumentation with auto-tracing for CRUD operations

**CRUD Operations** ([src/memory/crud.py](src/memory/crud.py)):
- `upsert_item()`: PostgreSQL upsert for durable items using `ON CONFLICT`
- `log_event()`: Insert events without keys (creates new entry each time)
- `update_event()` / `delete_event()`: Event modifications by UUID
- `get_overview()`: Returns context-filtered items with truncated content (200 words) for efficient scanning
  - `planning` context: goals, program, week, plan (recent 5), preference, knowledge, log (recent 10)
  - `upcoming` context: goals, week, plan (recent 5), log (recent 7)
  - `knowledge` context: goals, program, preference, knowledge
  - `history` context: goals, log (all), metric (all)
- `get_items_by_keys()`: Fetch full content for specific items by (kind, key) tuples
- `list_items()` / `list_events()`: Fetch filtered lists of items or events
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
FastMCP Tool (4 tools in src/mcp_server.py)
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

**Overview Truncation Pattern**: `get_overview()` returns context-filtered active items and truncates verbose content to 200 words (knowledge, preferences, logs, program). This enables efficient context scanning without loading full entries. Use `get()` to fetch complete content for specific items. Goals/week/plan show full content (should be concise). Use context parameter to filter relevant data: 'planning' for comprehensive workout planning, 'upcoming' for near-term focus, 'knowledge' for constraints and preferences.

**Pull-Based Context Composition**: LLMs should scan truncated overview, then pull full details only for relevant items using `get()`. Multiple small queries >> one giant dump.

**Content Brevity Guidelines**: Store concise but complete entries with "why" context:
- Goals: 100-200 chars with current state, priority, deadline, and rationale
- Program: 400-600 chars explaining long-term vision, current focus, weekly structure
- Week: 200-400 chars with daily schedule and adjustments
- Plan: 200-400 chars with exercises and rationale for specific workout
- Knowledge: 200-400 chars typical, 600 max - user-specific observations only (not general science LLMs already know)
- Preference: 200-400 chars for equipment, style, timing, recovery
- Logs: As much detail as provided - one log per workout session
- Metric: 50-200 chars for point-in-time measurements
- See [FITNESS_COACH_INSTRUCTIONS_SIMPLE.md](FITNESS_COACH_INSTRUCTIONS_SIMPLE.md) for detailed guidelines

**Status Values**: Enforced binary constraint - only `active` or `archived` allowed. Overview **excludes** `archived` items for clean working context.

**Timestamp Handling**:
- `occurred_at`: For events (logs, metrics, notes) - when the event happened
- `created_at` / `updated_at`: Automatic timestamps for all entries
- Due dates, deadlines: Put directly in content ("Due: 2025-12-31")

**Relationships**: Express in content as natural text:
- "Part of squat-progression program"
- "Week 3 of 8-week cycle"
- "Relates to knee-health knowledge entry"

**Kind Values**: Clean 9-kind architecture:
- **Items (with keys)**: `goal`, `program`, `week`, `plan`, `knowledge`, `preference`, `log` (workout logs)
  - Same key = update existing (upsert pattern)
  - Goals include current state, priority, deadline, why
  - Program is single `current-program` entry with long-term vision + current focus
  - Week/plan are dated (`2025-week-43`, `2025-10-28-upper`)
  - Knowledge is user-specific observations only (no general principles)
  - Preference for equipment, style, timing, recovery
  - **Logs with date keys** (`2025-10-29-upper`) for one-log-per-workout pattern
- **Events (no keys, UUID only)**: `metric`, `note`
  - Always creates new entry (immutable timeline)
  - Metrics are point-in-time measurements
  - Notes are timestamped observations

No enforced enum - new kinds can be added without schema changes, but stick to these 9 for simplicity.

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
- **Two-Phase Rule**: Propose plans first, save ONLY after user approval
  - Exception: User provides completed info ("I just did squats") → log immediately
- Always call `overview()` with appropriate context at session start:
  - `overview(context='planning')` for workout planning (comprehensive)
  - `overview(context='upcoming')` for near-term focus
  - `overview(context='knowledge')` for constraints/preferences
  - `overview(context='history')` for progress review (all logs/metrics)
  - `overview()` for everything (default)
- Verbose content truncated to 200 words - use `get()` to pull full details
- Use `upsert()` for ALL data (same key = update for items, empty key for events)
- Archive items instead of deleting (preserves history)

**Data Fetching Rules (Safety First)**:
- **Before programming workouts**: ALWAYS fetch ALL knowledge (injuries/limitations)
- **Recent training context**: Fetch 2 weeks of logs (`limit=14`, usually 6-12 sessions)
- **Active program**: Review program to understand current training phase
- Better to over-fetch safety info than miss critical limitations

**Content Guidelines & "Everything in Content" Principle**:
- Goals: 100-200 chars with current state, priority, deadline, why
- Knowledge: 200-400 chars typical, 600 max - user-specific observations only
- Program: 400-600 chars with long-term vision, current focus, weekly structure
- Week: 200-400 chars with daily schedule and adjustments
- Plan: 200-400 chars with exercises and rationale
- Logs: As much detail as provided - one log per workout session
- **Put everything in content field** - no attrs needed

**Common Mistakes to Avoid**:
- **Saving before approval**: Propose plans first, save ONLY after user agrees
- Creating duplicate items instead of updating existing ones (same key = update)
- Storing textbook knowledge instead of user-specific observations (200-400 chars)
- Missing safety checks: ALWAYS fetch all knowledge before programming workouts

**Workflow Examples**:
- **User wants workout**: `overview(context='planning')` → Review goals, program, week, plan, knowledge (2 weeks logs) → **Propose (don't save)** → Get approval → `upsert()` plan + user does workout → `upsert()` log
- **User asks "what's coming up"**: `overview(context='upcoming')` → See week, plans, recent logs (1 week)
- **User asks about progress**: `overview(context='history')` → See all logs and metrics over time → Analyze trends
- **User provides completed workout**: Log immediately with `upsert(kind='log', key='YYYY-MM-DD-type')`
- **User provides goal/knowledge**: Save immediately with `upsert()`
- **User asks question**: `overview(context='knowledge')` → See constraints, preferences → `get()` full details if needed → Answer
- **Program/week/plan updates**: Update immediately when agreed with `upsert()`
