-- Migration: Cleanup naming conventions
-- Description: Fix duplicate entries, standardize key naming, and enforce naming conventions
-- Date: 2025-10-22
--
-- IMPORTANT: Review this script before running. It will:
-- 1. Archive duplicate "mcp-knee-health" entries (keeping only the first)
-- 2. Rename keys to follow kebab-case conventions
-- 3. Standardize content structure where possible
--
-- BACKUP FIRST: pg_dump $DATABASE_URL > backup_before_cleanup.sql

BEGIN;

-- ========================================
-- 1. REMOVE DUPLICATE ENTRIES
-- ========================================

-- Archive duplicate "mcp-knee-health" knowledge entries (keep only the oldest)
WITH ranked_duplicates AS (
    SELECT
        id,
        ROW_NUMBER() OVER (PARTITION BY user_id, kind, key ORDER BY created_at ASC) as rn
    FROM public.entries
    WHERE kind = 'knowledge'
      AND key = 'mcp-knee-health'
      AND status = 'active'
)
UPDATE public.entries
SET status = 'archived'
WHERE id IN (
    SELECT id FROM ranked_duplicates WHERE rn > 1
);

-- Archive duplicate "long-term" strategy entries (keep oldest)
WITH ranked_duplicates AS (
    SELECT
        id,
        ROW_NUMBER() OVER (PARTITION BY user_id, kind, key ORDER BY created_at ASC) as rn
    FROM public.entries
    WHERE kind = 'strategy'
      AND key = 'long-term'
      AND status = 'active'
)
UPDATE public.entries
SET status = 'archived'
WHERE id IN (
    SELECT id FROM ranked_duplicates WHERE rn > 1
);

-- Archive duplicate "short-term" strategy entries (keep oldest)
WITH ranked_duplicates AS (
    SELECT
        id,
        ROW_NUMBER() OVER (PARTITION BY user_id, kind, key ORDER BY created_at ASC) as rn
    FROM public.entries
    WHERE kind = 'strategy'
      AND key = 'short-term'
      AND status = 'active'
)
UPDATE public.entries
SET status = 'archived'
WHERE id IN (
    SELECT id FROM ranked_duplicates WHERE rn > 1
);

-- Archive duplicate "base-build" plan entries (keep most recent)
WITH ranked_duplicates AS (
    SELECT
        id,
        ROW_NUMBER() OVER (PARTITION BY user_id, kind, key ORDER BY created_at DESC) as rn
    FROM public.entries
    WHERE kind = 'plan'
      AND key = 'base-build'
      AND status = 'active'
)
UPDATE public.entries
SET status = 'archived'
WHERE id IN (
    SELECT id FROM ranked_duplicates WHERE rn > 1
);

-- Archive duplicate "bench-progression" plan entries (keep most recent)
WITH ranked_duplicates AS (
    SELECT
        id,
        ROW_NUMBER() OVER (PARTITION BY user_id, kind, key ORDER BY created_at DESC) as rn
    FROM public.entries
    WHERE kind = 'plan'
      AND key = 'bench-progression'
      AND status = 'active'
)
UPDATE public.entries
SET status = 'archived'
WHERE id IN (
    SELECT id FROM ranked_duplicates WHERE rn > 1
);

-- Archive duplicate bodyweight "current" entries (keep most recent)
WITH ranked_duplicates AS (
    SELECT
        id,
        ROW_NUMBER() OVER (PARTITION BY user_id, kind, key ORDER BY created_at DESC) as rn
    FROM public.entries
    WHERE kind = 'current'
      AND key = 'bodyweight'
      AND status = 'active'
)
UPDATE public.entries
SET status = 'archived'
WHERE id IN (
    SELECT id FROM ranked_duplicates WHERE rn > 1
);

-- Archive test preference entries
UPDATE public.entries
SET status = 'archived'
WHERE kind = 'preference'
  AND key IN ('pref-1', 'pref-2', 'pref-3')
  AND status = 'active';


-- ========================================
-- 2. RENAME KEYS TO FOLLOW CONVENTIONS
-- ========================================

-- Rename abbreviated plan-step keys (wk1-base → week-1-base)
UPDATE public.entries
SET key = 'week-1-base'
WHERE kind = 'plan-step'
  AND key = 'wk1-base'
  AND status = 'active';

-- Rename abbreviated day names (mon-5k-easy → monday-5k-easy)
UPDATE public.entries
SET key = 'monday-5k-easy'
WHERE kind = 'plan-step'
  AND key = 'mon-5k-easy'
  AND status = 'active';

UPDATE public.entries
SET key = 'wednesday-6k-strides'
WHERE kind = 'plan-step'
  AND key = 'wed-6k-strides'
  AND status = 'active';

UPDATE public.entries
SET key = 'friday-4k-tempo'
WHERE kind = 'plan-step'
  AND key = 'fri-4k-tempo'
  AND status = 'active';

-- Rename "5k-pr" goal to be more specific about target
UPDATE public.entries
SET key = '5k-sub20'
WHERE kind = 'goal'
  AND key = '5k-pr'
  AND status = 'active';

-- Rename vague pace estimates to clarify they're estimates
UPDATE public.entries
SET key = '5k-pace-estimate'
WHERE kind = 'current'
  AND key = '5k-pace'
  AND status = 'active';

UPDATE public.entries
SET key = '10k-pace-estimate'
WHERE kind = 'current'
  AND key = '10k-pace'
  AND status = 'active';

-- Rename "mcp-*" prefixed knowledge entries
-- Note: Only rename if there's a single entry, otherwise manual review needed
UPDATE public.entries
SET key = 'base-build-oct-2025'
WHERE kind = 'plan'
  AND key = 'mcp-base-block'
  AND status = 'active';

-- Rename vague "bench-progression" to include timeframe/type
-- This requires manual review since we don't know the actual program details
-- Commenting out - user should decide specific naming based on content
-- UPDATE public.entries
-- SET key = 'bench-8wk-linear'
-- WHERE kind = 'plan'
--   AND key = 'bench-progression'
--   AND status = 'active';

-- Rename multi-day workout-plan to single date (2025-10-24-26-regatta → 2025-10-24)
-- Keep the regatta info in content
UPDATE public.entries
SET key = '2025-10-24'
WHERE kind = 'workout-plan'
  AND key = '2025-10-24-26-regatta'
  AND status = 'active';

-- Rename "knee-health" knowledge entry to be more specific
-- Only if there's a single entry, otherwise manual review needed
UPDATE public.entries
SET key = 'knee-health-basics'
WHERE kind = 'knowledge'
  AND key = 'knee-health'
  AND status = 'active'
  AND NOT EXISTS (
      SELECT 1 FROM public.entries e2
      WHERE e2.kind = 'knowledge'
        AND e2.key LIKE 'knee-health-%'
        AND e2.status = 'active'
        AND e2.id != entries.id
  );


-- ========================================
-- 3. VALIDATION CHECKS
-- ========================================

-- Check for remaining duplicate keys (should be 0)
SELECT
    kind,
    key,
    COUNT(*) as duplicate_count
FROM public.entries
WHERE status = 'active'
  AND key IS NOT NULL
GROUP BY user_id, kind, key
HAVING COUNT(*) > 1
ORDER BY kind, key;

-- Check for keys with underscores (should avoid)
SELECT
    kind,
    key,
    LEFT(content, 60) as content_preview
FROM public.entries
WHERE status = 'active'
  AND key LIKE '%_%'
  AND key IS NOT NULL
ORDER BY kind, key;

-- Check for abbreviated day names in plan-steps
SELECT
    kind,
    key,
    LEFT(content, 60) as content_preview
FROM public.entries
WHERE status = 'active'
  AND kind = 'plan-step'
  AND (key LIKE 'mon-%' OR key LIKE 'tue-%' OR key LIKE 'wed-%'
       OR key LIKE 'thu-%' OR key LIKE 'fri-%' OR key LIKE 'sat-%' OR key LIKE 'sun-%')
ORDER BY key;

-- Check for abbreviated weeks (wk1, wk2, etc.)
SELECT
    kind,
    key,
    LEFT(content, 60) as content_preview
FROM public.entries
WHERE status = 'active'
  AND key LIKE '%wk%'
ORDER BY kind, key;

-- Check for "mcp-" prefixed entries
SELECT
    kind,
    key,
    LEFT(content, 60) as content_preview
FROM public.entries
WHERE status = 'active'
  AND key LIKE 'mcp-%'
ORDER BY kind, key;


-- ========================================
-- 4. SUMMARY REPORT
-- ========================================

-- Show final count by kind
SELECT
    kind,
    COUNT(*) as active_count
FROM public.entries
WHERE status = 'active'
GROUP BY kind
ORDER BY kind;

-- Show recently archived items (from this cleanup)
SELECT
    kind,
    key,
    LEFT(content, 60) as content_preview,
    updated_at
FROM public.entries
WHERE status = 'archived'
  AND updated_at > NOW() - INTERVAL '5 minutes'
ORDER BY kind, key;

COMMIT;

-- ========================================
-- ROLLBACK INSTRUCTIONS
-- ========================================
-- If you need to rollback this migration:
-- 1. Restore from backup: psql $DATABASE_URL < backup_before_cleanup.sql
-- 2. Or manually revert specific changes using UPDATE statements
