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

## Week Examples (Scheduling & Adherence Focus)

### Example 1: Standard Week (No Constraints)

```
2025-week-43:
Mon: Upper @ Office 6am - bench 5x5 focus, rows 4x8. Tue: Lower @ Home 6am - squat 4x5 focus, RDL 3x8. Wed: Easy run 6:30am - Z2 30min. Thu: Upper @ Office 6am - OHP 4x6 focus, pull-ups 3x8. Fri: Lower @ Home 6am - deadlift 3x4 focus, Bulgarian split 3x8. Sat: Tempo run 7am - 4mi @ threshold. Sun: Long run 7am - 60min easy. Week goal: Complete Week 4 of strength block at prescribed loads (bench 185, squat 250, deadlift 285). Why: Normal schedule, no travel, good recovery. Standard split following program.
```

**Scheduling decisions:**
- Office Mon/Thu (per program equipment context)
- Home Tue/Fri (per program equipment context)
- All 6am/6:30am/7am (consistent timing per preferences)
- **Session targets** from program (bench/squat/deadlift as main focuses, secondary work noted)
- Hard days Mon/Tue/Thu/Fri/Sat (5 total - within program guideline)
- Week goal: Complete block progression at specific week loads

### Example 2: Travel Week (Thu-Sat Disrupted)

```
2025-week-44:
Mon: Upper @ Office 6am - bench 5x5, rows 4x8 (full session). Tue: Lower @ Home 6am - squat 4x5, RDL 3x8 (full session). Wed: Easy run 6:30am Z2 + prep/pack for travel. Thu: OFF (flight, travel day). Fri: Hotel bodyweight 7am 30min - push-ups 3x15, inverted rows, pistol progression (volume reduced, following program travel protocol). Sat: Easy run 3mi - easy pace, unfamiliar area. Sun: Return + full-body @ Home 9am - squat 3x5, bench 3x5, rows 3x8 (catch-up session). Week goal: Maintain 3x strength (Mon/Tue/Sun) despite Thu-Sat travel - adherence over perfection. Why: Conference Thu-Sat, hotel gym limited. Following program's travel constraint management (reduce volume 20-30%, maintain frequency). Sun catch-up before resume normal Mon.
```

**Scheduling decisions:**
- Wed: Extra prep time (pack gym clothes, bands, plan Fri/Sat)
- Thu: OFF (flight = lost day, per program don't force training on travel days)
- Fri: 30min hotel bodyweight (following program's bodyweight substitutions) - **session focus**: maintain movement patterns with available equipment
- Sat: Easy run only (jet lag = poor recovery, program says prioritize sleep)
- Sun: Make-up full-body session (maintain weekly frequency goal) - **combines upper/lower** to hit main lifts
- Week goal: 3x strength (acceptable vs normal 4x given travel)

### Example 3: Deload Week

```
2025-week-45:
Mon: Light upper @ Office 6am 40min - bench 3x5 @ 180lb (vs normal 5x5 @ 185), rows 3x8 (50% volume). Tue: Easy run 3mi Z2. Wed: Light lower @ Home 6am 40min - squat 2x5 @ 250lb (vs normal 4x5), RDL 2x8 (50% volume). Thu: OFF (extra rest). Fri: Easy run 3mi Z2. Sat: Mobility 30min - hip/shoulder work. Sun: OFF (extra rest). Week goal: Dissipate fatigue from 4-week block, maintain movement patterns at same intensity but 50% volume, arrive fresh for Week 1 of next block. Why: Deload per program schedule (every 4 weeks). Following program's deload protocol (50% volume method - keep intensity, reduce sets). Extra rest days (Thu/Sun).
```

**Scheduling decisions:**
- Mon/Wed only (2x strength vs normal 4x)
- Shorter sessions (40min vs 60min per program deload protocol)
- **Session targets**: Same weights (intensity maintained), half the sets (volume reduced) - per program deload protocol
- Extra rest days (Thu/Sun vs just Sun)
- Easy cardio only (no hard sessions this week)
- Week goal: Recovery and freshness (NOT progression)

### Example 4: High Stress Week (Work Deadline)

```
2025-week-46:
Mon: Upper @ Office 6am 45min - bench 4x5 (reduced from 5x5), rows 3x8, skip accessories (sleep priority). Tue: Easy walk 20min (instead of lower - prioritizing sleep). Wed: OFF (deadline crunch, sleep > training). Thu: Lower @ Home 6am 45min IF RECOVERED - squat 3x5, RDL 2x8 (if good sleep Wed night, otherwise skip). Fri: Easy run 3mi Z2. Sat: Full upper @ Office 9am - bench/OHP/rows IF FEELING GOOD (make up volume). Sun: Long run 60min OR OFF (assess recovery). Week goal: Maintain 2-3x strength minimum, prioritize sleep over hitting all sessions. Why: High work stress Mon-Wed (deadline Thu AM). Following program's stress constraint management (reduce volume 20%, maintain frequency when possible, sleep priority). Flexible Thu/Sat/Sun based on recovery.
```

**Scheduling decisions:**
- Mon: **Reduced volume** (4x5 vs 5x5), skip accessories to save time/fatigue
- Tue: Walk instead of lower (program says "maintain movement, reduce intensity")
- Wed: OFF (sleep > training during high stress)
- Thu: **Conditional session** - only if good sleep Wed night, with reduced volume
- Sat/Sun: **Flexible** (make up volume if feeling good, rest if still stressed)
- Week goal: 2-3x strength (vs normal 4x) + prioritize sleep
- Adherence: Lower bar = higher success rate

### Example 5: Injury Flare-Up Week (Knee Pain)

```
2025-week-47:
Daily: Knee protocol 2x/day 15min - backward sled, Nordics, tibialis, band walks (per program mandatory). Mon: Upper @ Office 6am - bench 5x5, rows 4x8, OHP 3x8 (unaffected, full session). Tue: Modified lower @ Home 6am - box squat to parallel 4x5 (no deep squat), RDL 3x8, leg curls 3x10 (following program injury protocol). Wed: Easy bike 20min Z2 (low-impact, knee-safe). Thu: Upper @ Office 6am - bench variations 4x8, pull-ups 3x8 (full session). Fri: OFF (extra rest for knee). Sat: Upper @ Home 9am - OHP 4x6, rows 4x8, accessories (extra upper volume vs missing second lower). Sun: Assess knee + easy walk 30min or mobility. Week goal: 3x upper (full volume), 1x modified lower (box squat only), daily knee protocol 2x compliance, NO pain aggravation. Why: Knee twinge Tue during squat. Following program's injury constraint (modify not skip, focus what you CAN do, increase prehab frequency). Extra upper Sat compensates for limited lower.
```

**Scheduling decisions:**
- Daily knee protocol 2x (non-negotiable per program) - **increased frequency from 1x to 2x** for rehab
- Tue: **Modified lower** (program has box squat to parallel substitution for knee pain) - specific exercise swap, same volume
- Fri: Extra rest (let knee settle)
- Sat: **Extra upper session** (focus what works per program) - upper unaffected, increase volume here
- Week goal: Compliance with rehab + maintain upper volume + no aggravation
- Adherence: Showing up with modifications > skipping everything

### Example 6: Equipment-Limited Week (Home Gym Only)

```
2025-week-48:
Mon: Full-body @ Home 6am - squat 4x5, bench 5x5, rows 4x8, face pulls 3x15 (normally upper only, but full equipment available). Wed: Full-body @ Home 6am - deadlift 3x4, OHP 4x6, pull-ups 3x8, RDL 3x8 (hinge + press focus). Fri: Full-body @ Home 6am - front squat 3x6, incline bench 4x8, DB rows 3x10, leg curls 3x10 (variation day, different exercises). Tue/Thu/Sat: Easy runs 3-4mi Z2. Sun: Long run 60min Z2. Week goal: Maintain 3x strength via full-body split (vs normal 4x upper/lower), hit all main movements at program loads. Why: Office gym closed (renovation Mon-Fri). All training @ home with full barbell equipment. Following program's equipment substitution (have barbell so can do all main lifts, just different split to fit 3x schedule vs normal 4x). Advantage: All barbell work (vs DBs at office).
```

**Scheduling decisions:**
- 3x full-body (Mon/Wed/Fri) instead of 4x upper/lower
- **Session focuses**: Mon = squat+bench, Wed = deadlift+OHP, Fri = variations (front squat+incline)
- All @ home (per constraint - office closed)
- 48-72hr between sessions (per program recovery guidelines)
- Week goal: Maintain volume via different split, hit all program main lifts
- **Advantage**: All barbell work (vs DBs at office) - can use heavier loads on bench/OHP

---

## Week Updates Mid-Week

**When plans change during the week:**

Same key = replaces old version
Update when: Unexpected travel, injury, sick, opportunity, schedule conflict

Example:
```
# Monday - original plan
"2025-week-43: Mon: Upper @ Office. Tue: Lower @ Home. Wed: Run. Thu: Upper @ Office. Fri: Lower @ Home. Sat: Tempo. Sun: Long run. Week goal: Hit all 4 strength at Week 3 loads."

# Wednesday - got sick Tuesday night, updating plan
fitness-mcp:upsert(
    kind='week',
    key='2025-week-43',
    content='Mon: Upper @ Office ✓. Tue: OFF (sick). Wed: Still sick, OFF. Thu: Easy walk if feeling better. Fri: Light upper @ Office 40min (if recovered). Sat: Lower @ Home (if fully recovered). Sun: Easy run or OFF. Week goal REVISED: Recover from illness, maintain 1-2x light strength if possible. Why: Got sick Tue night. Prioritizing recovery per program (rest > pushing through). Will resume normal Week 44.'
)
```

**Update pattern:**
- Mark completed (✓)
- Show changes
- Revise week goal if needed
- Explain constraint
- Plan adjusted approach

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
