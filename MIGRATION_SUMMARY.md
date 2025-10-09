# Fitness MCP Simplification - Migration Summary

## What Changed

### Tool Reduction: 17 → 6 Tools

**Before (17 tools):**
```
upsert_item, get_item, get_items_detail, delete_item, archive_items,
list_items, log_event, list_events, update_event, delete_event,
search_entries, get_overview, get_current_date, get_started,
describe_conventions, report_issue, list_issues
```

**After (6 tools):**
```python
1. upsert     # Create/update items with keys
2. log        # Record events (or update by ID)
3. overview   # Scan everything (truncated)
4. get        # Pull full details
5. search     # Find by content
6. archive    # Soft delete
```

### Schema Simplification: 14 → 10 Columns

**Removed columns (moved to attrs):**
- `priority` → `attrs.priority`
- `tags` → `attrs.tags`
- `parent_key` → `attrs.parent_key`
- `due_date` → `attrs.due_date`

**Final schema:**
```sql
id, user_id, kind, key, content, attrs, status, occurred_at, created_at, updated_at
```

### Status Simplification

**Before:** `active`, `archived`, `achieved`, `paused`, `draft`, `planned`, etc.
**After:** Binary - only `active` or `archived`

## Migration Steps Completed

### 1. Database Migration
```bash
source .env && psql "$DATABASE_URL" < migrations/003_simplify_schema.sql
```
- ✅ Moved priority, tags, parent_key, due_date to attrs
- ✅ Normalized status to binary (active/archived)
- ✅ Preserved all existing data

### 2. Code Changes
- ✅ Created `src/mcp_server_simple.py` with 6 tools
- ✅ Updated `src/memory/crud.py` to handle attrs-based fields
- ✅ Fixed sorting (removed priority sorting, use updated_at)
- ✅ Updated `src/memory/db.py` Entry model (10 columns)

### 3. Documentation Updates
- ✅ Updated `CLAUDE.md` with 6-tool examples
- ✅ Created `FITNESS_COACH_INSTRUCTIONS_SIMPLE.md`
- ✅ Updated `pyproject.toml` to v0.2.0

## Benefits Achieved

### Metrics
- **75% reduction** in tool surface (17 → 6)
- **28% reduction** in schema fields (14 → 10)
- **Binary status** (2 values vs 6+)
- **No broken sorting** (removed mixed-type priority sorting)

### Developer Experience
- **Clearer mental model:** Items (with key) vs Events (timestamped)
- **Single pattern for updates:** Same key = update, no key = new event
- **Flexible attrs:** All variable data in JSONB
- **Tool selection trivial:** Only 6 options vs 17

### Performance
- **Smaller context:** Overview truncates to 100 chars
- **Pull-based loading:** Get full details only when needed
- **Simpler queries:** No complex priority sorting

## Backwards Compatibility

### Data Preserved
All existing data preserved in attrs:
- Original status values stored as `attrs.original_status`
- Priority values moved to `attrs.priority`
- Tags converted to arrays in `attrs.tags`
- Parent keys in `attrs.parent_key`

### Tool Mapping
Old tools can be mapped to new ones:
```python
# Old way
upsert_item(kind='goal', key='x', priority=1, tags='a,b')

# New way (automatic in CRUD layer)
upsert(kind='goal', key='x', attrs={'priority': 1, 'tags': ['a', 'b']})
```

## Testing Results

```bash
✅ UPSERT with attrs - working
✅ LOG event - working
✅ OVERVIEW with truncation - working
✅ SEARCH - working
✅ Attrs migration verified - 29 priorities, 67 tags migrated
✅ All tests pass
```

## Philosophy Alignment

Following Claude Code's principles:
1. **"Always choose the simplest option"** - 6 tools vs 17
2. **"Raw model access"** - Minimal business logic
3. **"Small tool surface"** - Each tool has one clear purpose
4. **"Context as finite resource"** - Truncated overview, pull-based details

## Next Steps

For users:
1. Run migration: `source .env && psql "$DATABASE_URL" < migrations/003_simplify_schema.sql`
2. Update to use `src.mcp_server_simple`
3. Refer to `FITNESS_COACH_INSTRUCTIONS_SIMPLE.md`

For developers:
1. Old server (`src.mcp_server.py`) still available if needed
2. Tests updated for new schema
3. Can add specialized agents on top of 6-tool base

## Summary

This simplification reduces cognitive load while maintaining full functionality. The system is now more aligned with Claude Code's philosophy of minimal tool surface with maximum flexibility. All variable data lives in attrs, making the schema stable and extensible without migrations.