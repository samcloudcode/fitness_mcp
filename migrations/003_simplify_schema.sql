-- Migration 003: Simplify schema - move priority, tags, parent_key, due_date to attrs
-- This reduces schema complexity and follows the "attrs for everything variable" pattern

BEGIN;

-- Step 1: Migrate priority to attrs (if not null)
UPDATE entries
SET attrs = jsonb_set(
    COALESCE(attrs, '{}'::jsonb),
    '{priority}',
    to_jsonb(priority)
)
WHERE priority IS NOT NULL;

-- Step 2: Migrate tags to attrs as array (if not null)
UPDATE entries
SET attrs = jsonb_set(
    COALESCE(attrs, '{}'::jsonb),
    '{tags}',
    CASE
        WHEN tags IS NOT NULL AND tags != ''
        THEN to_jsonb(string_to_array(tags, ','))
        ELSE '[]'::jsonb
    END
)
WHERE tags IS NOT NULL AND tags != '';

-- Step 3: Migrate parent_key to attrs (if not null)
UPDATE entries
SET attrs = jsonb_set(
    COALESCE(attrs, '{}'::jsonb),
    '{parent_key}',
    to_jsonb(parent_key)
)
WHERE parent_key IS NOT NULL;

-- Step 4: Migrate due_date to attrs (if not null)
UPDATE entries
SET attrs = jsonb_set(
    COALESCE(attrs, '{}'::jsonb),
    '{due_date}',
    to_jsonb(due_date::text)
)
WHERE due_date IS NOT NULL;

-- Step 5: Drop the columns we've migrated
ALTER TABLE entries DROP COLUMN priority;
ALTER TABLE entries DROP COLUMN tags;
ALTER TABLE entries DROP COLUMN parent_key;
ALTER TABLE entries DROP COLUMN due_date;

-- Step 6: Drop the index on parent_key since column is gone
DROP INDEX IF EXISTS idx_entries_user_kind_parent;

-- Step 7: Simplify status values to just 'active' and 'archived'
-- Move other statuses to attrs for posterity
UPDATE entries
SET
    attrs = jsonb_set(
        COALESCE(attrs, '{}'::jsonb),
        '{original_status}',
        to_jsonb(status)
    ),
    status = CASE
        WHEN status IN ('archived', 'deleted', 'inactive') THEN 'archived'
        ELSE 'active'
    END
WHERE status NOT IN ('active', 'archived');

-- Step 8: Add check constraint for simplified status
ALTER TABLE entries ADD CONSTRAINT check_status_values
    CHECK (status IN ('active', 'archived') OR status IS NULL);

-- Step 9: Create index on attrs for common queries (optional, can add later if needed)
-- CREATE INDEX idx_entries_attrs_priority ON entries ((attrs->>'priority')) WHERE attrs ? 'priority';
-- CREATE INDEX idx_entries_attrs_parent_key ON entries ((attrs->>'parent_key')) WHERE attrs ? 'parent_key';

COMMIT;

-- Verification queries (run these after migration to check)
-- SELECT COUNT(*) FROM entries WHERE attrs ? 'priority';
-- SELECT COUNT(*) FROM entries WHERE attrs ? 'tags';
-- SELECT COUNT(*) FROM entries WHERE attrs ? 'parent_key';
-- SELECT COUNT(*) FROM entries WHERE attrs ? 'due_date';
-- SELECT DISTINCT status FROM entries;