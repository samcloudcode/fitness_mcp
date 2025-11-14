# Program Creation

> **⚠️ COMPLEXITY WARNING**
>
> Program creation is the hardest task in fitness coaching. It requires deep analytical thinking, cross-checking multiple data sources (goals, knowledge, preferences, logs), referencing evidence-based protocols, and multi-dimensional validation.
>
> **Expect to iterate.** Your first design will likely score <8.5 and need refinement. This is normal and necessary for quality. Think hard, check thoroughly, and improve until you get it right.

## Background

You are creating a comprehensive training program (1-3 month mesocycle) for a user. Programs are strategic documents showing how all goals fit together and providing the framework to achieve them.

**What a program contains:**
- Goals & priorities with current state and targets
- Training split & frequencies
- Exercise architecture (main/secondary/accessories/mobility)
- Progression framework
- Recovery strategy (deload schedule, hard/easy distribution)
- Constraint management (equipment, injury, schedule)
- Complete rationale

**Program hierarchy:**
- **Program**: Comprehensive strategy for 1-3 months (all frameworks and principles)
- **Week**: 7-day schedule implementing program (when/where for each session)
- **Workout**: Today's session details (exact exercises, sets/reps/weights)

**Storage:**
- Kind: `program`
- Key: Always `current-program` (single living document)
- Content: 400-600 chars with all strategic elements
- Update when strategy changes or becomes stale (3+ months)

---

## Instructions

### Step 1: Extract All Context from MCP Server

**Fetch:** `fitness-mcp:overview(context='planning')`

This returns: goals, program (current if exists), week, plan (recent 5), preferences, knowledge, logs (recent 10)

**Extract and analyze:**

**From Goals:**
- Priorities (p1/p2/p3) → Volume/frequency allocation
- Target metrics → Progression timeline
- Deadlines → Periodization urgency
- Current state → Realistic progress rate

**From Knowledge:**
- Injury history → Exercise modifications, prehab protocols
- Movement limitations → Alternative exercises
- Recovery patterns → Frequency decisions
- Technique proficiency → Exercise complexity

**From Preferences:**
- Equipment access → Exercise selection per day
- Time available → Volume/superset strategy
- Activity preferences → Schedule around fixed activities
- Training style → Exercise selection

**From Logs (recent 10):**
- Current working weights → Starting loads for program
- Volume tolerance → Volume targets
- Exercise responses → Exercise selection
- Frequency patterns → Programming frequency

**From Current Program (if exists):**
- What's working → Keep and build on
- What's not working → Modify or replace
- How long running → Determine if need variation

**CRITICAL:** Extract from ACTUAL data, not assumptions.

### Step 2: Reference Protocols for Domain Expertise

**Protocols provide evidence-based frameworks. Reference them to inform your thinking, not as validation checklists.**

**Check protocol index:** `planning/protocols/INDEX.md` to determine which protocol files to load based on user's goals and constraints.

**Load protocols as needed based on:**
- User's injury history or limitations
- Specific training goals (endurance, strength, etc.)
- Known issues (knee problems, tendon issues, etc.)
- Recovery modalities user employs (ice baths, sauna, etc.)

**Use protocols to:** Understand principles, inform decisions, critically evaluate your plan.

### Step 3: Design Comprehensive Strategy

**Analyze deeply:**
- Where are they NOW? (from logs)
- Where do they want to be? (from goals)
- What's the gap? (realistic progression calculation)
- What are constraints? (from knowledge)
- What are preferences? (from preferences)

**Design comprehensive plan:**
- Volume/frequency allocation (based on priorities and tolerance)
- Exercise architecture (main/secondary/accessories matched to equipment and limitations)
- Periodization timeline (based on deadlines and current state)
- Equipment strategy (which gym when, travel adaptations)
- Progression scheme (from progression.md, matched to training age)
- Constraint protocols (injury rehab, deload schedule)
- Hard/easy distribution (total hard days, sequencing)

### Step 4: Critically Evaluate & Score

**Before proposing, score your program against objectives (1-10 scale):**

**Goal Alignment (10 = perfect):**
- Does this ACTUALLY achieve the p1 goals in the timeline? (realistic progression rate?)
- Are p2/p3 goals appropriately maintained without interfering with p1?
- Score: __/10. If <8, what needs adjustment?

**Safety (10 = fully safe):**
- Does it account for ALL limitations in knowledge entries? (injuries, movement restrictions)
- Are exercise modifications appropriate for constraints?
- Is volume/frequency sustainable for this user's recovery capacity?
- Score: __/10. If <9, what's unsafe?

**Adherence (10 = highly sustainable):**
- Does it fit life constraints? (equipment access, schedule, preferences)
- Is it realistic given work/life/travel patterns?
- Does it align with user's training style preferences?
- Score: __/10. If <8, what reduces adherence?

**Evidence-Based (10 = fully aligned):**
- Does progression scheme match training age (from progression.md)?
- Is volume appropriate per recovery-management.md principles?
- Are exercises selected per exercise-selection.md criteria?
- Score: __/10. If <8, what conflicts with protocols?

**Overall Score: (sum/4) = __/10**

**If overall score <8.5, iterate on design before proposing.** Identify specific weaknesses and refine.

**Common failure modes to check:**
- ❌ Progression too aggressive (unrealistic timeline)
- ❌ Missed injury limitation (unsafe exercise selection)
- ❌ Equipment assumption (user doesn't have access)
- ❌ Ignores schedule constraint (programs Wed when user travels)
- ❌ Volume too high (doesn't match logs' sustainable frequency)

**After scoring ≥8.5, proceed to propose.**

### Step 5: Propose Program

Present comprehensive strategy with:
- Training frequencies and approach
- How it integrates preferences (equipment contexts, fixed activities)
- Main/secondary/accessory breakdown
- Starting weights/loads (from logs)
- Injury prevention protocols
- Progression timeline
- Equipment strategy
- Constraint management
- Complete rationale

**NOT a daily schedule** - that's for week planning.

### Step 6: Get Approval & Save

After approval:

```python
fitness-mcp:upsert(
    kind='program',
    key='current-program',
    content='[comprehensive strategy 400-600 chars with all strategic elements]'
)
```

**After saving:**
- Confirm success
- Summarize key features
- Highlight how limitations addressed
- Suggest next steps

---

## Example: Complete Execution

**User Request:** "Create a 12-week strength program for rugby, training 4x/week"

**Step 1: Extract from overview(context='planning')**

```
# Goals:
"rugby-strength" - increase maximal strength for scrums (p1)
Current: Squat 225x5, Bench 185x5, Deadlift 275x5
Target: Squat 315x5, Bench 225x5, Deadlift 315x5 by April (5 months)

# Knowledge:
"knee-tracking": Knee issues with narrow stance, need wide stance squats
"shoulder-history": Previous impingement, avoid overhead pressing behind neck

# Preferences:
"equipment-home-gym": Barbell, rack, bench, limited dumbbells
"schedule-constraint": Train Mon/Tue/Thu/Sat (work travel Wed/Fri)

# Recent Logs:
Squat 5x5 @ 225lbs RPE 7, Bench 4x8 @ 175lbs RPE 7
Deadlift 3x5 @ 275lbs RPE 8, OHP 3x8 @ 115lbs RPE 7
Volume: 12-15 sets per session, recovery good, training 3x/week currently
```

**Step 2: Reference Protocols**

Check `planning/protocols/INDEX.md`:
- Knee history → Load knee-health-prevention.md (valgus prevention, wide stance)
- Shoulder history → (Note: No shoulder-specific protocol yet, apply general injury prevention principles)
- Progression guidance → (Use knowledge of intermediate progression: weekly linear or wave loading, 2.5-5lb upper / 5-10lb lower)
- Recovery planning → (Apply recovery principles: 4x/week appropriate, deload every 4 weeks, adequate rest days)

**Step 3: Design**

Analysis:
- 225lb → 315lb squat in 5 months = +90lbs = ~4.5lb/week needed
- Currently 3x/week → wants 4x/week (matches schedule Mon/Tue/Thu/Sat)
- 12-week block, intermediate lifter
- MUST: wide stance squats (knee), no behind-neck press (shoulder)

Decisions:
- Upper/Lower split 4x/week (fits schedule, equipment contexts)
- Block periodization: 3 blocks x 4 weeks (hypertrophy → strength → peak)
- Wide stance squats ONLY
- Front OHP only (shoulder safety)
- Wave loading (prevent staleness)
- Deload week 4, 8, 12

**Step 4: Propose**

"Based on your context:

**Training Split:** Upper/Lower 4x/week (Mon/Tue/Thu/Sat matching schedule)
- Mon: Lower (squat focus)
- Tue: Upper (bench/press focus)
- Thu: Lower (deadlift focus)
- Sat: Upper (power/accessories)

**Progression:** 3 blocks to April
- Block 1 (Weeks 1-4): Hypertrophy - 4x8-12 reps
- Block 2 (Weeks 5-8): Strength - 4x5-8 reps
- Block 3 (Weeks 9-12): Peak - 3x3-5 reps
- Deload every 4th week (60% volume)

**Exercise Architecture:**
- Main: Squat (WIDE STANCE), Bench, Deadlift, OHP (front only)
- Secondary: RDL, rows, face pulls (shoulder prehab)
- Accessories: Lunges, DB work, core
- Daily: Hip mobility

**Starting Loads** (from logs):
- Squat: 225→285 by week 12
- Bench: 185→215 by week 12
- Deadlift: 275→335 by week 12

**Safety:**
- Wide stance squats only (knee tracking)
- No behind-neck pressing (shoulder history)
- Face pulls daily (shoulder prehab)

**Why:**
- Rugby April deadline needs strength peak
- Upper/Lower 4x matches Mon/Tue/Thu/Sat schedule
- Block periodization builds foundation → strength → peak
- Addresses knee + shoulder limitations
- Home gym equipment sufficient

Approve to save?"

**Step 5: Save**

```python
upsert(
    kind='program',
    key='current-program',
    content='''12wk strength for rugby (p1): 4x/week upper/lower (Mon/Tue/Thu/Sat).
    Block 1-3 progress 8-12→5-8→3-5 reps. Squat 225→285, bench 185→215, deadlift 275→335.
    Wide stance squats ONLY (knee tracking), front press only (shoulder safety).
    Daily hip mobility, face pulls. Deload week 4,8,12 (60% volume).
    Why: April rugby peak, matches schedule/equipment, addresses knee+shoulder limitations.'''
)
```

---

## Goal-Driven Programming Framework

**Prioritize by p-value:**
- **p1:** Primary focus - most volume, highest frequency, best recovery
- **p2:** Secondary - maintain, don't progress aggressively
- **p3:** Minimal viable dose - don't interfere with p1/p2

**Handling competing p1 goals:**
- Sequential blocks (12 weeks each, alternate focus)
- Concurrent (train both, accept 30% slower progress)
- Redefine priorities (make one p2)

**Deload protocols (from recovery-management.md):**
- When: Every 4-8 weeks scheduled, or reactive
- How: 50% volume OR 50% intensity OR 50% frequency (choose one)
- Why: Dissipates fatigue, maintains neural patterns

---

## Anti-Patterns

❌ Ignoring knowledge entries (injuries/limitations)
❌ Arbitrary loads not from logs
❌ Equipment assumptions
❌ Missing "why" context
❌ No deload strategy
❌ Progression inappropriate for training age
❌ Programming contraindicated exercises
❌ Too verbose (>600 chars) or too vague (<400 chars)

---

## Notes

- Always check knowledge entries for limitations (safety paramount)
- Base loads on recent logs (not arbitrary)
- Reference protocols as expertise sources (not validation gates)
- Think deeply about best approach (no cookie-cutter)
- Get user approval before saving
- Programs are living documents (update when strategy changes)
- Length: 400-600 chars guideline, prioritize completeness over brevity
