#!/usr/bin/env python3
"""Seed database with Sam's hybrid athlete training profile."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from src.memory.db import SessionLocal
from src.memory import crud

def get_user_id() -> str:
    user_id = os.getenv('FITNESS_USER_ID') or os.getenv('DEFAULT_USER_ID')
    if not user_id:
        raise ValueError("FITNESS_USER_ID (or DEFAULT_USER_ID) must be set in environment")
    return user_id

def seed_profile():
    """Seed database with complete training profile."""
    user_id = get_user_id()
    session = SessionLocal()

    try:
        print(f"Seeding profile for user: {user_id}")

        # ========================================
        # 1. LONG-TERM STRATEGY (12+ months)
        # ========================================
        print("\n📋 Creating long-term strategy...")
        crud.upsert_item(
            session, user_id,
            kind='strategy',
            key='long-term',
            content='Develop hybrid athlete profile: strong, mobile, and enduring. Balance strength maintenance (barbell + bodyweight), aerobic base (15-20km comfort), joint resilience (knees, hips, spine), and skill development (handstands, HSPU, rings, acro). Maintain year-round performance, not just peak.',
            status='active',
            attrs={
                'timeline_months': 12,
                'focus_areas': ['strength', 'endurance', 'mobility', 'skill'],
                'philosophy': 'hybrid-athlete'
            }
        )

        # ========================================
        # 2. SHORT-TERM STRATEGY (current 8-12 week block)
        # ========================================
        print("📋 Creating short-term strategy...")
        crud.upsert_item(
            session, user_id,
            kind='strategy',
            key='short-term',
            content='Current training block: 3 strength sessions/week (HSPU progression, weighted pull-ups, squat/deadlift), 2-3 endurance days (VO2 max intervals + zone-2), 2 mobility/recovery blocks (yoga, MIA). Focus: build freestanding HSPU volume, progress weighted pull-ups to +40kg, extend zone-2 to 75-80min.',
            status='active',
            due_date=date(2025, 12, 1),
            attrs={
                'weeks': 8,
                'strength_sessions_per_week': 3,
                'endurance_sessions_per_week': 3,
                'mobility_sessions_per_week': 2
            }
        )

        # ========================================
        # 3. PRIMARY GOALS
        # ========================================
        print("\n🎯 Creating goals...")

        # HSPU goal
        crud.upsert_item(
            session, user_id,
            kind='goal',
            key='hspu-deficit-progression',
            content='Progress freestanding HSPU: 4x5 clean → 5x5 → add 2-3cm deficit',
            priority=1,
            status='active',
            tags='strength upper-body skill',
            attrs={'current_reps': 20, 'target_reps': 25, 'deficit_cm': 0, 'target_deficit_cm': 3}
        )

        # Weighted pull-up goal
        crud.upsert_item(
            session, user_id,
            kind='goal',
            key='weighted-pullup-40kg',
            content='Weighted pull-up progression: +30kg x7 → +40kg x3-5',
            priority=1,
            status='active',
            tags='strength upper-body pulling',
            attrs={'current_weight_kg': 30, 'current_reps': 7, 'target_weight_kg': 40, 'target_reps': 5}
        )

        # Bulgarian split squat goal
        crud.upsert_item(
            session, user_id,
            kind='goal',
            key='bulgarian-48kg',
            content='Bulgarian split squat: 4x6/leg @ 40kg → 4x8/leg @ 48kg with full depth',
            priority=2,
            status='active',
            tags='strength lower-body unilateral',
            attrs={'current_weight_kg': 40, 'current_reps': 6, 'target_weight_kg': 48, 'target_reps': 8}
        )

        # Deadlift goal
        crud.upsert_item(
            session, user_id,
            kind='goal',
            key='deadlift-100kg-peak',
            content='Deadlift peak: 3x3 @ 100kg (~85% max) with excellent bar speed',
            priority=2,
            status='active',
            tags='strength lower-body posterior',
            attrs={'current_weight_kg': 90, 'target_weight_kg': 100, 'current_sets': 3, 'current_reps': 6}
        )

        # Zone-2 goal
        crud.upsert_item(
            session, user_id,
            kind='goal',
            key='zone2-80min',
            content='Extend zone-2 base runs: 60min → 75-80min with avg HR ≤135 bpm',
            priority=2,
            status='active',
            tags='endurance running aerobic',
            attrs={'current_duration_min': 60, 'target_duration_min': 80, 'current_avg_hr': 135, 'target_avg_hr': 135}
        )

        # VO2 max goal
        crud.upsert_item(
            session, user_id,
            kind='goal',
            key='vo2-4x4min',
            content='VO2 max intervals: 4x3min @ 16km/h → 4x4min @ 16km/h with 2-2.5min recovery',
            priority=2,
            status='active',
            tags='endurance running vo2max',
            attrs={'current_intervals': 4, 'current_duration_min': 3, 'target_duration_min': 4, 'pace_kmh': 16}
        )

        # ========================================
        # 4. CURRENT STATE / METRICS
        # ========================================
        print("\n📊 Recording current state...")

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='hspu-performance',
            content='Freestanding HSPU: 4x5 clean reps (advanced)',
            tags='upper-body strength skill',
            attrs={'sets': 4, 'reps': 5, 'difficulty': 'advanced'}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='weighted-pullup-performance',
            content='Weighted pull-up: 7 reps @ +30kg, training 4x5 @ +30-32.5kg',
            tags='upper-body strength pulling',
            attrs={'max_weight_kg': 30, 'max_reps': 7, 'training_weight_kg': 32.5, 'training_sets': 4, 'training_reps': 5}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='squat-max',
            content='Back squat: Max 80kg, training @ 60kg for 4x6 (70-75%)',
            tags='lower-body strength',
            attrs={'max_kg': 80, 'training_kg': 60, 'training_sets': 4, 'training_reps': 6, 'training_intensity': 0.75}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='deadlift-max',
            content='Deadlift: Max ~110-120kg, training 80-90kg for 3x4-6 (70-75%)',
            tags='lower-body strength posterior',
            attrs={'max_kg': 115, 'training_kg': 85, 'training_sets': 3, 'training_reps': 5, 'training_intensity': 0.74}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='5k-pace',
            content='Running 5k pace: ~13 km/h (~4:36/km)',
            tags='running endurance',
            attrs={'distance_km': 5, 'pace_kmh': 13, 'pace_per_km': '4:36'}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='vo2-intervals',
            content='VO2 intervals: 4x3min @ 16km/h or 6x2min @ 16-17km/h, HR peaks ~170',
            tags='running vo2max intervals',
            attrs={'protocol_1': '4x3min @ 16km/h', 'protocol_2': '6x2min @ 16-17km/h', 'peak_hr': 170, 'recovery_sec': 90}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='zone2-runs',
            content='Zone-2 runs: 60-70min @ 9.5-10.5km/h, HR 120-140bpm, avg ~132-136bpm',
            tags='running zone2 aerobic',
            attrs={'duration_min': 65, 'pace_low_kmh': 9.5, 'pace_high_kmh': 10.5, 'hr_low': 120, 'hr_high': 140, 'hr_avg': 134}
        )

        crud.upsert_item(
            session, user_id,
            kind='current',
            key='hrv-recovery',
            content='HRV: Typical 110-120ms, recovers fast. No current injuries, minor knee/shoulder prehab ongoing',
            tags='recovery hrv health',
            attrs={'hrv_ms': 115, 'recovery_quality': 'high', 'injuries': None, 'prehab': ['knee', 'shoulder']}
        )

        # ========================================
        # 5. PREFERENCES
        # ========================================
        print("\n⚙️  Creating preferences...")

        crud.upsert_item(
            session, user_id,
            kind='preference',
            key='weekly-structure',
            content='Training 6 days/week: Mon (VO2 intervals), Tue (home strength), Wed (yoga/mobility), Thu (zone-2), Fri (gym strength), Sat (long run/hike/acro), Sun (recovery/skill)',
            tags='schedule structure',
            attrs={'days_per_week': 6, 'strength_days': 3, 'endurance_days': 3, 'mobility_days': 2}
        )

        crud.upsert_item(
            session, user_id,
            kind='preference',
            key='equipment-access',
            content='Home: bodyweight, rings, pull-up bar, dumbbells. Gym: barbell, squat rack, deadlift platform',
            tags='equipment logistics',
            attrs={'home_equipment': ['bodyweight', 'rings', 'pullup-bar', 'dumbbells'], 'gym_equipment': ['barbell', 'squat-rack', 'deadlift-platform']}
        )

        crud.upsert_item(
            session, user_id,
            kind='preference',
            key='mobility-practices',
            content='Hot yoga weekly, Dylan Werner MIA sessions (Superficial Back Line, Posterior Functional Line), 90/90 hip flow, AcroMotion on weekends',
            tags='mobility yoga recovery',
            attrs={'yoga_frequency': 'weekly', 'yoga_types': ['hot-yoga', 'MIA'], 'mobility_drills': ['90-90-hip-flow', 'acro-motion']}
        )

        crud.upsert_item(
            session, user_id,
            kind='preference',
            key='recovery-protocols',
            content='Sauna + ice bath weekly (Friday post-lift). HRV monitoring guides session intensity. Movement quality prioritized over volume.',
            tags='recovery sauna ice-bath hrv',
            attrs={'sauna_frequency': 'weekly', 'ice_bath_frequency': 'weekly', 'hrv_monitoring': True, 'philosophy': 'quality-over-volume'}
        )

        # ========================================
        # 6. KNOWLEDGE BASE
        # ========================================
        print("\n📚 Creating knowledge entries...")

        crud.upsert_item(
            session, user_id,
            kind='knowledge',
            key='training-philosophy',
            content='Hybrid athlete approach: equal respect for strength, endurance, and mobility. Auto-regulation via HRV + subjective readiness. Movement quality > volume. Recovery and tendon work are non-negotiable.',
            tags='philosophy principles training',
            attrs={'approach': 'hybrid', 'autoregulation': True, 'priorities': ['quality', 'recovery', 'balance']}
        )

        crud.upsert_item(
            session, user_id,
            kind='knowledge',
            key='recovery-patterns',
            content='HRV 110-120ms typical, recovers fast. Strength sessions need proper spacing. Mobility twice/week maintains fascial health. Sleep quality significantly impacts performance.',
            tags='recovery hrv sleep',
            attrs={'hrv_range_ms': [110, 120], 'recovery_speed': 'fast', 'mobility_min_weekly': 2}
        )

        crud.upsert_item(
            session, user_id,
            kind='knowledge',
            key='hspu-technique',
            content='Freestanding HSPU: Currently 4x5 clean. Focus on handstand hold stability, controlled descent, explosive push. Next progression: build to 5x5, then add 2-3cm deficit.',
            tags='hspu handstand skill upper-body',
            attrs={'current_volume': 20, 'next_milestone': 'deficit', 'technique_focus': ['stability', 'control', 'explosiveness']}
        )

        crud.upsert_item(
            session, user_id,
            kind='knowledge',
            key='weighted-pullup-progression',
            content='Weighted pull-up: Max +30kg x7. Training 4x5 @ +30-32.5kg for strength. Target: +40kg x3-5. Focus on full ROM, controlled eccentric, explosive concentric.',
            tags='pull-up weighted upper-body pulling',
            attrs={'max_weight_kg': 30, 'max_reps': 7, 'target_weight_kg': 40, 'technique': ['full-ROM', 'controlled-eccentric', 'explosive-concentric']}
        )

        crud.upsert_item(
            session, user_id,
            kind='knowledge',
            key='running-zones',
            content='Zone-2: 9.5-10.5 km/h, HR 120-140bpm for base building. VO2 max: 16km/h intervals, HR peaks ~170. 5k pace: ~13km/h. HR control improving with training.',
            tags='running zones heart-rate endurance',
            attrs={
                'zone2_pace_kmh': [9.5, 10.5],
                'zone2_hr': [120, 140],
                'vo2_pace_kmh': 16,
                'vo2_hr_peak': 170,
                '5k_pace_kmh': 13
            }
        )

        # ========================================
        # 7. TRAINING PRINCIPLES
        # ========================================
        print("\n📐 Creating training principles...")

        crud.upsert_item(
            session, user_id,
            kind='principle',
            key='progressive-overload',
            content='Gradual progression in strength (weight, reps, or difficulty), endurance (duration, pace, or intervals), and skill (complexity or volume). Avoid big jumps that risk injury.',
            tags='progression strength endurance',
            attrs={'methods': ['weight', 'reps', 'duration', 'pace', 'complexity']}
        )

        crud.upsert_item(
            session, user_id,
            kind='principle',
            key='autoregulation',
            content='HRV + subjective readiness guide intensity. Lower HRV or fatigue → reduce intensity or take extra recovery. Listen to body signals (joint stress, energy, motivation).',
            tags='autoregulation hrv recovery',
            attrs={'signals': ['HRV', 'subjective_readiness', 'joint_health', 'energy', 'motivation']}
        )

        crud.upsert_item(
            session, user_id,
            kind='principle',
            key='balance-push-pull',
            content='Maintain balance: push/pull ratio, upper/lower body, endurance/recovery. Prevent imbalances and overuse injuries through varied training.',
            tags='balance injury-prevention',
            attrs={'ratios': ['push-pull', 'upper-lower', 'endurance-recovery']}
        )

        crud.upsert_item(
            session, user_id,
            kind='principle',
            key='joint-resilience',
            content='Prehab for knees, shoulders critical. Include Nordics, soleus raises, tibialis work, ring work for shoulder health. Mobility twice/week non-negotiable.',
            tags='prehab injury-prevention joints',
            attrs={'prehab_areas': ['knees', 'shoulders'], 'exercises': ['nordics', 'soleus-raises', 'tibialis-raises', 'ring-work'], 'mobility_frequency': 'twice-weekly'}
        )

        # ========================================
        # 8. ACTIVE TRAINING PLAN (weekly structure)
        # ========================================
        print("\n📅 Creating weekly training plan...")

        crud.upsert_item(
            session, user_id,
            kind='plan',
            key='weekly-hybrid-split',
            content='Hybrid athlete weekly structure: 3 strength (Tue home, Fri gym, Sat optional), 3 endurance (Mon VO2, Thu zone-2, Sat long), 2 mobility (Wed yoga, Sun recovery/skill)',
            status='active',
            parent_key='short-term',
            tags='weekly-plan strength endurance mobility',
            attrs={
                'strength_days': ['tuesday', 'friday', 'saturday'],
                'endurance_days': ['monday', 'thursday', 'saturday'],
                'mobility_days': ['wednesday', 'sunday'],
                'total_sessions_per_week': 6
            }
        )

        # Plan steps (weekly template)
        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='monday-vo2',
            content='Monday: VO2 max intervals - 4x3min @ 15-16km/h with 90s rest (HR peaks ~170) + core stability',
            priority=1,
            parent_key='weekly-hybrid-split',
            tags='running intervals vo2max',
            attrs={'day': 'monday', 'type': 'vo2_intervals', 'intervals': 4, 'duration_min': 3, 'pace_kmh': 16, 'rest_sec': 90}
        )

        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='tuesday-home-strength',
            content='Tuesday: Home strength - Freestanding HSPU 4x5, Bulgarian split squats 4x6/leg @ 40kg (3s eccentric), weighted pull-ups 4x5 @ +30kg, ring archer push-ups 3x6/side, ring fallouts 3x8',
            priority=2,
            parent_key='weekly-hybrid-split',
            tags='strength upper-body lower-body home',
            attrs={
                'day': 'tuesday',
                'type': 'home_strength',
                'exercises': [
                    {'name': 'Freestanding HSPU', 'sets': 4, 'reps': 5},
                    {'name': 'Bulgarian Split Squat', 'sets': 4, 'reps': 6, 'weight_kg': 40, 'tempo': '3s eccentric'},
                    {'name': 'Weighted Pull-up', 'sets': 4, 'reps': 5, 'weight_kg': 30},
                    {'name': 'Ring Archer Push-up', 'sets': 3, 'reps': 6},
                    {'name': 'Ring Fallout', 'sets': 3, 'reps': 8}
                ]
            }
        )

        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='wednesday-mobility',
            content='Wednesday: Mobility/Yoga - Hot yoga OR Dylan Werner MIA (Superficial Back Line, Posterior Functional Line), 90/90 hip flow, fascia + thoracic focus',
            priority=3,
            parent_key='weekly-hybrid-split',
            tags='mobility yoga recovery',
            attrs={'day': 'wednesday', 'type': 'mobility', 'options': ['hot-yoga', 'MIA'], 'focus': ['fascia', 'thoracic', 'hips']}
        )

        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='thursday-zone2',
            content='Thursday: Zone-2 endurance - 60min @ 9.5-10.5km/h, HR 120-140bpm (avg ~132-136bpm), conversational pace',
            priority=4,
            parent_key='weekly-hybrid-split',
            tags='running zone2 aerobic',
            attrs={'day': 'thursday', 'type': 'zone2_run', 'duration_min': 60, 'pace_kmh': 10, 'hr_range': [120, 140]}
        )

        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='friday-gym-strength',
            content='Friday: Gym strength - Back squat 4x6 @ 60kg, Deadlift 3x5 @ 85kg, Bar muscle-ups 3x6, Ring rows 3x8, Nordics 2x4, Soleus raises 2x15, Tibialis raises 1x20. Post-workout: Sauna + ice bath',
            priority=5,
            parent_key='weekly-hybrid-split',
            tags='strength lower-body gym pulling',
            attrs={
                'day': 'friday',
                'type': 'gym_strength',
                'exercises': [
                    {'name': 'Back Squat', 'sets': 4, 'reps': 6, 'weight_kg': 60},
                    {'name': 'Deadlift', 'sets': 3, 'reps': 5, 'weight_kg': 85},
                    {'name': 'Bar Muscle-up', 'sets': 3, 'reps': 6},
                    {'name': 'Ring Row', 'sets': 3, 'reps': 8},
                    {'name': 'Nordic Curl', 'sets': 2, 'reps': 4},
                    {'name': 'Soleus Raise', 'sets': 2, 'reps': 15},
                    {'name': 'Tibialis Raise', 'sets': 1, 'reps': 20}
                ],
                'recovery': 'sauna + ice bath'
            }
        )

        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='saturday-long-run',
            content='Saturday: Long aerobic/hike/AcroMotion - 8-10km hilly run (500-700m elevation, 6:00-6:40/km pace) OR acro yoga + skill practice',
            priority=6,
            parent_key='weekly-hybrid-split',
            tags='endurance running hiking acro skill',
            attrs={
                'day': 'saturday',
                'type': 'long_endurance_or_skill',
                'option_1': {'type': 'hilly_run', 'distance_km': 9, 'elevation_m': 600, 'pace': '6:20/km'},
                'option_2': {'type': 'acro_yoga', 'focus': ['mobility', 'partner_strength', 'locomotion']}
            }
        )

        crud.upsert_item(
            session, user_id,
            kind='plan-step',
            key='sunday-recovery',
            content='Sunday: Recovery/skill practice - Light handstand work, yoga, full rest (listen to HRV)',
            priority=7,
            parent_key='weekly-hybrid-split',
            tags='recovery skill handstand yoga',
            attrs={'day': 'sunday', 'type': 'recovery_or_skill', 'options': ['handstand', 'yoga', 'full-rest']}
        )

        print("\n✅ Profile seeded successfully!")
        print(f"\nSeeded for user: {user_id}")
        print("\nSummary:")
        print("- Strategies: long-term + short-term")
        print("- Goals: 6 primary objectives")
        print("- Current state: 7 performance metrics")
        print("- Preferences: 4 training preferences")
        print("- Knowledge: 5 key insights")
        print("- Principles: 4 training principles")
        print("- Weekly plan: 7-day hybrid structure with detailed steps")

    except Exception as e:
        print(f"\n❌ Error seeding profile: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_profile()
