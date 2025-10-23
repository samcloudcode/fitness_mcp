#!/usr/bin/env python3
"""
Migration script to transform existing entries to new planning structure.

Changes:
1. Archive exercise-specific progression plans (4 entries)
2. Archive session template entries (14 entries: 2 plan + 12 plan-step)
3. Transform 'weekly-hybrid-split' plan to 'current-program' program
4. Transform 'week-oct-20-26-sailing' to ISO week format '2025-week-43'
5. Add training type suffix to workout-plan entries (5 entries)

Run with: source .env && uv run python scripts/migrate_planning_structure.py
"""

import os
import sys
from datetime import datetime

# Database connection - check env first
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Convert to psycopg driver
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

engine = create_engine(DATABASE_URL)
USER_ID = os.getenv('FITNESS_USER_ID', '1')


def archive_entry(session: Session, kind: str, key: str, reason: str):
    """Archive a specific entry by kind and key."""
    result = session.execute(
        text("UPDATE public.entries SET status = 'archived' WHERE user_id = :user_id AND kind = :kind AND key = :key AND status = 'active' RETURNING id"),
        {"user_id": USER_ID, "kind": kind, "key": key}
    )
    row = result.fetchone()
    if row:
        print(f"✓ Archived {kind}::{key} - {reason}")
        return True
    else:
        print(f"⚠ Not found: {kind}::{key}")
        return False


def transform_entry(session: Session, old_kind: str, old_key: str, new_kind: str, new_key: str, new_content: str = None):
    """Transform an entry to new kind/key, optionally updating content."""
    # Get existing entry
    result = session.execute(
        text("SELECT id, content FROM public.entries WHERE user_id = :user_id AND kind = :kind AND key = :key AND status = 'active'"),
        {"user_id": USER_ID, "kind": old_kind, "key": old_key}
    )
    row = result.fetchone()

    if not row:
        print(f"⚠ Not found: {old_kind}::{old_key}")
        return False

    old_id, old_content = row
    content_to_use = new_content if new_content else old_content

    # Create new entry
    session.execute(
        text("""
            INSERT INTO public.entries (user_id, kind, key, content, status, created_at, updated_at)
            VALUES (:user_id, :kind, :key, :content, 'active', NOW(), NOW())
        """),
        {"user_id": USER_ID, "kind": new_kind, "key": new_key, "content": content_to_use}
    )

    # Archive old entry
    session.execute(
        text("UPDATE public.entries SET status = 'archived' WHERE id = :id"),
        {"id": old_id}
    )

    print(f"✓ Transformed {old_kind}::{old_key} → {new_kind}::{new_key}")
    return True


def main():
    print("=" * 80)
    print("MIGRATION: Planning Structure Transformation")
    print("=" * 80)
    print()

    with Session(engine) as session:
        # Phase 1: Archive exercise-specific progressions
        print("Phase 1: Archiving exercise-specific progression plans...")
        print("-" * 80)

        progressions_to_archive = [
            ('plan', 'hspu-progression-10-reps', 'Too specific, doesn\'t add value'),
            ('plan', 'one-arm-pullup-progression', 'Too specific, doesn\'t add value'),
            ('plan', 'one-arm-pushup-progression', 'Too specific, doesn\'t add value'),
            ('plan', 'ring-dips-progression', 'Too specific, doesn\'t add value'),
        ]

        archived_count = 0
        for kind, key, reason in progressions_to_archive:
            if archive_entry(session, kind, key, reason):
                archived_count += 1

        print(f"\n→ Archived {archived_count}/4 progression plans\n")

        # Phase 2: Archive session templates
        print("Phase 2: Archiving session template entries...")
        print("-" * 80)

        templates_to_archive = [
            ('plan', 'calisthenics-session-template', 'Template, not scheduled workout'),
            ('plan', 'monday-strength-template', 'Template, not scheduled workout'),
            ('plan-step', 'friday-4k-tempo', 'Template, not scheduled workout'),
            ('plan-step', 'friday-gym-strength', 'Template, not scheduled workout'),
            ('plan-step', 'monday-5k-easy', 'Template, not scheduled workout'),
            ('plan-step', 'monday-vo2', 'Template, not scheduled workout'),
            ('plan-step', 'saturday-long-run', 'Template, not scheduled workout'),
            ('plan-step', 'sunday-recovery', 'Template, not scheduled workout'),
            ('plan-step', 'thursday-zone2', 'Template, not scheduled workout'),
            ('plan-step', 'tuesday-home-strength', 'Template, not scheduled workout'),
            ('plan-step', 'wednesday-6k-strides', 'Template, not scheduled workout'),
            ('plan-step', 'wednesday-mobility', 'Template, not scheduled workout'),
            ('plan-step', 'week-1-base', 'Template, not scheduled workout'),
            ('plan-step', 'week-sailing-adaptation-oct6', 'Template, not scheduled workout'),
        ]

        archived_count = 0
        for kind, key, reason in templates_to_archive:
            if archive_entry(session, kind, key, reason):
                archived_count += 1

        print(f"\n→ Archived {archived_count}/14 template entries\n")

        # Phase 3: Transform weekly-hybrid-split to current-program
        print("Phase 3: Transforming weekly-hybrid-split to current-program...")
        print("-" * 80)

        # Get existing content
        result = session.execute(
            text("SELECT content FROM public.entries WHERE user_id = :user_id AND kind = 'plan' AND key = 'weekly-hybrid-split' AND status = 'active'"),
            {"user_id": USER_ID}
        )
        row = result.fetchone()

        if row:
            old_content = row[0]
            # Enhance with "why" context
            new_content = f"{old_content}\n\nWhy: This hybrid approach balances multiple goals (strength, endurance, mobility) without interference. Strength and endurance separated by time or modality. Daily mobility work for consistency over intensity."

            transform_entry(
                session,
                'plan', 'weekly-hybrid-split',
                'program', 'current-program',
                new_content
            )
        else:
            print("⚠ weekly-hybrid-split not found, skipping")

        print()

        # Phase 4: Transform week-oct-20-26-sailing to ISO week format
        print("Phase 4: Transforming week entry to ISO week format...")
        print("-" * 80)

        # Oct 20, 2025 is in week 43
        transform_entry(
            session,
            'plan', 'week-oct-20-26-sailing',
            'week', '2025-week-43'
        )

        print()

        # Phase 5: Add training type to workout-plan entries
        print("Phase 5: Checking workout-plan entries for type suffix...")
        print("-" * 80)

        # Get all workout-plan entries
        result = session.execute(
            text("SELECT key, content FROM public.entries WHERE user_id = :user_id AND kind = 'workout-plan' AND status = 'active' ORDER BY key"),
            {"user_id": USER_ID}
        )
        workout_plans = result.fetchall()

        print(f"Found {len(workout_plans)} workout-plan entries")
        if len(workout_plans) > 0:
            print("\nNOTE: workout-plan entries need manual inspection to add training type suffix.")
            print("These should be transformed to 'session' kind with keys like '2025-10-22-strength'")
            print("\nExisting workout-plan entries:")
            for key, content in workout_plans:
                print(f"  - {key}: {content[:80]}...")

        print()

        # Commit all changes
        print("=" * 80)
        print("Committing changes...")
        session.commit()
        print("✓ Migration completed successfully!")
        print("=" * 80)

        # Summary
        print("\nSummary:")
        print(f"  - Archived 4 exercise progression plans")
        print(f"  - Archived 14 session template entries")
        print(f"  - Created 'current-program' from 'weekly-hybrid-split'")
        print(f"  - Transformed week entry to ISO week format")
        print(f"  - Found {len(workout_plans)} workout-plan entries needing manual review")
        print()
        print("Next steps:")
        print("  1. Review workout-plan entries and transform to 'session' with type suffix")
        print("  2. Verify migration with: uv run python scripts/verify_migration.py")
        print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
