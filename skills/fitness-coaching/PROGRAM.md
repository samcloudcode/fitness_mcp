# Program Creation

**Load this file when:** Creating or updating the overall training program strategy.

**This file contains:**
- How to create a comprehensive training program
- Program templates and examples
- Integrating multiple goals
- Concurrent training management

---

## Program - Overall Training Strategy

How all goals fit together. Single living document - update when strategy changes or stale (3+ months):

```python
fitness-mcp:upsert(
    kind='program',
    key='current-program',
    content='As of Oct 2025: Strength primary (bench-225, squat-315 goals) 4x/week, running secondary 3x/week (20-25mpw maintains base for sub-20-5k without interfering). Daily hip mobility (15min AM) for hip-mobility goal. Why this balance: Rugby season April needs strength peak. 5K race mid-April aligns. Hip work daily because consistency > intensity for mobility gains. Concurrent training managed by keeping running easy (80%) except 1-2 hard sessions/week.'
)
```

**Key:** Always `current-program` (update as strategy evolves)

**Content must include:**
- "As of Month-Year" (when last updated)
- Which goals are being targeted (reference goal keys)
- Training split/frequency for each modality (strength/running/mobility/etc.)
- How modalities interact (e.g., concurrent training management)
- Why this approach makes sense (rationale for balance, sequencing, priorities)

**Length:** 400-600 chars

---

## Program Template

```python
fitness-mcp:upsert(
    kind='program',
    key='current-program',
    content='As of {Month Year}: {Primary focus} {frequency}, {secondary focus} {frequency}. Why this balance: {rationale for approach}.'
)
```

---

## Creating/Updating Program Workflow

1. **Review current state**: `fitness-mcp:overview(context='planning')` to see goals and current program

2. **Propose program**: Present overall strategy linking all goals
   - Identify goal priorities (p1 = highest)
   - Determine training frequencies for each modality
   - Explain how modalities fit together
   - Account for time/equipment/recovery constraints

3. **Get approval**: Refine based on feedback

4. **Save**: `fitness-mcp:upsert(kind='program', key='current-program', content='As of...')`

---

## Program Design Principles

### Goal-Driven Programming

**Start with goals:** Every program element should trace back to a specific goal.

```
Example:
- Goal: p1-bench-225 → Strength 4x/week (primary focus)
- Goal: p2-5k-sub20 → Running 3x/week (secondary, maintenance)
- Goal: p1-pain-free-squat → Daily mobility (injury prevention)
```

**Prioritize based on p1/p2/p3:**
- p1 goals get primary focus (most volume, highest frequency, best recovery)
- p2 goals get secondary focus (maintain, don't progress aggressively)
- p3 goals get minimal viable dose (don't let interfere with p1/p2)

### Integrating Multiple Goals

**Concurrent training:** When combining strength + endurance:
- Keep endurance work easy (80% at conversational pace)
- Limit high-intensity endurance to 1-2x/week
- Separate hard strength and hard endurance by 6-24 hours
- Use easy cardio as active recovery between strength sessions

**Complementary goals:** When goals support each other:
- Mobility + strength = better movement quality, injury prevention
- Skill work + recovery days = efficient use of rest time
- Easy cardio + active recovery = dual benefit

**Competing goals:** When goals interfere:
- Prioritize higher p-value goal
- Use periodization (focus on one, maintain the other, then switch)
- Accept sub-optimal progress on lower priority

### Time-Based Structure

**When to update program:**
- Strategy no longer matches goals (goal priorities changed)
- Stale (3+ months old, needs fresh approach)
- Major life change (injury, equipment access, time availability)
- Client feedback indicates approach isn't working

**Program phases (optional structure):**
- Base building (high volume, lower intensity)
- Intensification (moderate volume, higher intensity)
- Peaking (lower volume, highest intensity, race/test prep)
- Deload/recovery (planned breaks)

---

## Real-World Program Examples

### Single Primary Goal (Strength)
```
As of Jan 2025: Strength primary (bench-225 goal) 4x/week upper/lower split. Daily mobility 15min AM (injury prevention). Easy cardio 2x/week 20-30min (general health, doesn't interfere with strength). Why: Single focus allows maximum strength adaptation. Mobility daily for consistency. Cardio for health without fatigue accumulation.
```

### Dual Goals (Strength + Endurance)
```
As of Mar 2025: Strength primary (squat-315, bench-225) 4x/week. Running secondary (maintain sub-20-5k ability) 3x/week 20-25mpw, 80% easy. Daily hip mobility 10min. Why: Rugby season Apr needs strength peak. Running maintains conditioning without interfering (easy pace, modest volume). Concurrent training managed by keeping runs easy except 1 tempo/week.
```

### Triple Goals (Strength + Endurance + Skill)
```
As of May 2025: Calisthenics strength primary (handstand-press, one-arm-chin) 4x/week skill-focused. Running secondary 3x/week 15-20mpw zone-2. Weekly acro/movement 1x 90min (fun/community). Why: Skill-based strength requires frequency and freshness. Running volume reduced to accommodate skill work CNS demands. Acro session replaces one run, counts toward weekly volume.
```

### Injury Recovery + Goal Maintenance
```
As of Aug 2025: Knee rehab primary (pain-free-squat goal) - daily PT exercises 20min, strength 3x/week (upper focus + modified lower). Running paused (was 3x/week). Mobility 2x/week 30min. Why: Knee health is p1 until resolved. Upper body maintenance to avoid detraining. Running reintroduce after 4 weeks pain-free squatting. Aggressive rehab now prevents chronic issues.
```

---

## Managing Program Freshness

**Review program at session start:**
1. Check "As of" date - stale if 3+ months old
2. Compare to current goals - do they still align?
3. Check recent logs - is client following the program?

**When to propose update:**
- Goals changed (new goal added, priority shifted)
- Strategy not working (client feedback, lack of progress)
- Life circumstances changed (new job, moved, equipment access)
- Approaching staleness (2.5 months old, proactively refresh)

**Update process:**
```
1. "I see your program is from Jan and it's now April - let's review"
2. Check if goals have changed
3. Propose updated program reflecting current reality
4. Get approval
5. Save with new "As of" date
```

---

## Quick Reference

```
Creating program:
1. Review all goals (overview context='planning')
2. Determine priorities (p1 = primary focus)
3. Design training frequencies for each modality
4. Explain how it all fits together
5. Propose → get approval → save

Updating program:
- Same key 'current-program' = replaces old version
- Update "As of" date
- Explain what changed and why
```

**Remember:** Program is the big-picture strategy. Week planning (WEEK.md) and workout creation (WORKOUT.md) implement this strategy day-to-day.
