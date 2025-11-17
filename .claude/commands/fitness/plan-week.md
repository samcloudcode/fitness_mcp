# Week Planning

## Background

You are creating a 7-day training schedule for a user. Weeks are scheduling documents that implement the program strategy within real-world constraints and maximize adherence.

**What a week contains:**
- Daily schedule (type + location + time + session focus/target)
- Week goal (what to accomplish this 7 days)
- Deviations from normal program (travel, constraints, adaptations)
- Rationale for adjustments

**Week hierarchy:**
- **Program**: Comprehensive strategy for 1-3 months (all frameworks and principles)
- **Week**: 7-day schedule implementing program (when/where for each session)
- **Workout**: Today's session details (exact exercises, sets/reps/weights)

**Session focus/target** (derived from program):
- Strength: "bench 5x5 focus" or "deload 50% volume"
- Cardio: "VO2 intervals 5x4min" or "easy Z2"
- Activity: "yoga recovery" or "MTB easy ride"
- NOT exact weights (those go in workout)

**Storage:**
- Kind: `week`
- Key: ISO week format `YYYY-week-NN` (week 01-53)
- Content: 200-600 chars (complex weeks with constraints need more)

---

## Instructions

### Step 1: Review Program Strategy

**Fetch:** `fitness-mcp:overview(context='planning')`

Returns: goals, program (with all frameworks), week (current), plan (recent), knowledge, preferences, logs (recent)

**Extract from program:**
- Training frequencies (4x strength, 3x cardio, etc.)
- Split structure (upper/lower, full-body, etc.)
- Equipment context (which gym which days)
- Hard/easy distribution (total hard days per week)
- Special protocols (daily prehab, deload schedule)
- Known constraints (travel weeks, injury protocols)

**If program stale (3+ months) or doesn't match goals:** Update program first using create-program.md instructions.

### Step 2: Identify This Week's Constraints

**Check recent logs and conversation BEFORE asking:**
- User may have mentioned: "Traveling Thu-Sat" or "Work deadline" or "Knee hurting"
- Recent logs may show: Missed sessions, lower RPE, pain notes
- Program may already note: Travel weeks, deload schedule, injury protocols

**Only ask if:**
1. Creating first-ever week (no pattern)
2. Significant change from last week (missed 3+ sessions, injury mentioned)
3. Genuinely unclear

**Brief check (if needed):** "Creating week plan. Any travel, schedule conflicts, or recovery concerns this week?"

**Common constraints:**
- Travel (which days? equipment available?)
- Work stress (deadline week? lighter volume?)
- Recovery status (run down? extra rest?)
- Schedule conflicts (meetings, social events?)
- Equipment changes (gym closed? traveling?)
- Injury/pain (flare-up? modifications?)

**Default if no constraints:** Normal week following program.

### Step 3: Map Program to 7 Days

**Assign when/where for each session:**

From program frequencies:
- Which days for which types? (Mon/Tue/Thu/Fri strength, Wed/Sat/Sun cardio)
- Match equipment availability (office Mon/Wed, home Tue/Sat)
- Match schedule (prefer AM, meetings Wed)
- Apply hard/easy distribution (don't stack hard sessions)

**Schedule around fixed activities:**
- Yoga class Sundays 9am
- Climbing Tue/Thu 6pm
- Work meetings Wed AM

**Result:** 7-day calendar with type/location/time/focus for each day.

**Reference protocols for guidance (not validation):**

Refer to [protocols/INDEX.md](../protocols/INDEX.md) for the current list of available protocols. Load relevant protocols based on:

- Managing fatigue, deload decisions, recovery assessment
- Emerging issues, overuse risk, volume adjustments
- Understanding where in program cycle

### Step 4: Set Week Goal & Plan for Adherence

**Week goal examples:**
- "Week 3 of strength block - hit all 4 sessions at prescribed loads"
- "Travel week - maintain 3x training despite hotel gym"
- "Deload - dissipate fatigue, maintain movement patterns"

**Maximize completion likelihood:**
- Hard sessions on days with best recovery
- Consistent times (habit building)
- Specific times ("Mon 6am" not "Mon morning")
- Backup options if miss session

### Step 5: Validate with Plan-Validator Agent

**Use the plan-validator agent to critically review your week schedule draft:**

Use the Task tool to call the plan-validator agent with your drafted week schedule. The agent will:
- Cross-reference against user's current program, knowledge entries (injuries/limitations), recent logs, and preferences
- Check for program alignment (frequencies, split, sequencing rules)
- Verify adherence feasibility (realistic given constraints, fixed activities respected)
- Assess recovery adequacy (hard session spacing, deload implementation, rest days)
- Validate constraint management (equipment contexts, travel, injury modifications)

**Pass to the agent:**
- The complete week schedule draft you've designed
- Context: "This is a week plan proposal for week [YYYY-week-NN]. Please validate against the user's program and current context."

**Review the validation report and address:**
- **Critical issues** (must fix before proceeding - overreaching, missed constraints)
- **Important considerations** (should address - sequencing, equipment contexts)
- **Suggestions** (incorporate if they improve adherence or recovery)

**Iterate on your week schedule based on the validation feedback until the agent assessment is "Pass with modifications" or "Approved as-is".**

### Step 6: Propose & Save

Present 7-day schedule with:
- What each day (type + location + time + focus)
- Week goal
- Adjustments from program
- How managing constraints

After approval:

```python
fitness-mcp:upsert(
    kind='week',
    key='YYYY-week-NN',
    content='Mon: ... Week goal: ... Why: ...'
)
```

---

## Week Scheduling Considerations

**These are factors to consider when mapping program to 7 days, not rigid rules.**

### Recovery & Sequencing (If Program Allows Flexibility)

**Consider:**
- How many hard days total? (program may specify or be flexible)
- How to space similar sessions? (program may require 72hr lower→lower)
- Which days hard vs easy? (some programs specify, others flexible)
- Interference between modalities? (follow program guidance)

**Examples of program-driven decisions:**
- Program: "72hr minimum between heavy lower days" → Week: Tue lower → Fri lower minimum
- Program: "Separate hard cardio from heavy legs by 6hr" → Week schedules accordingly
- Program flexible → Week optimizes for adherence

### Timing & Adherence

**Consider what increases completion likelihood:**
- Consistent times (6am daily vs varying)
- Before obligations (AM before work)
- Around fixed activities (schedule training around non-negotiables)
- Specific accountability ("Mon 6am" not "Mon morning")

**Program doesn't dictate timing - this is personal adherence.**

### Equipment Context

**Program already specifies equipment strategy - week implements it:**
- Program: "Office Mon/Wed (DBs only), Home Tue/Fri (full rack)"
- Week: Maps to actual locations/days

---

## Same-Day Session Sequencing

**When combining multiple modalities same day, use this ordering to maximize quality and minimize injury risk:**

**Optimal order:** Skill/Power → Strength → Endurance

**Rationale:**
1. **Skill/Power work first** (plyometrics, Olympic lifts, sprints, handstands, technical drills)
   - Requires maximum CNS freshness and neuromuscular coordination
   - Speed/power output degrades rapidly with fatigue
   - Injury risk increases if attempted when tired (landing mechanics breakdown, form deteriorates)
   - Examples: Box jumps, sprint drills, muscle-up practice, handstand work

2. **Strength second** (heavy compounds, hypertrophy work)
   - Still needs neuromuscular capacity for safe heavy loading
   - Pre-fatigue from skill work minimal (neural, not metabolic exhaustion)
   - Can handle moderate fatigue better than power work
   - Examples: Squats, deadlifts, bench press, weighted pull-ups

3. **Endurance last** (cardio, conditioning, metabolic work)
   - Performance minimally affected by pre-fatigue (can run tired, can't safely max squat tired)
   - Acts as "metabolic finisher" - already fatigued, so cardio effort feels appropriate
   - Lowest injury risk when fatigued (vs explosive/heavy movements)
   - Examples: Runs, cycling, rowing intervals, conditioning circuits

**Same-day intensity management:**
- **Both HARD → Avoid if possible** (risk overreaching, reduce second session quality)
- **One HARD + one EASY → OK** (e.g., heavy squats + easy Z2 jog 15min, OR easy strength + hard intervals)
- **Both MODERATE → OK if total <90min** and adequate fueling/recovery

**Separation minimum:**
- If same session (back-to-back): Use ordering above, keep one modality easy
- If same day separated: 6-8 hours minimum between hard sessions

**Reference:** Load relevant protocols from [protocols/INDEX.md](../protocols/INDEX.md) for detailed interference effects and session spacing strategies.

---

## Week Structure Templates

**Common training frequencies with example day assignments:**

### 4-Day Template (Most Common)

**Upper/Lower Split:**
- Mon: Lower
- Tue: Upper
- Wed: OFF or easy cardio/mobility
- Thu: Lower
- Fri: Upper
- Sat: Long endurance or OFF
- Sun: OFF or active recovery

**Full-Body + Endurance:**
- Mon: Full-body strength
- Tue: Intervals/HIIT
- Wed: OFF
- Thu: Full-body strength
- Fri: Long easy cardio
- Sat: Full-body strength or skill work
- Sun: OFF

**When to use:** Time-constrained, general fitness, maintenance phases

---

### 5-Day Template

**Hybrid (Strength + Endurance):**
- Mon: Lower strength
- Tue: Upper strength
- Wed: Endurance (intervals)
- Thu: Lower strength
- Fri: Upper strength
- Sat: Long endurance
- Sun: OFF or mobility

**Push/Pull/Legs + Cardio:**
- Mon: Push (chest/shoulders/triceps)
- Tue: Easy cardio
- Wed: Pull (back/biceps)
- Thu: Intervals/HIIT
- Fri: Legs
- Sat: Long cardio or skill work
- Sun: OFF

**When to use:** Balanced strength + endurance goals, most hybrid athletes

---

### 6-Day Template (High Volume)

**Upper/Lower + Endurance:**
- Mon: Lower strength
- Tue: Endurance (intervals)
- Wed: Upper strength
- Thu: Endurance (easy/long)
- Fri: Lower strength
- Sat: Upper strength + skill work
- Sun: OFF or active recovery

**Body Part Split + Cardio:**
- Mon: Chest/Triceps
- Tue: Back/Biceps
- Wed: Endurance
- Thu: Shoulders/Arms
- Fri: Legs
- Sat: Full-body or weak points
- Sun: Long endurance

**When to use:** Competitive athletes, bodybuilding+endurance, high work capacity

---

### Template Selection Criteria

**Choose based on:**
- **Time availability:** 4-day if <5 hrs/week, 5-day if 5-7 hrs/week, 6-day if 7+ hrs/week
- **Recovery capacity:** Older athletes (40+) often better with 4-5 days, younger can handle 6
- **Goals:** Strength-primary → 4-day with 2-3 cardio, Endurance-primary → 5-6 day with 3-4 cardio
- **Lifestyle:** Irregular schedule → 4-day easier to maintain, consistent schedule → 5-6 day manageable

**Adaptation:**
- Templates are starting points - adjust to program's specific requirements
- Program dictates frequencies (e.g., "4x strength, 3x endurance") - template shows how to schedule it
- Week applies template to actual calendar constraints (travel, work, fixed activities)

---

## 6-Workout Cycle Alternative (Flexible Rotation)

**Andy Galpin's unstructured approach for irregular schedules:**

**Concept:**
- Instead of rigid weekly schedule (Mon = legs, Tue = upper, etc.), create a SEQUENCE of workouts
- Rotate through sequence regardless of calendar - if you miss a day, just do next workout in cycle whenever you can train

**Example 6-workout cycle:**
1. Heavy strength (squat focus)
2. HIIT cardio (VO2 intervals)
3. Mobility/skill (yoga, handstands)
4. Moderate strength (upper body hypertrophy)
5. Long endurance (easy run/ride 60-90min)
6. Cross-training fun (MTB, swim, sport)

**How it works:**
- Monday: Do workout #1 (heavy strength)
- Tuesday: Busy, skip training
- Wednesday: Do workout #2 (HIIT) - pickup where left off
- Thursday: Do workout #3 (mobility)
- Friday: Travel, skip
- Saturday: Do workout #4 (upper body) - continue sequence
- Sunday: Do workout #5 (long run)
- Next Monday: Do workout #6 (cross-training), then cycle restarts at #1

**Benefits:**
- Accommodates irregular schedules without feeling "behind"
- Still hits all training elements in proper rotation
- Reduces stress about "missing leg day" - you'll do it next time you train
- Maintains variety and progression through cycle

**When to use:**
- Irregular work schedule (shift work, travel, on-call)
- Life chaos periods (young kids, moving, major projects)
- Prefer flexibility over structure
- Still want comprehensive training (all modalities) without rigid calendar

**Design your cycle:**
- Include all modalities program requires (strength sessions, cardio types, mobility, skills)
- Order logically (avoid back-to-back very hard sessions if training consecutive days)
- Typical cycle length: 6-8 workouts (completes every 6-12 days depending on frequency)
- Mark completed workouts to track position in cycle

**Trade-off:**
- PRO: Maximum flexibility, never "behind schedule"
- CON: Less structured progression tracking (weeks in program become fuzzy)
- Best for: General fitness, maintenance phases, life chaos periods
- Avoid for: Competition prep, specific event training (those need calendar structure)

---

## Examples

### Example 1: Standard Week

**Context from overview:**
- Program: 4x upper/lower, office Mon/Thu, home Tue/Fri
- No travel, Week 4 of strength block

```
2025-week-43:
Mon: Upper @ Office 6am - bench 5x5 focus, rows 4x8.
Tue: Lower @ Home 6am - squat 4x5 focus, RDL 3x8.
Wed: Easy run 6:30am - Z2 30min.
Thu: Upper @ Office 6am - OHP 4x6 focus, pull-ups 3x8.
Fri: Lower @ Home 6am - deadlift 3x4 focus, Bulgarian split 3x8.
Sat: Tempo run 7am - 4mi @ threshold.
Sun: Long run 7am - 60min easy.

Week goal: Complete Week 4 of strength block at prescribed loads (bench 185, squat 250, deadlift 285).
Why: Normal schedule, no travel, good recovery. Standard split.
```

### Example 2: Travel Week

**Context:**
- Program: Same 4x upper/lower
- User mentioned "Conference Thu-Sat"
- Program has travel protocol (reduce volume 20-30%)

```
2025-week-44:
Mon: Upper @ Office 6am - bench 5x5, rows 4x8 (full).
Tue: Lower @ Home 6am - squat 4x5, RDL 3x8 (full).
Wed: Easy run 6:30am + prep/pack.
Thu: OFF (flight, travel).
Fri: Hotel bodyweight 7am 30min - push-ups 3x15, inverted rows, pistol progression (reduced per travel protocol).
Sat: Easy run 3mi - easy pace, jet lag recovery.
Sun: Return + full-body @ Home 9am - squat 3x5, bench 3x5, rows 3x8 (catch-up).

Week goal: Maintain 3x strength (Mon/Tue/Sun) despite Thu-Sat travel - adherence over perfection.
Why: Conference Thu-Sat, hotel gym limited. Travel protocol: reduce volume 20-30%, maintain frequency.
```

### Example 3: Deload Week

**Context:**
- Program: Deload week 4 (50% volume)
- Week 4 of current block

```
2025-week-45:
Mon: Light upper @ Office 6am 40min - bench 3x5 @ 180lb (vs 5x5 @ 185), rows 3x8 (50% volume deload).
Tue: Easy run 3mi Z2.
Wed: Light lower @ Home 6am 40min - squat 2x5 @ 250lb (vs 4x5), RDL 2x8 (50% volume deload).
Thu: OFF (extra rest).
Fri: Easy run 3mi Z2.
Sat: Mobility 30min - hip/shoulder work.
Sun: OFF (extra rest).

Week goal: Dissipate fatigue from 4-week block, maintain movement patterns at same intensity but 50% volume.
Why: Deload per program schedule. 50% volume method - keep intensity, reduce sets.
```

### Example 4: Reactive Adaptation

**Scenario A - Work stress:**

User: "Huge deadline Mon-Wed"

```
2025-week-46:
Mon: Upper @ Office 6am 45min IF TIME - bench 4x5 (reduced from 5x5), skip accessories.
Tue: Easy walk 20min (sleep priority).
Wed: OFF (deadline).
Thu: Lower @ Home 6am IF RECOVERED - squat 3x5, RDL 2x8.
Fri: Easy run 3mi.
Sat/Sun: Flexible.

Week goal: Maintain 2-3x strength minimum, prioritize sleep.
Why: Deadline Mon-Wed. Reduce volume 20%, sleep priority. Lower bar = higher adherence.
```

**Scenario B - Knee pain:**

User: "Knee twinge Tuesday, didn't train Wed"

Reference relevant protocols from [protocols/INDEX.md](../protocols/INDEX.md) for modification guidance.

```
2025-week-48:
Daily: Knee protocol 2x/day 15min - backward sled, Nordics, tibialis (increased for rehab).

Mon: Upper @ Office - bench 5x5, rows 4x8, OHP 3x8 (unaffected, full).
Tue: Modified lower @ Home - box squat to parallel 4x5 (no deep), RDL 3x8, leg curls.
Wed: Easy bike 20min (low-impact).
Thu: Upper @ Office (full).
Fri: OFF (extra knee rest).
Sat: Upper @ Home (extra volume vs missing second lower).
Sun: Assess + mobility.

Week goal: 3x upper (full), 1x modified lower, daily knee protocol 2x, NO pain aggravation.
Why: Knee twinge. Modify not skip, focus what CAN do, increase prehab.
```

---

## Week Updates Mid-Week

**When plans change:** Same key replaces old version.

**Update when:** Unexpected travel, injury, sick.

**Pattern:** Mark completed (✓), show changes, revise goal, explain why.

Example:
```
2025-week-47 UPDATED Wed:
Mon: Upper @ Office ✓.
Tue: OFF (sick).
Wed: Still sick, OFF.
Thu: Easy walk IF better.
Fri: Light upper 40min IF recovered.
Sat: Lower IF fully recovered.
Sun: Easy run or OFF.

Week goal REVISED: Recover from illness, maintain 1-2x light strength if possible.
Why: Got sick Tue night. Rest > pushing through.
```

---

## Week Schedule Quality Checklist

Before finalizing, verify the week artifact contains:

- [ ] All 7 days specified with session type/location/time/focus
- [ ] Session types match program frequencies (e.g., 4x strength sessions)
- [ ] Equipment contexts correct (office Mon/Wed, home Tue/Thu, etc.)
- [ ] Hard sessions appropriately spaced per program requirements
- [ ] Fixed activities respected (yoga class, climbing partners, meetings)
- [ ] Week goal clearly stated (what to accomplish this 7 days)
- [ ] Deviations from normal program explained (travel, fatigue, constraints)
- [ ] Session focuses derived from program (e.g., "bench 5x5 focus", "deload 50% volume")
- [ ] Specific times, not vague ("Mon 6am" not "Mon morning")
- [ ] (if applicable) Backup options for likely disruptions
- [ ] (if applicable) Modifications for injury/pain noted
- [ ] Content length 200-600 chars

---

## Quick Reference

**Week planning is about:**
1. When: Map program to 7 days
2. Where: Assign gym/location from program equipment contexts
3. What: This week's goal
4. How: Maximize adherence despite constraints

**Not about:**
- Exercise selection (in program)
- Sets/reps/loads (in program & workout)
- Training principles (in program)

**Process:**
1. Review program from overview
2. Identify constraints (check logs/context first)
3. Map to 7 days (when/where, session focus from program)
4. Set week goal
5. Plan for adherence
6. Propose → approve → save

**Remember:** Week schedules and keeps you on track. Program has execution details. Workout applies details to today.
