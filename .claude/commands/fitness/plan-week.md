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
- **recovery-management.md** - If managing fatigue, deload decision, recovery assessment
- **injury-prevention.md** - If emerging issues, overuse risk, volume adjustments
- **progression.md** - For understanding where in program cycle

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

### Step 5: Critically Evaluate & Score

**Before proposing, score your week against objectives (1-10 scale):**

**Program Alignment (10 = perfect):**
- Does this implement the program's training split correctly?
- Are session frequencies matching program prescription (e.g., 4x strength)?
- Does it respect program's sequencing rules (e.g., 72hr between heavy lower)?
- Score: __/10. If <8, what doesn't match program?

**Adherence (10 = highly likely to complete):**
- Is this realistic given this week's specific constraints (travel, work, etc.)?
- Are sessions scheduled at times user can actually train?
- Does it respect fixed activities (yoga class, climbing partners, etc.)?
- Are backup plans included for likely disruptions?
- Score: __/10. If <8, what reduces completion likelihood?

**Recovery (10 = optimal):**
- Are hard days appropriately spaced?
- Is total hard day count sustainable (not overreaching)?
- If deload week, is volume/intensity reduced per program protocol?
- Are rest days adequate given recent training load (from logs)?
- Score: __/10. If <8, what recovery issues exist?

**Constraint Management (10 = all addressed):**
- Are equipment contexts correctly assigned (office vs home gym)?
- Are injury modifications included where needed?
- Is travel/schedule disruption handled appropriately?
- Score: __/10. If <8, what constraints ignored?

**Overall Score: (sum/4) = __/10**

**If overall score <8.5, iterate on schedule before proposing.** Identify specific weaknesses and refine.

**Common failure modes to check:**
- ❌ Ignores program's rest day requirements
- ❌ Stacks hard sessions back-to-back (overreaching)
- ❌ Schedules training on day user mentioned they can't train
- ❌ Wrong equipment context (programs barbell work at gym that only has DBs)
- ❌ Doesn't account for travel (programs 4 sessions when traveling Thu-Sun)
- ❌ No week goal set (unclear what to accomplish)

**After scoring ≥8.5, proceed to propose.**

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

Reference injury-prevention.md for modification guidance.

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
