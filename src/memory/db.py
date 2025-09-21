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

# Create engine with psycopg3
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
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

SessionLocal = sessionmaker(bind=engine)