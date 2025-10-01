-- Refresh schema for unified entries-based design
-- Safe to run multiple times

-- Ensure required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Optional: drop legacy table from test phase
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'memories') THEN
        DROP TABLE memories CASCADE;
    END IF;
END $$;

-- Create entries table
CREATE TABLE IF NOT EXISTS entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    kind VARCHAR(50) NOT NULL,
    key VARCHAR(255),
    parent_key VARCHAR(255),
    content TEXT NOT NULL,
    status VARCHAR(50),
    priority SMALLINT,
    tags VARCHAR(255),
    occurred_at TIMESTAMPTZ,
    due_date DATE,
    attrs JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Enforce uniqueness for durable keyed items
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'uq_entries_user_kind_key'
    ) THEN
        ALTER TABLE entries
        ADD CONSTRAINT uq_entries_user_kind_key UNIQUE (user_id, kind, key);
    END IF;
END $$;

-- Generated column for full-text search
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_entries_fts'
    ) THEN
        CREATE INDEX idx_entries_fts ON entries
        USING GIN (to_tsvector('english', coalesce(key,'') || ' ' || content));
    END IF;
END $$;

-- Helpful indexes
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_entries_user_kind'
    ) THEN
        CREATE INDEX idx_entries_user_kind ON entries(user_id, kind);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_entries_user_occured_at'
    ) THEN
        CREATE INDEX idx_entries_user_occured_at ON entries(user_id, occurred_at DESC);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_entries_parent_key'
    ) THEN
        CREATE INDEX idx_entries_parent_key ON entries(user_id, kind, parent_key);
    END IF;
END $$;

-- updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'entries_updated_at'
    ) THEN
        CREATE TRIGGER entries_updated_at
            BEFORE UPDATE ON entries
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at();
    END IF;
END $$;

