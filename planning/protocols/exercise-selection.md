# Exercise Selection Protocol

## Purpose

Provides evidence-based criteria for selecting exercises that match training goals, individual constraints, and movement quality standards. Ensures exercises are appropriate for user's skill level, equipment availability, and injury limitations.

## When to Use

- Designing program exercise architecture (program-creator)
- Selecting specific exercises for workouts (workout-creator)
- Evaluating exercise substitutions (any agent)
- Assessing if exercises align with user's goals and constraints

## Decision Framework

### Primary Exercise Selection Criteria

**1. Goal Specificity**
- **Strength**: Compound movements with heavy loading potential (squat, deadlift, bench press, overhead press, rows)
- **Hypertrophy**: Mix of compounds and isolation with good tension/pump (moderate-high reps, controlled tempo)
- **Power**: Explosive movements with force-velocity emphasis (Olympic lifts, jumps, throws)
- **Endurance**: Submaximal loading with sustained effort (circuits, high reps, minimal rest)
- **Sport-specific**: Movements matching sport demands (e.g., rugby → ground-based strength, scrummage positions)

**2. Movement Pattern Coverage** (Cross-check: movement-patterns.md)
- Squat pattern (bilateral knee flexion)
- Hinge pattern (hip flexion, posterior chain)
- Push (horizontal and vertical)
- Pull (horizontal and vertical)
- Loaded carry
- Unilateral/single-leg
- Core/anti-movement

**3. Training Age and Skill Level**
- **Beginner** (0-1 years): Simple, stable movements (goblet squat, trap bar deadlift, machine press, supported rows)
- **Intermediate** (1-3 years): Standard barbell lifts, more technical variations (back squat, conventional deadlift, barbell bench)
- **Advanced** (3+ years): Complex variations, specialty bars, advanced techniques (front squat, sumo deadlift, pause reps)

**4. Equipment Availability** (Check user preferences)
- Required equipment must be available
- No assumptions (verify before selecting)
- Have substitutions ready for common constraints

**5. Injury and Limitation Constraints** (CRITICAL - Cross-check: injury-prevention.md)
- **ALWAYS check user's knowledge entries for limitations**
- Contraindicated movements must be avoided
- Modified versions may be appropriate
- Substitute within same movement pattern when needed

**6. Technical Complexity vs Fatigue State**
- High-skill exercises (Olympic lifts, heavy compounds) early in session/week
- Lower-skill exercises (machines, isolation) when fatigued
- Don't program complex movements on high-fatigue days

### Exercise Hierarchy Framework

**Tier 1: Primary Movements** (main strength/skill work)
- Highest neural demand
- Most specific to goals
- Programmed first in session
- Examples: Competition lifts, main compound movements

**Tier 2: Secondary Movements** (support primary)
- Support primary movement development
- Less technically demanding than primary
- Moderate to high load
- Examples: Variations of primary (paused squats, deficit deadlifts), or secondary compounds (Romanian deadlifts, incline press)

**Tier 3: Accessory Movements** (address weaknesses, balance)
- Targeted muscle groups or movement patterns
- Lower neural demand
- Moderate load, higher volume potential
- Examples: Isolation work (hamstring curls, bicep curls, lateral raises), unilateral work (lunges, single-leg RDL)

**Tier 4: Prehab/Mobility** (injury prevention, movement quality)
- Lowest intensity, highest frequency potential
- Address individual limitations
- Can be done daily
- Examples: Band work (face pulls, pull-aparts), rotator cuff exercises, hip CARs, core stability

### Exercise Selection Logic Flow

```
1. Review user's goals (from goals, program)
   ↓
2. LOAD injury-prevention.md → Check user's knowledge entries for limitations
   ↓
3. Identify required movement patterns (from movement-patterns.md)
   ↓
4. Select Tier 1 (primary) exercises:
   - Match goal specificity
   - Appropriate for training age
   - Equipment available
   - NO contraindications
   ↓
5. Select Tier 2 (secondary) exercises:
   - Support primary movements
   - Fill movement pattern gaps
   - Check equipment and limitations
   ↓
6. Select Tier 3 (accessory) exercises:
   - Address weaknesses
   - Balance muscle groups
   - Complete movement patterns
   ↓
7. Select Tier 4 (prehab/mobility):
   - Target specific limitations (from knowledge)
   - Preventive for high-risk areas
   - Daily sustainability
   ↓
8. Validate:
   - All limitations honored? (injury-prevention.md)
   - Movement balance achieved? (movement-patterns.md)
   - Equipment available? (user preferences)
   - Appropriate complexity for training age?
```

## Validation Criteria

### Must-Have Checks
✅ All user limitations from knowledge entries honored (NO contraindicated exercises)
✅ Equipment verified available (from preferences)
✅ Exercises appropriate for training age (skill level)
✅ Primary exercises match training goal
✅ Movement patterns balanced (cross-check movement-patterns.md)

### Warning Signs (not failures, but review carefully)
⚠️ High-skill exercises programmed late in session (may compromise technique)
⚠️ New exercises introduced during high-fatigue phase
⚠️ Excessive exercise variety (more than 2-3 new exercises per program)
⚠️ Isolation-heavy program for strength goals (need more compounds)

### Automatic Failures
❌ Exercise contraindicated by user's limitations (injury/movement restriction)
❌ Equipment not available
❌ Exercise too advanced for training age (safety risk)
❌ Movement patterns severely imbalanced

## Cross-Check Points

- **injury-prevention.md** - ALWAYS check before finalizing exercise selection
- **movement-patterns.md** - Ensure balanced stimulus across patterns
- **progression.md** - Consider how exercise progresses over time (some have limited progression potential)
- **recovery-management.md** - More complex exercises require more recovery

## Examples

### Example 1: Strength Goal, Intermediate, Home Gym
**Context**: User wants strength, 2 years training, has barbell/rack/bench/dumbbells

**Selection**:
- Tier 1: Back squat, bench press, deadlift (core strength movements, appropriate skill level, equipment available)
- Tier 2: Romanian deadlift, overhead press, barbell rows (support primary, fill movement gaps)
- Tier 3: Dumbbell lunges, dumbbell chest flyes, bicep curls (accessories with available equipment)
- Tier 4: Face pulls, hip CARs (prehab)

**Validation**:
- ✅ All movements match equipment
- ✅ Appropriate for intermediate (2 years)
- ✅ Strength focus (compound-heavy)
- ✅ Movement patterns covered (squat, hinge, push, pull, unilateral)

### Example 2: Strength Goal with Knee Limitation
**Context**: User wants strength, has "knee-tracking" limitation (knees over toes, avoid narrow stance)

**Selection Modification**:
- Back squat: MODIFIED → Wide stance squat (honors knee tracking)
- Leg press: AVOID → Narrow stance would stress knees
- Goblet squat: MODIFIED → Wide stance if used
- Lunges: REVIEW → May be okay if knee tracks properly (lighter load, cue awareness)

**Validation**:
- ✅ Wide stance prescribed (honors limitation)
- ✅ No narrow-stance movements
- ✅ Lunges included with cueing note

### Example 3: Beginner, Limited Equipment
**Context**: User beginner (3 months training), only has dumbbells and resistance bands

**Selection**:
- Tier 1: Goblet squat (DB), dumbbell bench press, dumbbell Romanian deadlift (simple, stable movements for beginners)
- Tier 2: DB overhead press, DB rows (complete basic patterns)
- Tier 3: DB lunges, DB lateral raises, band pull-aparts (accessories within equipment)
- Tier 4: Band face pulls, bodyweight core (prehab with available equipment)

**Validation**:
- ✅ All movements use available equipment (DB + bands)
- ✅ Simple, beginner-appropriate (no complex barbell movements)
- ✅ Movement patterns covered with equipment constraints
- ✅ No exercises beyond current skill level

### Example 4: Hypertrophy Goal, Advanced
**Context**: User wants muscle growth, 5 years training, full gym access

**Selection**:
- Tier 1: Back squat, incline barbell bench, deadlift (compounds for base stimulus)
- Tier 2: Leg press, dumbbell bench variations, barbell rows (more volume-friendly)
- Tier 3: Leg extensions, leg curls, cable flyes, bicep curls, tricep extensions (isolation for targeted hypertrophy)
- Tier 4: Rotator cuff work, core (prehab)

**Validation**:
- ✅ Mix of compounds + isolation (hypertrophy goal)
- ✅ Advanced variations appropriate (5 years experience)
- ✅ Volume-friendly exercises (machines, dumbbells for accessories)
- ✅ Complete muscle coverage

## Anti-Patterns

❌ **Selecting exercises without checking limitations** - ALWAYS review knowledge entries first
❌ **Assuming equipment availability** - Verify from preferences
❌ **Beginner doing complex Olympic lifts** - Match skill to training age
❌ **Isolation-only program for strength** - Need compounds for strength goals
❌ **Compound-only program for hypertrophy** - Need isolation for complete development
❌ **New exercises every week** - Consistency needed for progression
❌ **Ignoring movement pattern balance** - Creates imbalances and injury risk
❌ **High-skill exercises when fatigued** - Technique breakdown risk

## References

- Schoenfeld et al. 2017 - "Effects of Resistance Training Frequency on Measures of Muscle Hypertrophy" (exercise selection for hypertrophy)
- Suchomel et al. 2018 - "The Importance of Muscular Strength" (exercise selection for strength)
- Haff & Triplett 2016 - "Essentials of Strength Training and Conditioning" (exercise classification, movement patterns)
- McGill 2015 - "Low Back Disorders" (exercise selection for injury prevention)
- Boyle 2016 - "New Functional Training for Sports" (movement pattern balance, exercise progressions)
