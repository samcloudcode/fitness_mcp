from sqlalchemy import create_engine, Column, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os

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

class Memory(Base):
    __tablename__ = "memories"

    id = Column(UUID, primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    topic = Column(String(255), index=True)
    embedding = Column(Text)  # Reserved for pgvector
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Generated tsvector column for FTS
    __table_args__ = (
        Index('idx_memories_fts',
              func.to_tsvector('english', content),
              postgresql_using='gin'),
    )

# Create session factory with autoflush disabled for better performance
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,  # Disable autoflush for better performance
    expire_on_commit=False  # Don't expire objects after commit
)