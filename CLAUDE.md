# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simplified fitness tracking MCP server following Claude Code's philosophy: **minimal tool surface (6 tools), maximum flexibility**. Built with FastMCP and PostgreSQL, using a unified entry-based architecture where all variable data lives in JSONB attrs.

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

**Simplified Schema** (10 columns, down from 14):
- Removed: `priority`, `tags`, `parent_key`, `due_date` (all moved to attrs)
- Binary status: Only `active` or `archived`
- Everything variable goes in `attrs` JSONB field

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
upsert(kind='goal', key='bench-225', content='Bench 225lbs x5')

# 2. LOG - Timestamped events
log(kind='workout', content='Squats 3x5 @ 225lbs', occurred_at='2025-01-15T10:00:00Z')

# 3. OVERVIEW - Scan everything (truncated)
overview()  # Returns all active items with truncated verbose content

# 4. GET - Pull full details
get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])  # Specific items
get(kind='workout', start='2025-01-01', limit=10)  # Filtered list

# 5. SEARCH - Find by content
search('knee pain', kind='knowledge')

# 6. ARCHIVE - Soft delete
archive(kind='goal', key='old-goal')  # Specific item
archive(kind='preference')  # Bulk archive all active preferences
```

### Common Workflows

**Goal Tracking:**
```python
# Create goal with progress tracking
upsert(kind='goal', key='bench-225', content='Bench 225lbs x5',
       attrs={'baseline': {'value': '185lbs', 'date': '2025-09-01'},
              'target': {'value': '225lbs', 'date': '2026-03-01'}})

# Log progress
log(kind='workout', content='Bench 3x5 @ 205lbs')

# Check status
overview()  # See all goals with progress
```

**Knowledge Management:**
```python
# Store knowledge
upsert(kind='knowledge', key='knee-health',
       content='Keep knees tracking over toes...',
       attrs={'tags': ['injury-prevention', 'squat']})

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

**Overview Truncation Pattern** (NEW): `get_overview()` returns ALL active items but truncates verbose content to 100 chars (knowledge, principles, preferences, plan-steps, workouts). This enables efficient context scanning without loading full textbook entries. Use `get_items_detail([{"kind": "knowledge", "key": "knee-health"}])` to fetch complete content for specific items. Goals/plans/current show full content (should be concise).

**Pull-Based Context Composition**: LLMs should scan truncated overview, then pull full details only for relevant items using `get_items_detail()`, `search_entries()`, or `list_items()`. Multiple small queries >> one giant dump.

**Attribute Handling**: `attrs` is JSONB accepting any valid JSON structure (arrays, nested objects). Standards defined in `describe_conventions()`:
- Goals: `{baseline: {value, date}, target: {value, date}}` (enables progress tracking)
- Plans: `{start_date: 'YYYY-MM-DD', duration_weeks: number}` (enables temporal context)
- Workouts: `{exercises: [{name, sets, reps, weight, rpe}], duration_min, rpe}`
- Use attrs for structured data (numbers, arrays), content for narratives

**Content Brevity Guidelines**: Store concise summaries, not textbooks:
- Goals: 10-20 words ("Bench 225lbs x5")
- Knowledge: 200-400 words, user-specific observations only (not general science LLMs already know)
- Principles: 150-300 words, reminders not full protocols
- See [FITNESS_COACH_INSTRUCTIONS.md](FITNESS_COACH_INSTRUCTIONS.md) for detailed guidelines

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

**Critical Patterns (NEW - Pull-Based Context)**:
- Always call `get_overview()` at session start - returns ALL items with truncated content (100 chars)
- Scan overview to see what exists (keys visible, content truncated for verbose kinds)
- Pull full details on-demand: `get_items_detail([{"kind": "knowledge", "key": "knee-health"}])`
- Or search for specifics: `search_entries(query='knee pain', kind='knowledge', limit=3)`
- Use `upsert_item()` for durable data (never duplicate same key)
- Use `log_event()` for timestamped events (creates new each time)
- Archive items (`status='archived'`) instead of deleting (preserves history)

**Context Composition Patterns** (see [FITNESS_COACH_INSTRUCTIONS.md](FITNESS_COACH_INSTRUCTIONS.md#context-composition-patterns)):
- **Workout Planning**: Overview → see active plans → pull plan steps if needed
- **Injury Query**: Overview → scan truncated knowledge → pull relevant items or search
- **Goal Review**: Overview → goals show full content (already concise)
- **Preferences**: Overview → truncated → pull only if relevant to current task

**Content Brevity**:
- Goals: 10-20 words max ("Bench 225lbs x5")
- Knowledge: 200-400 words, user-specific observations only
- Principles: 150-300 words, reminders not full protocols
- Store what LLM doesn't know, not textbook content

**Attrs Standards** (see `describe_conventions()` tool):
- Goals: `{baseline: {value, date}, target: {value, date}}`
- Plans: `{start_date, duration_weeks}` (enables temporal context)
- Workouts: `{exercises: [{name, sets, reps, weight, rpe}], duration_min, rpe}`
- Use attrs for structured data (numbers, arrays), content for narratives

**Common Mistakes to Avoid**:
- Using backticks for strings (use `'goal'` not `` `goal` ``)
- Stringifying attrs (`attrs='{"key": "value"}'` instead of `attrs={'key': 'value'}`)
- Creating duplicate items instead of updating existing ones
- Storing textbook knowledge instead of user-specific observations
- Pulling all knowledge every session (use truncated overview + selective pulls)

**Tool Selection**:
- `get_overview()`: Lightweight scan of all data (truncated content)
- `get_items_detail()`: Fetch full content for specific items by keys
- `search_entries()`: Find entries by content when key unknown
- `list_items()`: Targeted queries by kind/status/tags
- `upsert_item()`: Goals, plans, preferences, knowledge (anything with memorable key)
- `log_event()`: Workouts, metrics, notes (timestamped occurrences)
- `update_event()`: Fix logged events after the fact
- `archive_items()`: Bulk archiving by kind/status/tags
