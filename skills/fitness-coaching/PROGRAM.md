# Program Creation

**Load this file when:** Creating or updating the overall training program strategy.

**This file contains:**
- Data-driven workflow extracting from overview context
- p1/p2/p3 priority-based programming framework
- Activity integration strategies (scheduling around preferences)
- Examples showing overview → program derivation

---

## What is a Program?

**The self-aware strategic document** showing how all goals fit together and the comprehensive framework to achieve them. Contains everything needed to plan weeks and create workouts. Single living document updated when strategy changes or becomes stale (3+ months).

**Timeframe:** 1-3 months (can reference longer-term progression but focus on current mesocycle)

**Hierarchy:**
- **Program** (this file): Comprehensive strategy - exercise types, mobility protocols, recovery approach, sequencing rules, rationale
- **Week** (WEEK.md): This week's specific schedule derived from program strategy, travel/life adaptations
- **Workout** (WORKOUT.md): Today's session details - exact exercises, sets/reps/weights within program framework

**Template:**
```
fitness-mcp:upsert(
    kind='program',
    key='current-program',
    content='As of {Month Year}: {comprehensive strategic content - see required elements below}'
)
```

**Key:** Always `current-program` (update replaces)

**Required Strategic Elements (comprehensive):**

1. **Goals & Priorities**: Which goals (p1/p2/p3), current state, targets, deadlines, why this priority order
2. **Training Split & Frequencies**: Sessions per modality with contexts (e.g., "4x strength: upper Mon/Thu @ office, lower Tue/Fri @ home")
3. **Exercise Architecture**:
   - Main lifts (movements, intensity/rep ranges, specific exercises if constraint-driven)
   - Secondary work (volume focus, examples)
   - Accessories (isolation, prehab, specific protocols)
4. **Mobility & Prehab**:
   - Daily protocols (e.g., "knee protocol 10min AM: backward sled, Nordics, tibialis - why: knee injury history")
   - Integrated mobility (e.g., "hip work during squat rest - accumulate 60min/week")
   - Stretching targets (e.g., "hip ER for yoga lotus goal")
5. **Recovery Strategy**:
   - Deload schedule (every X weeks, method)
   - Hard/easy distribution (total hard days, sequencing)
   - Sleep/nutrition if critical constraint
6. **Progression Framework**:
   - Current phase (hypertrophy/strength/peak week X of Y)
   - Rep/set schemes per phase
   - How to progress (e.g., "add 2.5lb/week bench, 5lb/week squat")
   - Timeline milestones
7. **Activity Integration**:
   - Fixed activities (yoga, MTB, climbing - when, with whom, non-negotiable)
   - How they fit (recovery aid vs interference source)
   - Scheduling rules
8. **Constraint Management**:
   - Injury accommodations (what to avoid, what to emphasize)
   - Equipment per context (office DBs only, home full rack)
   - Travel adaptations
   - Time constraints
9. **Sequencing & Interference**:
   - Separation rules (e.g., "6hr minimum heavy lower → hard cardio")
   - Antagonist balance (e.g., "push:pull 1:1 for shoulder health")
   - Fatigue management between sessions
10. **Rationale & Why**:
    - Why this approach for these goals
    - How modalities combine/interact
    - Trade-offs accepted (e.g., "concurrent = slower gains but maintains both p1 goals")
    - What makes this sustainable for this person

**Length:** As comprehensive as needed (600-1500 chars typical). Quality over brevity - the program must contain complete strategic information for downstream week/workout planning.

---

## Knowledge Files Reference

Load these when relevant to user's context (Step 2):

- **KNEE-HEALTH.md**: Mechanisms and principles for knee health programming (VMO stabilization, eccentric loading, tissue adaptation, modification decision trees)

---

## Program Creation Workflow

### Step 1: Extract All Context from Overview

**PRIMARY DATA SOURCE:** `fitness-mcp:overview(context='planning')`

This returns: goals, program (current), week, plan (recent 5), preferences, knowledge, logs (recent 10)

**What to extract and how it informs programming (adapt to actual data):**

**From Goals** - Check actual priorities, targets, deadlines, current state:
- Priorities (p1/p2/p3) → Determines volume/frequency allocation
- Target metrics (e.g., "bench-225", "sub-20-5K") → Sets progression timeline
- Deadlines → Determines periodization urgency
- Current state → Calculates realistic progress rate

**From Preferences** - Check actual equipment, time, activities, style:
- Equipment access (e.g., "office gym Mon/Fri, home Tue/Sat") → Exercise selection per day
- Time available (e.g., "45min sessions") → Volume/superset strategy
- Activity preferences (e.g., "yoga Sundays 90min", "MTB Saturdays") → Schedule around fixed activities
- Training style (e.g., "prefer DB over barbell", "hate burpees") → Exercise selection

**From Knowledge** - Check actual injury history, limitations, recovery patterns, proficiency:
- Injury history (e.g., "knee pain in deep squat eccentric") → Exercise modifications, prehab protocols
- Movement limitations (e.g., "can't overhead press pain-free") → Alternative exercises
- Recovery patterns (e.g., "need 72hr between heavy lower days") → Frequency decisions
- Technique proficiency (e.g., "comfortable with Olympic lifts") → Exercise complexity

**From Recent Logs (10 sessions)** - Check actual weights, volume responses, exercise responses, frequency patterns:
- Current working weights (e.g., "Squat 5x5 @ 265lbs last week") → Starting loads for program
- Volume tolerance (e.g., "completed 20 sets chest, felt great" vs "18 sets back, very sore") → Volume targets
- Exercise responses (e.g., "RDL aggravates hamstring" vs "Single-leg RDL feels great") → Exercise selection
- Frequency patterns (e.g., "4x/week sustainable" vs "3x/week better") → Programming frequency

**From Current Program (if exists)** - Check actual performance and feedback:
- What's working → Keep and build on
- What's not working → Modify or replace
- How long running → Determine if need variation
- Staleness → If 3+ months, refresh approach

**IMPORTANT:** These are example patterns. Always extract from ACTUAL data in overview, not assumptions. User's context may be completely different (e.g., climbing focus, yoga preference, home gym only, injury rehab, etc.).

### Step 2: Think Deeply to Optimize for Goals Based on Priority

**This is where coaching expertise matters most. Think critically about the best path forward, prioritizing higher-priority goals while maintaining lower-priority ones.**

**Process:**
1. **Load relevant knowledge files** based on goals and context:
   - Injury/limitation mentioned? Load relevant knowledge file (e.g., KNEE-HEALTH.md)
   - Specific training goal? Load relevant expertise (e.g., periodization, exercise selection)
   - Activity focus? Load domain knowledge (e.g., climbing, running, concurrent training)

2. **Analyze current status deeply:**
   - Where are they NOW? (from logs - actual weights, volumes, frequencies working)
   - Where do they want to be? (from goals - targets, deadlines, priorities)
   - What's the gap? (realistic progression rate calculation)
   - What are constraints? (from knowledge - injuries, limitations, recovery patterns)
   - What are preferences? (from preferences - equipment, time, activities, style)

3. **Design comprehensive plan** using frameworks below:
   - Volume/frequency allocation (based on priorities and tolerance from logs)
   - Exercise architecture (main/secondary/accessories matched to equipment and limitations)
   - Periodization timeline (based on goals' deadlines and current state)
   - Equipment strategy (which gym when, travel adaptations)
   - Efficiency approach (session duration, supersets, mobility integration)
   - Hard/easy distribution (total hard days, sequencing, concurrent management)
   - Constraint protocols (injury rehab, deload schedule, recovery patterns)

4. **Critically evaluate your plan:**
   - Does this ACTUALLY get them to their goals in the timeline? (realistic?)
   - Does it account for ALL limitations mentioned in knowledge? (safe?)
   - Does it fit their life constraints from preferences? (sustainable?)
   - Where can it be improved? (better exercise selection, smarter sequencing?)

5. **Refine and improve:**
   - Adjust based on critical evaluation
   - Optimize for adherence 
   - Balance ambition with sustainability 

**Key principle:** Maximize efficiency to achieve goals within constraints and preferences. Use ACTUAL data from overview - their logs show what works, their knowledge shows limitations to respect, their preferences show what they'll actually sustain. The best program is one they'll follow. 

### Step 3: Propose Program

Present strategy with:
- **Training frequencies and approach** (e.g., "3x upper, 2x lower, combine mobility with strength when possible, variety conditioning daily")
- **How it integrates preferences** (yoga, MTB, climbing, fixed activities - schedule around these)
- **Main/secondary/accessory breakdown** derived from logs (what exercises, volume ranges)
- **Starting weights/loads** based on recent performance (actual numbers from logs)
- **Injury prevention protocols** based on knowledge entries (daily prehab, modifications, what to avoid)
- **Progression timeline** toward goals (1-3 month focus, which phase of periodization)
- **Equipment strategy** (which gym for which work, travel adaptations)
- **Efficiency approach** (session duration norms, when to superset, mobility integration)
- **Hard/easy distribution** (total hard days, how to sequence)
- **Constraint management** (deload schedule, known travel, injury protocols)

**Not prescriptive daily schedule** - that's for WEEK.md. Program says "3x upper, 2x mobility" not "Mon upper, Tue mobility".

### Step 4: Ask Clarifying Questions (Only If Critical Gaps)

**MINIMIZE QUESTIONS.** Only ask if:
- Overview context has conflicting info (e.g., goal says "squat 315" but no recent squat logs)
- Critical detail missing that fundamentally changes program (e.g., injury mentioned but no pain location/severity)
- Need to choose between two valid approaches (e.g., two p1 goals competing, need priority decision)

**Question format (if needed):**
"[Data from overview] - [specific gap] - [how it changes program] - [2 options based on answer]"

Example: "Your logs show squat 5x5 @ 265 but goal is 315 by June (3 months, need +50lbs = 17lb/month, very aggressive). Should we extend timeline to 5 months (realistic) or keep 3-month target (will require perfect execution, may need adjustment)?"

### Step 5: Get Approval & Save

Refine based on feedback, then save with `fitness-mcp:upsert(kind='program', key='current-program', content='...')`

---

## Program Design Framework

### Goal-Driven Programming

**Prioritize by p-value:**
- **p1 goals:** Primary focus - most volume, highest frequency, best recovery
- **p2 goals:** Secondary - maintain, don't progress aggressively
- **p3 goals:** Minimal viable dose - don't interfere with p1/p2

**Example:**
- p1-bench-225 → Strength 4x/week (primary)
- p2-5k-sub20 → Running 3x/week maintenance (secondary)
- p1-pain-free-squat → Daily mobility (injury prevention)

**Handling Multiple p1 Goals:**
If two p1 goals compete (e.g., squat-315 + sub-20-5K):
- **Option 1:** Sequential blocks - 12 weeks squat focus (running maintenance), then 12 weeks running focus (strength maintenance)
- **Option 2:** Concurrent - Train both, accept 30% slower progress on each due to interference
- **Option 3:** Redefine priorities - Make one p1, other p2 (clearer focus, faster progress on true priority)

### Deload Protocols

**When:** Every 4-8 weeks scheduled, or reactive (strength regressing, persistent soreness, sleep disruption)

**How (choose ONE):**
- 50% volume (keep intensity, reduce sets: 5→2-3)
- 50% intensity (keep volume, reduce load: 80%→60%)
- 50% frequency (keep session work, train 2x instead of 4x)

**Why:** Dissipates fatigue while maintaining neural patterns. Often leads to PRs after deload week.

---

## Efficiency Techniques

**Rest-Period Mobility Integration:**

Embed mobility during rest WITHOUT compromising performance:
- Upper session rest → lower body mobility (hips, hamstrings, ankles)
- Lower session rest → upper body mobility (shoulders, t-spine, wrists)
- Long rests (4-5min) → 2-3min mobility
- Result: 15min mobility per workout = 60min/week accumulated

**Superset Strategies:**

When: Antagonist pairs (push/pull), non-competing muscle groups, time-constrained sessions
How: Add 30s to normal rest, monitor performance
Never: Main lifts (compromises adaptation)
Result: 15-20min time savings per session

---

## Program Examples

### Example 1: Diverse Activities (Yoga + MTB + VO2 Max)

**OVERVIEW CONTEXT:**
- Goals: p1-vo2-52 (currently 45, target 52 by Feb), p2-maintain-strength (squat 225x5, bench 185x5)
- Preferences: Yoga Sundays 9am (non-negotiable, social), MTB Saturdays (1-2hr with friends), prefer morning workouts
- Knowledge: No injuries, high recovery capacity
- Recent logs: Running 3x/week 25-30min easy, strength 2x/week sustainable

**COMPREHENSIVE PROGRAM:**
```
As of Nov 2025: VO2 max improvement primary (p1, currently 45 ml/kg/min → target 52 by Feb, 12 weeks). Running 3x/week: 2 hard interval sessions (Tue/Fri), 1 easy Zone 2 (Wed), MTB Saturdays (fun cardio, don't structure). Strength maintenance secondary (p2, preserve muscle) 2x/week full-body Mon/Thu (squat 225x5, bench 185x5, deadlift 275x5 - maintain these loads, no progression). Yoga Sundays 9am local studio with friends (non-negotiable social, aids recovery).

EXERCISE ARCHITECTURE:
- Main lifts (maintenance): Squat 3x5 @ 225, Bench 3x5 @ 185, Deadlift 3x5 @ 275, OHP 3x6 @ 115 (compound focus, no progression)
- Secondary: RDL 3x8, Pull-ups 3x8, Rows 3x8 (volume work)
- Accessories: Face pulls 3x15, Bulgarian split 3x8/leg, Core 3x30s (injury prevention, balance)
- Intervals: 5x4min @ 95% max HR, 3min recovery (VO2 stimulus, primary adaptation)

MOBILITY & PREHAB:
- No daily protocols needed (no injury history)
- Hip mobility 2x/week during strength rest (maintain flexibility for MTB/yoga)
- Yoga Sundays serves mobility needs (90min comprehensive)

RECOVERY:
- Deload every 4 weeks (50% volume: strength 2x5 instead of 3x5, intervals 3x3min instead of 5x4min)
- Total hard days = 4/week (2 intervals Tue/Fri + 2 strength Mon/Thu)
- Easy days: Wed easy run, Sat MTB easy-moderate, Sun yoga (recovery)
- Sleep/nutrition: No constraints noted

PROGRESSION (12 weeks to Feb):
- Weeks 1-4: Build VO2 tolerance (4x3min → 5x4min), strength maintain
- Weeks 5-8: VO2 volume peak (5x4min), strength maintain
- Weeks 9-11: VO2 intensity peak (6x4min or 4x5min), strength reduce to 1x/week
- Week 12: Taper (2x3min easy), test VO2 max

ACTIVITY INTEGRATION:
- Yoga Sundays 9am: Scheduled around (social commitment), aids recovery, meets mobility needs
- MTB Saturdays: After Fri intervals (legs need easy day), social rides with friends, don't add structure
- Morning preference: Strength 7am Mon/Thu, intervals 6:30am Tue/Fri, easy run 6:30am Wed

SEQUENCING & INTERFERENCE:
- Hard interval Fri → easy MTB Sat (24hr recovery, no leg interference)
- Strength Mon/Thu separated by 72hr (adequate recovery for maintenance)
- Easy run Wed between Tue interval and Thu strength (active recovery)
- No heavy lower before hard cardio (both use legs minimally at maintenance intensity)

RATIONALE:
- VO2 p1 needs 2-3 hard interval sessions + easy aerobic base (80/20 principle)
- Strength p2 gets 2x/week maintenance (sufficient to preserve muscle per research, allows VO2 focus)
- Yoga/MTB are fixed social activities → schedule training around them (sustainable > optimal)
- Total 4 hard days manageable with high recovery capacity (from knowledge)
- Trade-off: Not building strength, but maintaining both p1/p2 goals without interference
```

### Example 2: Zero Questions Asked - Complete Derivation from Overview

**OVERVIEW CONTEXT:**
- Goals: p1-bench-225 (currently 185x5, June deadline = 5mo), p2-sub-21-5K (currently 22:30, maintain)
- Preferences: Office gym Mon/Wed (DBs to 75lbs, cables), Home gym Fri/Sat (full rack), 60min max, 6am workouts, Yoga Sundays 8am with partner (non-negotiable)
- Knowledge: Rotator cuff strain 2024 (healed, avoid behind-neck press, face pulls mandatory), need 72hr between heavy lower, no Olympic lift experience
- Recent logs: Bench 4x8 @ 175lbs RPE 7, Squat 4x6 @ 245lbs, Deadlift 3x5 @ 295lbs RPE 9 (too heavy), Running 3x/week 25min, 4x/week pattern working

**COMPREHENSIVE PROGRAM (zero questions asked, all from overview):**
```
As of Jan 2025: Bench-225 primary goal (p1, currently 185x5 → target 225x1 by June, 20 weeks = 2lb/week realistic). Strength 4x/week upper/lower split. Running secondary (p2, maintain sub-21 5K) 3x/week easy 25min Zone 2. Yoga Sundays 8am with partner (90min, non-negotiable). Shoulder prehab daily 5min (rotator cuff strain 2024 healed, face pulls mandatory prevention). Equipment: Office gym Mon/Wed (DBs to 75lbs, cables - upper days), Home gym Fri/Sat (full rack - lower days + Sat upper). 60min sessions @ 6am (from preferences).

EXERCISE ARCHITECTURE:
- Main lifts: Bench 5x5 (DB @ office, BB @ home), Squat 4x5 @ 250 (home only, barbell), Deadlift 3x4 @ 285 (home, reduced from 295 - was RPE 9), OHP variations (landmine @ office safer, BB @ home)
- Secondary: Incline DB 3x10, Front squat 3x6, RDL 3x8 (no Olympic lifts - no experience per knowledge), Cable rows 3x10
- Accessories: Bulgarian split 3x8/leg, Leg curl 3x12, Tricep 3x12, Bicep 3x10
- Prehab: Face pulls 3x20 daily (shoulder health mandatory), Band pull-aparts 3x20 (push:pull balance)

MOBILITY & PREHAB:
- Daily shoulder protocol 5min: Face pulls 3x20, band pull-aparts 3x20 (rotator cuff history, non-negotiable)
- Integrated mobility: T-spine during upper rest, hip/ankle during lower rest (accumulate 45min/week)
- Yoga Sundays: 90min comprehensive mobility (meets flexibility needs)
- Avoid: Behind-neck press (shoulder constraint from knowledge)

RECOVERY:
- Deload every 4 weeks (50% volume: bench 3x5 instead of 5x5, squat 2x5 instead of 4x5)
- Total hard days = 4/week (all strength sessions, no hard cardio)
- Easy days: Tue/Thu easy runs, Sat walk, Sun yoga
- Lower body 72hr minimum (knowledge): Fri squat → Mon next week = 72hr
- Sleep/nutrition: 60min time constraint requires efficiency (superset accessories)

PROGRESSION (20 weeks to June, strength phase):
- Current: Week 1 of strength block (5x5 bench @ 180lb, 4x5 squat @ 250lb, 3x4 deadlift @ 285lb)
- Bench: Add 2.5lb/week (180→195 weeks 1-8, 195→210 weeks 9-16, 210→220 weeks 17-19)
- Squat: Add 5lb/week (250→290 weeks 1-8, maintain weeks 9-20 to prioritize bench p1)
- Deadlift: Add 5lb/week cautiously (start 285, was 295 RPE 9 - too heavy per logs)
- Week 20: Taper, test bench 1RM (target 225+)
- Rep scheme: 5x5 throughout (no phase changes, linear progression)

ACTIVITY INTEGRATION:
- Yoga Sundays 8am: With partner (social non-negotiable per preferences), serves mobility, schedule training Mon-Sat around this
- Running 3x/week: Tue/Thu between strength days (active recovery), Sat after lower + upper (combined session)
- Equipment contexts: Office Mon/Wed lunchtime (fixed schedule), Home Fri/Sat anytime

SEQUENCING & INTERFERENCE:
- Upper Mon @ office (DB bench) → Lower Fri @ home (squat - 96hr recovery, more than 72hr minimum)
- Upper Wed @ office (DB OHP) → Upper Sat @ home (bench barbell - 72hr, fresh for heavy)
- Lower Fri → Lower Mon next week = 72hr minimum (knowledge constraint)
- Antagonist balance: Push:pull 1:1 minimum (face pulls daily prevents shoulder issues)
- Running easy only (p2 maintenance, doesn't interfere with strength p1)

CONSTRAINT MANAGEMENT:
- Shoulder: Rotator cuff history → face pulls daily mandatory, avoid behind-neck press, landmine press safer than BB OHP
- Equipment: Office DBs only (75lb max) → limits upper loads, use BB bench @ home Sat for heavier work
- Equipment: Home has full rack → all barbell lower work here (Fri/Sat), squat/deadlift not possible at office
- Time: 60min max sessions → superset accessories (tricep + bicep, leg curl + calf), prioritize compounds
- No Olympic experience: Use RDL instead of cleans, focus barbell basics

RATIONALE:
- Bench p1: 4x upper sessions (2 DB @ office, 2 BB @ home) provides frequency for strength gains, 2lb/week realistic over 20 weeks
- Squat: Progressing weeks 1-8 then maintaining (focus bench p1, squat secondary importance)
- Running p2: 3x/week easy sufficient to maintain sub-21 fitness without interfering (from logs)
- Equipment split necessary: Office only DBs (Mon/Wed lunch), home full rack (Fri/Sat flexible)
- Shoulder prehab non-negotiable: History of injury, daily prevention better than reactive treatment
- 72hr lower: Knowledge says need this, schedule respects constraint (Fri → Mon+)
- Yoga social: Partner commitment, Sunday fixed, training adapts around life
- Trade-offs: Office DB limits upper loads (75lb/hand vs 180lb barbell), but frequency compensates
```

---

## Program Staleness & Updates

**Check "As of" date:** Stale if 3+ months old

**Update when:** Goals changed, strategy not working, life change (schedule/equipment/injury), approaching 3 months

**Update process:** Note staleness → check goal changes → propose updated program → get approval → save (same key = replaces)
