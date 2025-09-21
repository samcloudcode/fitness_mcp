-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create memories table
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    topic VARCHAR(255),
    embedding TEXT, -- Reserved for pgvector
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,

    -- Generated column for FTS
    fts TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', content || ' ' || COALESCE(topic, ''))
    ) STORED
);

-- Create indexes
CREATE INDEX idx_memories_user_id ON memories(user_id);
CREATE INDEX idx_memories_topic ON memories(topic);
CREATE INDEX idx_memories_fts ON memories USING GIN(fts);
CREATE INDEX idx_memories_created_at ON memories(created_at DESC);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER memories_updated_at
    BEFORE UPDATE ON memories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();