# Workout Creation

**Load this file when:** Client asks for a workout or you need to create a plan for a specific training session.

**This file contains:**
- Workout design workflow
- How to extract program strategy into today's session
- Workout types beyond resistance training
- Knowledge file integration
- Plan templates and examples

---

## Workout Design Workflow

When client asks for a workout:

**Fetch context first**: `fitness-mcp:overview(context='planning')` - gets goals, program, week, knowledge, recent logs (2 weeks). Check program/week are current (load PROGRAM.md or WEEK.md if stale or needing updates).

**Extract program → today**: Use program's comprehensive frameworks to design today's session. See "Creating Today's Plan" below. Load knowledge files if program mentions constraints (knee, shoulder, concurrent training).

**Propose → approve → save**: Present workout with complete rationale (goal connection, phase context, progression from last session). Refine based on feedback. **Only save after approval** → `fitness-mcp:upsert(kind='plan', key='YYYY-MM-DD-{type}', ...)`.

**After completion**: Log what actually happened → `fitness-mcp:upsert(kind='log', key='YYYY-MM-DD-{type}', content='...')`. Same key updates existing log if user provides info incrementally during session.

---

## Data Fetching Rules (Safety First)

**NEVER program a workout without reviewing saved context first.**

### ALWAYS Fetch Before Programming:
- **Use `fitness-mcp:overview(context='planning')` first** - Gets everything in one call (goals, program, week, plan, knowledge, recent logs)
- **If needed, fetch full details:** `fitness-mcp:get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])` for truncated content
- **Recent training:** Already in planning context (2 weeks of logs)
- **Current program:** Already in planning context
- **Preferences:** Already in planning context

### Only Fetch More If:
- User asks for specific analysis ("show me my bench progress over 3 months")
- Investigating patterns requiring deeper history

**Better to over-fetch and be thorough than miss critical limitations. Injuries happen from incomplete context.**

---

## Creating Today's Plan from Program Strategy

**Core principle**: Program contains comprehensive strategy (600-1500 chars). Extract relevant parts into today's executable session (400-800 chars).

### Extraction Process

**From program → today's plan:**
1. **Goals & exercises**: Which goal (p1/p2/p3), what type (from week), specific movements from program's architecture
2. **Loads & progression**: Last session + program's method → today's prescription (e.g., last 185lbs RPE 8 + 2.5lb/week method = 187.5lbs)
3. **Structure**: Warmup protocols, main work, accessories, cooldown (all from program)
4. **Modifications**: Apply program's constraint handling (equipment, injuries, time, fatigue, sequencing)
5. **Rationale**: How this serves goals, fits phase (Week X of Y), progresses from last session

**From recent logs → progression:**
- Last similar session → progress appropriately (weight, reps, RPE)
- Example: "Last lower: Squat 205×5 RPE 8 → Today: 210×5 RPE 8 (+5lb per program)"

### Execution Details for Great Plans

Plans should coach during the workout, not just list exercises. Include:

**Strategic clarity:**
- Goal connection with current state ("squat-315 p1, currently 225×5")
- Phase context ("Week 4 of 8 hypertrophy block per program")
- Specific progression from last session with numbers

**Tactical precision:**
- **Movement cues**: Form priorities from knowledge ("chest up, knees track toes per knowledge")
- **Tempo**: Where relevant ("2sec eccentric, explode up")
- **RPE calibration**: What it means today ("RPE 8 = bar speed consistent + 2 reps left")
- **Rest activities**: Mobility/antagonist work ("hip 90/90 stretches during 3min rest", "band pull-aparts rest periods")
- **Contingencies**: Known issues ("knee pain → swap Bulgarian for goblet squat")

**Priority in 400-800 char limit:**
1. Main work detail (cues, tempo, RPE, progression) - highest priority
2. Rest period utilization (efficiency + recovery)
3. Key accessories with purpose (not just exercise names)
4. Complete why (goal + phase + progression from last session)
5. Contingencies for known constraints

---

## Knowledge File Integration

**When program references specific constraints or protocols, load relevant knowledge files for mechanisms and principles.**

**Example - KNEE-HEALTH.md**: If program mentions knee protocol or knee injury history, load for understanding VMO stabilization, eccentric loading, tissue adaptation principles, modification decision trees, motor learning cues. Extract relevant principles and apply to user's specific context.

**How to use knowledge files:**
1. Check user's specific `knowledge` entries first (from overview) - their individual responses and constraints
2. If program references domain-specific protocols → load relevant knowledge file
3. Extract mechanisms and principles (don't copy protocols verbatim)
4. Apply principles to user's specific context (their knowledge + program strategy)

**Knowledge files provide expert mechanisms - user knowledge provides individual responses - program provides strategy.**

---

## Plan Template & Examples

**Key format:** `YYYY-MM-DD-{type}` (e.g., `2025-11-09-lower`, `2025-11-09-intervals`)

**Content structure:** `[Time/Location] {Type}: Warmup: {protocols}. Main: {exercises with sets×reps @ load RPE, cues, rest activities}. Accessories: {exercises}. Cooldown: {stretching}. Why: {goal + phase + progression}.`

**Length:** 400-800 chars. See examples below for execution detail density.

---

### Example 1: Lower Strength - Complete Execution Detail (761 chars)

```
fitness-mcp:upsert(
    kind='plan',
    key='2025-11-09-lower',
    content='6am Home Gym Lower (squat-315 p1). Warmup: Knee protocol 10min per program (slow eccentric step-downs 2×15, terminal knee ext 2×20 per knowledge), goblet squats 2×10, hip 90/90 stretches. Main: Back squat 5×5 @ 210lbs RPE 8 (last lower 205×5 RPE 8, +5lb per program progression) - cues: chest up, knees track toes per knowledge, 2sec eccentric, explode up, RPE 8 = bar speed consistent + 2 reps left - hip 90/90 mobility 3min rest. RDL 4×8 @ 160lbs RPE 7 (stretch bottom, squeeze glutes top) - band pull-aparts rest periods. Bulgarian split 3×8/leg @ 35lbs (knee stability per knowledge, control eccentric, quad-glute connection). Leg curl 3×12, calf 3×15. Cooldown: Hip flexor/quad stretch, foam roll IT band. Contingency: Knee pain → swap Bulgarian for goblet squat. Why: Week 4 of 8 hypertrophy block per program. Building squat-315 (currently 225×5). Last lower progressed clean, continue +5lb. Knee protocol maintains patellar tracking.'
)
```

### Example 2: Interval Run - Intensity Calibration & Progression (598 chars)

```
fitness-mcp:upsert(
    kind='plan',
    key='2025-11-09-intervals',
    content='6am Track Intervals (sub-20-5k p1). Warmup: 10min easy, dynamic drills per program (leg swings, high knees, butt kicks). Main: 6×800m @ 3:45/km (last week 5×800m @ 3:50/km RPE 8, progressed volume+pace per program), target HR 175-180, RPE 8-9, 2min jog recovery. RPE calibration: RPE 8 = hard but sustainable, breathing heavy, could hold 2 more intervals. If HR >185 or form breaks → extend recovery 2:30min. First 3 intervals build rhythm, last 3 test fitness. Cooldown: 10min easy, walking. Why: Week 5 of 12 VO2max block per program. Building sub-20-5k (current 21:15). Last week 5×800 felt controlled RPE 8, ready for +1 interval + pace drop per program method. Hard session 2 of 3 this week per program distribution.'
)
```


---

## Logging Completed Workouts

After the workout is done, log what actually happened.

**Log Template:**
```
fitness-mcp:upsert(
    kind='log',
    key='YYYY-MM-DD-{type}',
    content='{Type} ({duration}): {Exercise 1 sets×reps @ load RPE}, {Exercise 2...}. {Optional: how it felt, deviations, notes}.'
)
```

**Content**: Session type, duration, actual exercises/sets/reps/loads/RPE, deviations from plan, how it felt

**Length**: As detailed as provided. Comprehensive logs enable better progression tracking.

**Workflow**:
- User provides completed info → Save immediately
- Build incrementally → Same key updates existing log (add exercises as completed)

**Examples:**
```
Lower (62min): Back squat 4×10 @ 205lbs RPE 8, RDL 3×10 @ 155lbs RPE 7, Bulgarian split 3×8/leg @ 30lbs RPE 8, leg curls 3×12, calf raises 3×15. Knee felt stable, no pain. Good pump.

Intervals (48min): 5×4min @ 16.5 km/h, avg HR 175. First 3 reps RPE 8, last 2 reps RPE 9. Completed all, good recovery between. Legs tired from morning squat but manageable.

Climbing (75min): Warmup 4 routes V0-V2. Flagging drills V3-V4 20min (much better hand positioning). V6 project 6 burns, sent! Crimps felt strong. Shoulder prehab done, no pain.
```

---

## Quick Reference

**Workflow**: Fetch context (`overview(context='planning')`) → Check program/week current → Extract program → today → Propose → Approve → Save → Guide → Log after completion

**Key reminders:**
- **Propose → approve → save** (never save before approval, UNLESS user provides completed workout info to log)
- **Program has the strategy** - you apply it to today's context (location, time, fatigue, progression)
- **Load knowledge files** for mechanisms when program references constraints
- **Safety first** - always fetch context before programming
- **Broad scope** - resistance training, cardio, skills practice, mobility, sport-specific sessions
- **Length** - 400-800 chars with warmup, main, accessories, cooldown, complete why
