from sqlalchemy import create_engine, Column, String, Text, DateTime, Index, Integer, UniqueConstraint, Date
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR, JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os
from sqlalchemy import text as sql_text

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Update URL to use psycopg (v3) instead of psycopg2
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

# Optimized for Supabase pooler connection
# Since Supabase already provides connection pooling, we keep a minimal local pool
engine = create_engine(
    DATABASE_URL,
    pool_size=2,  # Small local pool since Supabase handles pooling
    max_overflow=3,  # Allow some overflow for bursts
    pool_pre_ping=False,  # Supabase pooler handles dead connections
    pool_recycle=-1,  # Disable recycling, let Supabase handle it
    echo_pool=False,  # Disable pool debugging
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000",  # 30 second statement timeout
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    } if DATABASE_URL.startswith("postgresql") else {}
)

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entries"

    # Core identity
    id = Column(UUID, primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(String(255), nullable=False, index=True)

    # Type and identity
    kind = Column(String(50), nullable=False, index=True)
    key = Column(String(255), nullable=True, index=True)  # Items have keys, events don't

    # Content and attributes
    content = Column(Text, nullable=False)
    attrs = Column(JSONB, nullable=False, server_default=sql_text("'{}'::jsonb"))  # All variable data goes here

    # Simple binary status
    status = Column(String(50), default='active')  # Only 'active' or 'archived'

    # Timestamps
    occurred_at = Column(DateTime(timezone=True))  # For events
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'kind', 'key', name='uq_entries_user_kind_key'),
        Index(
            'idx_entries_fts',
            func.to_tsvector('english', func.concat(func.coalesce(key, ''), ' ', content)),
            postgresql_using='gin'
        ),
        Index('idx_entries_user_occured_at', 'user_id', 'occurred_at'),
    )

# Create session factory with autoflush disabled for better performance
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,  # Disable autoflush for better performance
    expire_on_commit=False  # Don't expire objects after commit
)
