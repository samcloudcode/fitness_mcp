# Week Planning

**Load this file when:** Creating or updating weekly training schedule, client asks "what's coming up?", or adjusting for constraints.

**This file is about:** Scheduling and adherence - when to do what based on constraints and timing to maximize adherence to the program.

---

## What is a Week?

The 7-day schedule showing when to do what, this week's goals, and how to stay on track despite constraints.

**Timeframe:** 7 days (specific ISO week)

**Hierarchy:**
- **Program** (PROGRAM.md): Comprehensive playbook - all details, principles, approaches for 1-3 months
- **Week** (this file): Scheduling & adherence - when to do what this week, goals for the week
- **Workout** (WORKOUT.md): Execute from program - apply program details to today's session

**Template:**
```
fitness-mcp:upsert(
    kind='week',
    key='2025-week-43',
    content='Mon: {type} @ {location} {time} - {focus/target}. Tue: {type} @ {location} {time} - {focus/target}. [continue for all 7 days]. Week goal: {what to accomplish}. Why: {adjustments for constraints}.'
)
```

**Key:** ISO week format `YYYY-week-NN` (week 01 through 53)

**Content must include:**
- **Daily schedule**: Type + location + time + **session focus/target** (what to accomplish this session, derived from program)
- **Week goal**: What to accomplish this 7 days (progression milestone, adherence target, recovery goal)
- **Deviations**: Any changes from normal program (travel, constraints, adaptations)
- **Rationale**: Why adjustments make sense

**Session focus/target** (derived from program, details in workout):
- Strength: "bench 5x5 focus" or "lower volume week 3" or "deload 50% volume"
- Cardio: "VO2 intervals 5x4min" or "easy Z2" or "tempo @ threshold"
- Activity: "yoga recovery" or "MTB easy ride"
- NOT exact weights (those go in workout)

**Length:** 200-600 chars (complex weeks with constraints need more explanation)

---

## Week Planning Workflow

### Step 1: Review Program

**PRIMARY DATA SOURCE:** `fitness-mcp:overview(context='planning')`

Returns: goals, program (with all execution frameworks), week (current), logs (recent)

**Extract from program:**
- Training frequencies (4x strength, 3x cardio, etc.)
- Split structure (upper/lower, full-body, etc.)
- Equipment context (which gym which days)
- Hard/easy distribution (total hard days per week)
- Special protocols (daily prehab, deload schedule)
- Known constraints (travel weeks, injury protocols)

**If program stale (3+ months) or doesn't match goals:**
→ Load PROGRAM.md to update comprehensive playbook first

### Step 2: Identify This Week's Constraints (Start with Context First)

**Check recent logs and conversation for constraints BEFORE asking:**
- User may have already mentioned: "I'm traveling Thu-Sat" or "Work deadline this week" or "Knee hurting"
- Recent logs may show: Missed sessions (indicates stress/time), lower RPE (indicates recovery issues), pain notes
- Program may already note: Known travel weeks, deload schedule, injury protocols

**Only ask about constraints if:**
1. Creating first-ever week (no pattern established)
2. Significant change from last week (missed 3+ sessions, injury mentioned)
3. Genuinely unclear (logs look normal, no constraints mentioned, but unsure)

**Brief constraint check (if needed):**
"Creating week plan. Any travel, schedule conflicts, or recovery concerns this week?" (One question, not interrogation)

**Common constraints to check in context:**
- Travel (which days? what equipment available?)
- Work stress (high deadline week? need lighter volume?)
- Recovery status (feeling run down? need extra rest?)
- Schedule conflicts (meetings, social events, fixed activities?)
- Equipment changes (gym closed? traveling? home only?)
- Injury/pain (flare-up? need modifications?)

**Default assumption if no constraints mentioned:** Normal week following program schedule

### Step 3: Map Program to 7 Days

**Assign when to do what:**

From program frequencies (e.g., "4x strength, 3x cardio"):
- Which 4 days for strength? (Mon/Tue/Thu/Fri)
- Which 3 days for cardio? (Wed/Sat/Sun)
- Match to equipment availability (office Mon/Wed, home Tue/Sat)
- Match to schedule (prefer AM workouts, meetings Wed)
- Apply hard/easy distribution (separate hard sessions, don't stack)

**Schedule around fixed activities:**
- Yoga class Sundays 9am → program rest or before/after
- Climbing with partners Tue/Thu 6pm → non-negotiable
- Work meetings Wed AM → can't train AM that day

**Result:** 7-day calendar with type/location for each day

### Step 4: Set Week Goal

**What should be accomplished this week?**

Examples:
- "Week 3 of strength block - hit all 4 sessions at prescribed loads"
- "Travel week - maintain 3x training despite hotel gym limitations"
- "Deload - dissipate fatigue, maintain movement patterns"
- "Peak week - taper volume, stay fresh for Saturday race"

Week goal answers: What matters most this 7 days?

### Step 5: Plan for Adherence

**Maximize likelihood of completing the week:**

- Put hard sessions on days with best sleep/recovery
- Schedule workouts at consistent times (habit building)
- Pack gym bag night before if AM workout
- Set specific times ("Mon 6am" not "Mon morning")
- Plan meals around training (protein after strength)
- Identify backup options if miss a session (make up Sat vs skip entirely)

**Common adherence obstacles:**
- Travel: Pack bands, research hotel gym, accept volume reduction
- Stress: Lower bar (3 sessions OK vs 4), prioritize sleep
- Time: Use time-constrained templates from program (40min vs 60min)
- Motivation: Focus on showing up (movement > perfection)

### Step 6: Propose & Save

Present 7-day schedule with:
- What each day (strength/cardio/rest + location)
- Week goal (what to accomplish)
- Adjustments from normal program
- How managing constraints for adherence

Get approval, then save:
```
fitness-mcp:upsert(kind='week', key='YYYY-week-NN', content='Mon:... Week goal:... Why:...')
```

---

## Week Scheduling Considerations

**These are factors to consider when mapping program to 7 days, not rigid rules. The program defines the strategy - week planning implements it for this specific week.**

### Recovery & Sequencing (If Program Allows Flexibility)

**Consider:**
- How many hard days total? (program may specify, e.g., "4 hard days max" or be flexible)
- How to space similar sessions? (program may require 72hr lower→lower, or allow back-to-back)
- Which days are hard vs easy? (some programs specify, others leave flexible)
- Interference between modalities? (program handles this - follow its guidance)

**Examples of program-driven decisions:**
- Program says "72hr minimum between heavy lower days" → Week must respect this (Tue lower → Fri lower minimum)
- Program says "separate hard cardio from heavy legs by 6hr" → Week schedules accordingly
- Program says "4x strength, 3x cardio, 4 hard days total" → Week maps to specific days
- Program flexible on exact days → Week optimizes for adherence (early week when fresh, etc.)

### Timing & Adherence (Personal Optimization)

**Consider what increases likelihood of completing the week:**
- **Consistent times:** Habit building (6am daily vs varying) - but flexibility OK if needed
- **Before obligations:** AM before work often fewer conflicts - but PM works if that's your preference
- **Fixed activities:** Schedule around non-negotiables first (yoga class, climbing partners)
- **Specific times:** "Mon 6am" more accountable than "Mon morning" - but adjust for life

**Program doesn't dictate timing - this is about personal adherence.**

### Equipment Context (From Program)

**Program already specifies equipment strategy - week implements it:**
- Program says "Office Mon/Wed (DBs only), Home Tue/Fri (full rack)" → Week follows exactly
- Program says "Heavy compounds need barbell" → Week schedules where barbell available
- Program gives travel adaptations → Week applies them when traveling

**Week doesn't decide equipment strategy - just maps program's strategy to actual locations/days.**

---

## Week Examples (Scheduling & Adherence Focus)

### Example 1: Standard Week (No Constraints)

```
2025-week-43:
Mon: Upper @ Office 6am - bench 5x5 focus, rows 4x8. Tue: Lower @ Home 6am - squat 4x5 focus, RDL 3x8. Wed: Easy run 6:30am - Z2 30min. Thu: Upper @ Office 6am - OHP 4x6 focus, pull-ups 3x8. Fri: Lower @ Home 6am - deadlift 3x4 focus, Bulgarian split 3x8. Sat: Tempo run 7am - 4mi @ threshold. Sun: Long run 7am - 60min easy. Week goal: Complete Week 4 of strength block at prescribed loads (bench 185, squat 250, deadlift 285). Why: Normal schedule, no travel, good recovery. Standard split following program.
```

### Example 2: Travel Week (Thu-Sat Disrupted)

```
2025-week-44:
Mon: Upper @ Office 6am - bench 5x5, rows 4x8 (full session). Tue: Lower @ Home 6am - squat 4x5, RDL 3x8 (full session). Wed: Easy run 6:30am Z2 + prep/pack for travel. Thu: OFF (flight, travel day). Fri: Hotel bodyweight 7am 30min - push-ups 3x15, inverted rows, pistol progression (reduced volume per program travel protocol). Sat: Easy run 3mi - easy pace, unfamiliar area (jet lag recovery). Sun: Return + full-body @ Home 9am - squat 3x5, bench 3x5, rows 3x8 (catch-up session hits main lifts). Week goal: Maintain 3x strength (Mon/Tue/Sun) despite Thu-Sat travel - adherence over perfection. Why: Conference Thu-Sat, hotel gym limited. Following program's travel constraint management (reduce volume 20-30%, maintain frequency). Sun catch-up before resume normal Mon.
```

### Example 3: Deload Week

```
2025-week-45:
Mon: Light upper @ Office 6am 40min - bench 3x5 @ 180lb (vs normal 5x5 @ 185), rows 3x8 (50% volume deload). Tue: Easy run 3mi Z2. Wed: Light lower @ Home 6am 40min - squat 2x5 @ 250lb (vs normal 4x5), RDL 2x8 (50% volume deload). Thu: OFF (extra rest). Fri: Easy run 3mi Z2. Sat: Mobility 30min - hip/shoulder work. Sun: OFF (extra rest). Week goal: Dissipate fatigue from 4-week block, maintain movement patterns at same intensity but 50% volume, arrive fresh for Week 1 of next block. Why: Deload per program schedule (every 4 weeks). Following program's deload protocol (50% volume method - keep intensity, reduce sets). Extra rest days (Thu/Sun).
```

### Example 4: Reactive Adaptation (Stress/Illness/Injury)

**Pattern:** Modify not skip, focus what works, lower bar when needed

**Scenario A - High work stress:**
```
2025-week-46:
Mon: Upper @ Office 6am 45min - bench 4x5 (reduced from 5x5), rows 3x8, skip accessories (time/fatigue). Tue: Easy walk 20min (instead of lower - sleep priority). Wed: OFF (deadline crunch). Thu: Lower @ Home 6am IF RECOVERED - squat 3x5, RDL 2x8. Fri: Easy run 3mi. Sat/Sun: Flexible based on recovery. Week goal: Maintain 2-3x strength minimum, prioritize sleep over hitting all sessions. Why: Work deadline Mon-Wed. Following program stress protocol (reduce volume 20%, sleep priority). Lower bar = higher adherence.
```

**Scenario B - Illness (got sick mid-week):**
```
2025-week-47 UPDATED Wed:
Mon: Upper @ Office ✓. Tue: OFF (sick). Wed: Still sick, OFF. Thu: Easy walk IF feeling better. Fri: Light upper 40min IF recovered (3x5 bench, skip accessories). Sat: Lower IF fully recovered. Sun: Easy run or OFF. Week goal REVISED: Recover from illness, maintain 1-2x light strength if possible. Why: Got sick Tue night. Prioritizing recovery per program (rest > pushing through).
```

**Scenario C - Injury flare-up (knee pain):**
```
2025-week-48:
Daily: Knee protocol 2x/day 15min - backward sled, Nordics, tibialis (increased from 1x for rehab). Mon: Upper @ Office - bench 5x5, rows 4x8, OHP 3x8 (unaffected, full). Tue: Modified lower @ Home - box squat to parallel 4x5 (no deep), RDL 3x8, leg curls. Wed: Easy bike 20min (low-impact, knee-safe). Thu: Upper @ Office (full). Fri: OFF (extra rest for knee). Sat: Upper @ Home (extra volume vs missing second lower). Sun: Assess + mobility. Week goal: 3x upper (full), 1x modified lower (box squat only), daily knee protocol 2x, NO pain aggravation. Why: Knee twinge Tue. Following program injury protocol (modify not skip, focus what you CAN do, increase prehab). Extra upper compensates for limited lower.
```

**Key principles:**
- **Stress:** Reduce volume, prioritize sleep, conditional sessions (IF RECOVERED), flexible make-up days
- **Illness:** Update week mid-stream, rest until better, light return, don't rush back
- **Injury:** Increase prehab, modify affected exercises (box squat vs deep), focus unaffected areas (extra upper volume)

---

## Week Updates Mid-Week

**When plans change:** Same key = replaces old version

**Update when:** Unexpected travel, injury, sick, opportunity, schedule conflict

**Pattern:** Mark completed (✓), show changes, revise week goal, explain why, adjust remaining days

(See Example 4 Scenario B above for illness mid-week update pattern)

---

## Quick Reference

**Week planning is about:**
1. **When**: Map program to 7 specific days
2. **Where**: Assign gym/location based on equipment context
3. **What**: This week's goal (what to accomplish)
4. **How**: Maximize adherence despite constraints

**Not about:**
- Exercise selection (in program)
- Sets/reps/loads (in program & workout)
- Detailed substitutions (in program)
- Training principles (in program)

**Process:**
1. Review program (frequencies, split, equipment, protocols)
2. Identify this week's constraints (travel, stress, recovery, schedule)
3. Map program to 7 days (when/where for each session)
4. Set week goal (what to accomplish)
5. Plan for adherence (consistent timing, backup options, lower bar if needed)
6. Propose → approve → save

**Remember:** Week is about scheduling and staying on track. Program contains all the execution details. Workout applies program details to today.
