#!/usr/bin/env python3
"""Compact verbose database entries to follow brevity guidelines."""
import os
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from src.memory.crud import upsert_item
from src.memory.db import SessionLocal

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Target: Knowledge 200-400 words (~1000-2000 chars)
# Target: Principles 150-300 words (~750-1500 chars)
# Target: Preferences <200 words (~<1000 chars)

COMPACTED_ENTRIES = {
    # KNOWLEDGE - Store user-specific observations, not textbook content
    ('knowledge', 'mcgill-big-3-spine'): """McGill Big 3 - My spine stabilization core work:

**User's Contraindication Context**: Avoiding due to current low back sensitivity. Will reintroduce post-recovery as maintenance work.

**Protocol** (when cleared):
- Curl-up: Anti-extension (protect spine in flexion)
- Side plank: Anti-lateral flexion (stability under side load)
- Bird dog: Anti-rotation (coordinated hip/shoulder stability)

**Key Coaching Points**:
- These are HOLDS not reps - building endurance
- McGill's emphasis: spine stays neutral, no movement
- User should focus on bird dog for shoulder stability work
- Integrate post-recovery: 2-3x/week as warm-up or finisher""",

    ('knowledge', 'blueprint-supplements-analysis'): """Blueprint Supplements - User's current stack:

**What User Takes**:
- Longevity Mix (daily): Creatine, collagen, ashwagandha, various vitamins
- Red/Green powders: Polyphenols, antioxidants

**User-Specific Observations**:
- Taking for convenience, not because of belief in Blueprint protocol specifically
- Creatine (5g/day): solid evidence, keeping
- Collagen: User follows Keith Baar protocol separately (15g + vit C pre-training)
- Ashwagandha: May support recovery, low risk
- Polyphenols timing: Avoid immediately post-strength training (may blunt adaptation)

**Coaching Notes**:
- User doesn't need to defend Blueprint - just using convenient powder format
- Watch polyphenol timing around strength work
- Core supplements with strong evidence: creatine, collagen+vitC, protein""",

    ('knowledge', 'collagen-supplement-choice'): """Collagen: Gelatin vs Peptides (Keith Baar research)

**User's Choice**: Gelatin (15g + 50mg vit C, 30-60 min pre-training)

**Why Gelatin Over Peptides**:
- Both work, but gelatin cheaper and Baar's research used gelatin
- Pre-training timing: maximize blood amino acid levels during training
- Works for tendons, ligaments, connective tissue adaptation

**Protocol**:
- 15g gelatin + 50mg vitamin C
- 30-60 min before training
- Can use collagen peptides if preferred (more expensive, easier to mix)

**User Context**: Following for knee/tendon health during strength progressions""",

    ('knowledge', 'concurrent-training-management'): """Concurrent Training - User's hybrid approach:

**Interference Effect Reality**:
- Doing both strength + endurance creates conflicting signals
- User accepts some compromise on max strength/max VO2 for hybrid goals

**User's Management Strategies**:
- Separate by 3+ hours when possible (AM run, PM strength)
- Strength days: keep cardio easy/low volume
- VO2 days: separate from strength or accept fatigue
- Periodize: strength blocks vs endurance blocks
- Fuel properly (not fasted for key sessions)

**Key Principle**: User prioritizes well-rounded fitness over specialization. Managing interference, not eliminating it.""",

    ('knowledge', 'knee-health-best-practices'): """Knee Health - User's key practices:

**Alignment Focus**:
- Knees track over toes (prevent valgus collapse)
- Neutral arches (not collapsed)
- Glute engagement in squats/lunges

**User's Current Priorities**:
- VMO strengthening: ATG split squats, Peterson step-ups
- Patellar tracking: focus on foot/hip alignment
- Avoiding: deep knee flexion under load until tracking improves

**Contraindications Tracked**:
- Sharp pain = stop, dull stretch = okay
- Knee issues tagged in knowledge base for exercise selection

**Prehab Integration**: User does knee-focused warm-ups before lower body work""",

    ('knowledge', 'ankle-mobility-protocols'): """Ankle Mobility - User's approach:

**Assessment**:
- Wall test: knee 4-5" past toes without heel lift
- User's current status: Limited, working on it

**User's Protocol**:
- Daily ankle mobility: wall variations, controlled rotations
- Loaded work: heel-elevated goblet squats (working around limitation)
- ATG split squats: addresses both mobility + strength

**Why It Matters for User**:
- Squat depth limitation
- Pistol squat progression requirement
- Running mechanics

**Key Insight**: User improving through loaded movement (ATG split squats) more than static stretching""",

    ('knowledge', 'isometric-tendon-training'): """Isometric Tendon Training (Keith Baar):

**Protocol**:
- 2 sets × 30-60s holds
- Frequency: Daily or every-other-day
- Load: Moderate (not max effort)

**User Application**:
- Could use for knee tendon health (wall sit variations)
- Combine with collagen protocol (15g gelatin + vit C pre-work)

**Why Isometrics for Tendons**:
- Baar's research: long-duration tension stimulates collagen synthesis
- Safer than heavy dynamic loading during recovery
- User could integrate for patellar tendon health

**Current Status**: Not actively using, available protocol if needed""",

    ('knowledge', 'collagen-vitamin-c-protocol'): """Collagen + Vitamin C Protocol (Keith Baar):

**User's Protocol**:
- 15g gelatin + 50mg vitamin C
- Timing: 30-60 min before training
- Frequency: Before lower-body/tendon-focused sessions

**Why**:
- Maximizes blood amino acids during training
- Vitamin C required for collagen synthesis
- Targets connective tissue adaptation

**User Context**: Using for knee/tendon health during strength progressions. Simple, evidence-based, low-risk.""",

    # PRINCIPLES - Reminders, not full protocols
    ('principle', '80-20-polarization'): """80/20 Training: ~80% easy, ~20% hard.

**User's Application**:
- Most runs: conversational pace (Zone 2)
- 1-2x/week: VO2 intervals or tempo work
- Avoid "grey zone" (moderate-hard every day)

**Why**: Allows high volume + high intensity without chronic fatigue. Proven in endurance research.

**User's Current Challenge**: Tendency to push easy runs too hard. Need discipline on easy days.""",

    ('principle', 'exercise-ordering-fast-first'): """Exercise Order: Fast/explosive → strength → hypertrophy → endurance.

**Rationale**: Neural freshness for speed/power work, fatigue resistance for endurance.

**User's Application**:
- Start with explosive (plyo, Olympic lifts, sprints)
- Then heavy strength (squat, deadlift, weighted pull-ups)
- Finish with accessories or conditioning

**Key**: Don't do hard conditioning before strength work.""",

    ('principle', 'deload-protocol'): """Deload: Planned recovery week every 3-4 weeks.

**User's Protocol**:
- Reduce volume 40-50% (cut sets, not intensity)
- Keep intensity (heavy weights, hard intervals) but less of it
- Active recovery: mobility, light movement

**Why**: Allows supercompensation. Research shows performance improves post-deload.

**Signs User Needs Deload**: Sleep issues, motivation drop, nagging soreness, performance plateau.""",

    ('principle', 'rest-period-efficiency'): """Rest Periods: Use them productively.

**User's Approach**:
- Between strength sets: antagonist mobility or light antagonist work
- Example: Pull-up rest = shoulder mobility, squat rest = hip flexor stretch
- Superset antagonists when appropriate (push/pull)

**Benefits**: Time-efficient, maintains movement quality, addresses limiters.

**Key**: Don't compromise main lift performance.""",

    ('principle', 'connective-tissue-adaptation'): """Connective Tissue Adaptation: ~10x slower than muscle.

**Implication**: Tendons/ligaments need months to adapt, muscles need weeks.

**User's Application**:
- Progress load conservatively on joint-intensive movements
- Especially: pistols, HSPU, heavy overhead work
- Use isometrics + collagen protocol for tendon health
- Patience with skills requiring tendon strength

**Key**: Muscle strength can outpace tendon strength = injury risk. Progress wisely.""",

    # PREFERENCES - Brief, actionable
    ('preference', 'recovery-protocols'): """Recovery Timing Preferences:

**Sauna**: Post-workout, 2-3x/week, 20-30min. Avoid immediately before strength work.

**Cold Exposure**: Separate from strength training by 4+ hours if possible (may blunt adaptation). Fine before or after endurance work.

**Sleep**: 7-8 hours, prioritize consistency.

**Nutrition**: Not fasted for key strength/VO2 sessions. Post-workout protein within 2 hours.""",
}


def main():
    user_id = os.getenv('FITNESS_USER_ID') or os.getenv('DEFAULT_USER_ID')

    with get_session() as session:
        print("Compacting verbose entries...\n")

        for (kind, key), content in COMPACTED_ENTRIES.items():
            old_len = len(content)
            print(f"Updating {kind}/{key}...")
            print(f"  New length: {old_len} chars (~{old_len // 5} words)")

            upsert_item(
                session=session,
                user_id=user_id,
                kind=kind,
                key=key,
                content=content.strip()
            )

        session.commit()
        print(f"\n✅ Compacted {len(COMPACTED_ENTRIES)} entries")


if __name__ == '__main__':
    main()
