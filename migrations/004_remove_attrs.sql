-- Migration 004: Remove attrs column - pure simplicity
-- All data goes in content as natural text. No more JSONB complexity.

BEGIN;

-- Drop the attrs column
ALTER TABLE entries DROP COLUMN attrs;

COMMIT;

-- Final schema: 9 columns
-- id, user_id, kind, key, content, status, occurred_at, created_at, updated_at
-- Everything variable goes in content as plain text
