# Workout Creation

## Background

You are creating a specific workout plan for a training session. Workouts are executable documents that take the program's comprehensive strategy and apply it to today's specific session with exact exercises, loads, sets, reps, and execution details.

**What a workout contains:**
- Warmup protocols
- Main work (exercises with sets/reps/load/RPE/cues)
- Accessories
- Cooldown
- Progression from last session
- Complete rationale (goal + phase + progression)

**Workout hierarchy:**
- **Program**: Comprehensive strategy for 1-3 months (all frameworks and principles)
- **Week**: 7-day schedule implementing program (when/where for each session)
- **Workout**: Today's session details (exact exercises, sets/reps/weights)

**Storage:**
- Kind: `plan` (before session) or `log` (after completion)
- Key: `YYYY-MM-DD-{type}` (e.g., `2025-10-28-lower`, `2025-10-28-intervals`)
- Content: 400-800 chars with warmup, main, accessories, cooldown, complete why

---

## Instructions

### Step 1: Fetch Context

**Fetch:** `fitness-mcp:overview(context='planning')`

Returns: goals, program (with comprehensive frameworks), week, plan (recent), knowledge, preferences, logs (recent 10)

**NEVER program without reviewing saved context first. Injuries happen from incomplete context.**

**Extract:**

**From Program:**
- Exercise architecture (what movements, intensity ranges)
- Progression scheme (how to progress from last session)
- Current phase (where in periodization cycle)
- Constraint protocols (injury accommodations, equipment per context)

**From Week:**
- Today's session type and focus (e.g., "Lower - Squat focus deload 50% volume")
- Location and equipment context (office vs home gym)

**From Knowledge:**
- ALL injury/limitation entries (CRITICAL - never skip)
- Movement cues and modifications
- Prehab protocols

**From Recent Logs (10-14 days):**
- Last similar session → progression baseline
- Recent performance → loads, RPE, recovery status
- Volume tolerance → session design

### Step 2: Reference Protocols for Domain Expertise

**Protocols provide evidence-based frameworks. Reference them to inform your thinking.**

**Load as needed:**

Refer to [protocols/INDEX.md](../protocols/INDEX.md) for the current list of available protocols. Load relevant protocols based on:

- Exercise selection and tier structure
- Progression calculations (load adjustments from last session, RPE-based progressions)
- Safety checks (injury prevention before programming exercises)
- Within-session movement pattern balance

**Use protocols to:** Understand principles, calculate progressions, check safety.

### Step 3: Extract Program → Today's Executable Plan

**Core principle:** Program contains comprehensive strategy. Extract relevant parts into today's executable session.

**Extraction process:**

1. **Goals & Exercises:**
   - Which goal (p1/p2/p3)?
   - What type from week?
   - Specific movements from program's architecture

2. **Loads & Progression:**
   - Last similar session (from logs)
   - Program's progression method (e.g., "+2.5lb/week")
   - Today's prescription (e.g., last 185lbs RPE 8 + 2.5lb/week = 187.5lbs)

3. **Structure:**
   - Warmup protocols (from program)
   - Main work (from program architecture)
   - Accessories (from program)
   - Cooldown (from program)

4. **Modifications:**
   - Apply program's constraint handling (equipment, injuries, time, fatigue)
   - Check knowledge entries for specific cues

5. **Rationale:**
   - How this serves goals
   - Fits phase (Week X of Y)
   - Progresses from last session

**Reference protocols for:** Load calculation methods, RPE-based adjustments, deload implementation.

### Step 4: Create Plan with Execution Detail

**Great plans coach during the workout. Include:**

**Strategic clarity:**
- Goal connection with current state ("squat-315 p1, currently 225x5")
- Phase context ("Week 4 of 8 hypertrophy block per program")
- Specific progression from last session with numbers

**Tactical precision:**
- Movement cues from knowledge ("chest up, knees track toes")
- Tempo where relevant ("2sec eccentric, explode up")
- RPE calibration ("RPE 8 = bar speed consistent + 2 reps left")
- Rest activities - **BE SPECIFIC** with exact exercises:
  - During upper work: Lower mobility ("hip 90/90 stretches during bench rest", "ankle mobility between press sets")
  - During lower work: Upper mobility ("band pull-aparts between squats", "dead hangs during RDL rest")
  - Principle: Use antagonist/complementary body regions for efficiency + active recovery
  - Name specific exercises, not generic "mobility" - makes them actionable
- Contingencies ("knee pain → swap Bulgarian for goblet squat")

**Priority in 400-800 char limit:**
1. Main work detail (cues, tempo, RPE, progression) - highest priority
2. Rest period utilization (efficiency + recovery)
3. Key accessories with purpose
4. Complete why (goal + phase + progression from last session)
5. Contingencies for known constraints

**Reference protocols for:** Exercise tier structure, equipment substitutions, training age appropriateness, contraindications, modification decision trees, prehab protocols.

### Step 5: Validate with Plan-Validator Agent

**Use the plan-validator agent to critically review your workout draft:**

Use the Task tool to call the plan-validator agent with your drafted workout. The agent will:
- Cross-reference against user's goals, knowledge entries (injuries/limitations), recent logs, and current program
- Check for safety issues, inappropriate progression, and goal/phase alignment
- Verify loads are traceable to recent logs (not arbitrary)
- Check execution detail is sufficient (cues, tempo, contingencies)
- Ensure week focus is properly implemented (e.g., deload volume actually reduced)

**Pass to the agent:**
- The complete workout draft you've designed
- Context: "This is a workout plan proposal for [date]. Please validate against the user's context and recent training."

**Review the validation report and address:**
- **Critical issues** (must fix before proceeding - especially safety concerns)
- **Important considerations** (should address - progression, execution detail)
- **Suggestions** (incorporate if they improve the plan)

**Iterate on your workout based on the validation feedback until the agent assessment is "Pass with modifications" or "Approved as-is".**

### Step 6: Propose → Approve → Save

Present workout with complete rationale.

After approval:

```python
fitness-mcp:upsert(
    kind='plan',
    key='YYYY-MM-DD-{type}',
    content='[warmup + main + accessories + cooldown + why, 400-800 chars]'
)
```

**After session completion, log actual performance:**

```python
fitness-mcp:upsert(
    kind='log',
    key='YYYY-MM-DD-{type}',
    content='{Type} ({duration}): {actual exercises/sets/reps/loads/RPE}, {how it felt, deviations}'
)
```

---

## Example: Complete Execution

**User Request:** "What should I do for my lower body session today?"

**Step 1: Fetch from overview(context='planning')**

```
# Program:
"12wk strength: 4x/week upper/lower. Block 2 strength (5-8 reps).
Squat (wide stance), RDL, Bulgarian split. Daily hip mobility."

# Week:
"2025-week-44: Mon Lower - Squat focus (week 4 deload - 60% volume)"

# Knowledge:
"knee-tracking": Keep knees over toes, wide stance
"shoulder-history": No behind-neck pressing (not relevant for lower)

# Recent Logs:
Last Monday (week ago): Squat 5x5 @ 225lbs RPE 7, RDL 3x8 @ 185lbs RPE 6
Last Thu: Deadlift 3x5 @ 275lbs RPE 7
Overall: Good recovery, no issues
```

**Step 2: Reference Protocols**

- Reviewed protocols/INDEX.md and loaded relevant protocols:
- Progression → Deload = 60% volume (keep intensity, reduce sets 5→3)
- Injury prevention → Wide stance squats for knee tracking
- Exercise selection → Tier structure (main/secondary/accessories)

**Step 3: Extract → Today**

Analysis:
- Week says: "Squat focus deload 60% volume"
- Program says: "Wide stance squats, daily hip mobility"
- Last squat session: 5x5 @ 225lbs RPE 7
- Deload: 60% volume = 3x5 instead of 5x5, same load (225lbs), reduce RPE target (6-7 vs 8)

Design:
- Warmup: Hip mobility per program (knee health)
- Main: Squat 3x5 @ 225 (deload: same load, less volume, focus technique)
- Secondary: RDL 2x8 @ 185 (reduced from 3x8, maintain hip hinge pattern)
- Accessories: Light unilateral, no additional load (deload week)
- Cooldown: Stretch

**Step 4: Create Plan**

```
Session: Lower - Squat focus (deload week - 60% volume)
Date: 2025-10-28 (Monday, Week 4 of program)

Warmup: Hip CARs 2x5 each direction (knee health per knowledge), bodyweight squats 2x10 wide stance, bar squat 1x10, 135x5, 185x3, 225x1.

Main: Back Squat 3x5 @ 225lbs wide stance RPE 6-7 (deload from 5x5, same load, reduced volume. Cues: chest up, knees track toes per knowledge, 2sec eccentric, explode up. Focus technique over intensity. Band pull-aparts + dead hang 30sec during 3min rest for upper mobility).

RDL 2x8 @ 185lbs RPE 5-6 (deload from 3x8, maintain hip hinge. Stretch bottom, squeeze glutes top).

Walking lunges 2x12 each leg @ bodyweight (light unilateral, no added load on deload. Control eccentric, quad-glute connection).

Cooldown: Hip flexor/quad stretch, foam roll IT band.

Contingency: Knee pain → swap lunges for goblet squat.

Why: Week 4 deload per program (60% volume). Maintained loads from last week (squat 225, RDL 185), reduced sets. Wide stance squats honor knee tracking requirement. Focus movement quality over volume. Building squat-315 goal (currently 225x5).
```

**Step 5: Propose & Save**

"Based on your program and week plan:

**Lower Deload - Monday**

Today is week 4 deload (60% volume per program). Maintaining your loads from last week but reducing sets:
- Squat: 3x5 @ 225lbs (vs normal 5x5) - wide stance for knee health
- RDL: 2x8 @ 185lbs (vs normal 3x8)
- Lunges: 2x12 bodyweight only

Focus on movement quality and technique. Hip mobility warmup + upper body mobility during squat rest periods (band pull-aparts, dead hangs).

Approve to save?"

After approval:

```python
upsert(
    kind='plan',
    key='2025-10-28-lower',
    content='''6am Home Lower (squat-315 p1, deload). Warmup: Hip CARs 2x5, goblet squat 2x10. Main: Back squat 3x5 @ 225 wide stance RPE 6-7 (deload from 5x5, cues: chest up, knees track toes, 2sec eccentric - band pull-aparts + dead hang 30sec rest periods for upper mobility). RDL 2x8 @ 185 RPE 5-6. Walking lunges 2x12 BW (control eccentric). Cooldown: Hip/quad stretch, foam roll. Contingency: Knee pain → goblet squat. Why: Week 4 deload (60% volume), same loads, reduced sets, technique focus.'''
)
```

**After completion, user says:** "Done! Squat felt great, 3x5 @ 225 RPE 6. RDL 2x8 @ 185. Lunges 2x12. 55min total."

```python
upsert(
    kind='log',
    key='2025-10-28-lower',
    content='Lower deload (55min): Back squat 3x5 @ 225lbs RPE 6 (wide stance, felt smooth), RDL 2x8 @ 185lbs RPE 6, walking lunges 2x12 BW. Knee stable, no pain. Good deload - fresh and recovered.'
)
```

---

## Common Workout Types

### Resistance Training

- Warmup: Joint mobility, dynamic stretches, specific warmup sets
- Main: Compound movements (squat, bench, deadlift, press)
- Secondary: Variations and volume work (RDL, rows, incline)
- Accessories: Isolation and prehab (curls, face pulls, core)
- Cooldown: Static stretching, foam rolling

### Intervals/Cardio

- Warmup: Easy pace, dynamic drills
- Main: Interval structure (e.g., 6x800m @ target pace, recovery periods)
- RPE/HR calibration
- Cooldown: Easy pace, walking

### Skills Practice (Climbing, Sport-Specific)

- Warmup: Movement-specific prep
- Technique drills
- Main work (skill practice, bouldering, sport movement)
- Cooldown: Stretch, mobility

---

## Anti-Patterns

❌ Generic exercises without loads ("squats" not "squat 5x5 @ 225lbs")
❌ Arbitrary loads (not based on recent logs)
❌ Ignoring limitations (programming contraindicated exercises)
❌ No progression from last session (stagnation)
❌ Excessive progression (>5-10% load increase)
❌ Session doesn't match week's focus
❌ Sets/reps don't match program phase
❌ Missing warmup for injury-prone areas

---

## Workout Plan Quality Checklist

Before finalizing, verify the workout artifact contains:

- [ ] Warmup protocols specified (joint mobility, dynamic work, specific warmup sets)
- [ ] Main work includes: exercises, sets, reps, load, RPE, tempo/cues
- [ ] Loads traceable to recent logs (specific progression from last session)
- [ ] Progression rate appropriate (<5-10% load increase)
- [ ] ALL injury limitations respected (no contraindicated exercises)
- [ ] Movement cues from knowledge entries included
- [ ] RPE calibration clear (e.g., "RPE 8 = 2 reps left")
- [ ] Rest period activities specified with exact exercises (e.g., "band pull-aparts during squats" not just "mobility")
- [ ] Accessories with purpose stated
- [ ] Cooldown included (stretching, foam rolling)
- [ ] Session matches week focus (if week says "deload", workout reflects it)
- [ ] Rep ranges match program phase (hypertrophy/strength/peak)
- [ ] Contingencies for known constraints (e.g., "knee pain → swap to...")
- [ ] Complete "why" (goal + phase + progression explanation)
- [ ] (if applicable) Multi-modal ordering: skill→strength→endurance
- [ ] Content length 400-800 chars

---

## Notes

- Always fetch context before programming (NEVER skip)
- Propose → approve → save (unless user provides completed workout to log)
- Program has strategy - you apply it to today's context
- Load protocols for calculation frameworks, injury prevention, exercise selection
- Safety first - check ALL knowledge entries
- Length: 400-800 chars with complete execution detail
- Log after completion (actual performance, how it felt)
