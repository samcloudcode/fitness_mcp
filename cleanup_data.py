#!/usr/bin/env python3
"""Clean up fitness data to align with simplified 6-tool architecture."""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.environ.get("DATABASE_URL", "").replace(
    "postgresql://", "postgresql+psycopg://"
)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

USER_ID = os.environ.get("FITNESS_USER_ID") or os.environ.get("DEFAULT_USER_ID")
if not USER_ID:
    raise ValueError("FITNESS_USER_ID or DEFAULT_USER_ID must be set")

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def cleanup_data():
    """Run all cleanup operations."""
    with Session() as session:
        try:
            # 1. Remove tags from attrs (no longer needed in simplified system)
            print("1. Removing tags from attrs...")
            result = session.execute(
                text("""
                    UPDATE entries
                    SET attrs = attrs - 'tags'
                    WHERE user_id = :user_id
                    AND attrs ? 'tags'
                """),
                {"user_id": USER_ID}
            )
            print(f"   Removed tags from {result.rowcount} entries")

            # 2. Remove priority from attrs (moved out of schema)
            print("2. Removing priority from attrs...")
            result = session.execute(
                text("""
                    UPDATE entries
                    SET attrs = attrs - 'priority'
                    WHERE user_id = :user_id
                    AND attrs ? 'priority'
                """),
                {"user_id": USER_ID}
            )
            print(f"   Removed priority from {result.rowcount} entries")

            # 3. Set NULL status to 'active' (binary status system)
            print("3. Setting NULL status to 'active'...")
            result = session.execute(
                text("""
                    UPDATE entries
                    SET status = 'active'
                    WHERE user_id = :user_id
                    AND (status IS NULL OR status = '')
                """),
                {"user_id": USER_ID}
            )
            print(f"   Updated status for {result.rowcount} entries")

            # 4. Delete test workout entries
            print("4. Removing test workout entries...")
            result = session.execute(
                text("""
                    DELETE FROM entries
                    WHERE user_id = :user_id
                    AND kind = 'workout'
                    AND attrs->>'tags' = '["test", "workout"]'
                """),
                {"user_id": USER_ID}
            )
            print(f"   Deleted {result.rowcount} test workouts")

            # 5. Identify verbose knowledge entries
            print("5. Checking knowledge entry lengths...")
            result = session.execute(
                text("""
                    SELECT key, LENGTH(content) as len
                    FROM entries
                    WHERE user_id = :user_id
                    AND kind = 'knowledge'
                    AND LENGTH(content) > 600
                    ORDER BY LENGTH(content) DESC
                """),
                {"user_id": USER_ID}
            )
            verbose_entries = result.fetchall()
            if verbose_entries:
                print("   Verbose knowledge entries (>600 chars) that may need trimming:")
                for entry in verbose_entries:
                    print(f"   - {entry.key}: {entry.len} chars")
            else:
                print("   All knowledge entries are reasonably sized")

            # 6. Clean up empty attrs to just {}
            print("6. Normalizing empty attrs...")
            result = session.execute(
                text("""
                    UPDATE entries
                    SET attrs = '{}'::jsonb
                    WHERE user_id = :user_id
                    AND (attrs = '{}' OR attrs = 'null'::jsonb OR attrs IS NULL)
                """),
                {"user_id": USER_ID}
            )
            print(f"   Normalized attrs for {result.rowcount} entries")

            # Commit all changes
            session.commit()
            print("\n✅ Cleanup completed successfully!")

            # Show summary
            print("\n📊 Summary of cleaned data:")
            result = session.execute(
                text("""
                    SELECT
                        COUNT(*) as total_entries,
                        COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
                        COUNT(CASE WHEN status = 'archived' THEN 1 END) as archived,
                        COUNT(CASE WHEN attrs != '{}'::jsonb THEN 1 END) as with_attrs
                    FROM entries
                    WHERE user_id = :user_id
                """),
                {"user_id": USER_ID}
            )
            summary = result.fetchone()
            print(f"   Total entries: {summary.total_entries}")
            print(f"   Active: {summary.active}")
            print(f"   Archived: {summary.archived}")
            print(f"   With attrs data: {summary.with_attrs}")

        except Exception as e:
            session.rollback()
            print(f"❌ Error during cleanup: {e}")
            raise

if __name__ == "__main__":
    cleanup_data()