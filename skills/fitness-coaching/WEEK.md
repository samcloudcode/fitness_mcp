# Week Planning

**Load this file when:** Creating or updating a weekly training schedule.

**This file contains:**
- How to create weekly schedules
- Week templates and examples
- Balancing training across 7 days
- Adjusting for constraints

---

## Week - This Week's Schedule

Weekly plan across all training types, with constraints and context:

```python
fitness-mcp:upsert(
    kind='week',
    key='2025-week-43',
    content='Mon: Upper strength. Tue: Easy run 5mi (recovery). Wed: Lower strength. Thu: OFF - traveling for work, high stress. Fri: Tempo run 4mi (race-specific). Sat: Full body (extra volume to compensate Thu). Sun: Long run 8mi. Why: Thu travel means 6 sessions not 7. Compensating with Sat volume. Tempo Fri not Thu due to travel. Week 2 of current strength block.'
)
```

**Key:** ISO week format `2025-week-NN` (week 01 through 53)

**Content must include:**
- Daily schedule (Day: Type + brief description for each day)
- Any deviations from normal program (travel, fatigue, injury, time constraints)
- Rationale for adjustments this week
- Context: which phase/week of program, special considerations

**Length:** 200-400 chars

---

## Week Template

```python
fitness-mcp:upsert(
    kind='week',
    key='YYYY-week-NN',  # e.g., '2025-week-43'
    content='Mon: {type}. Tue: {type}. Wed: {type}. Thu: {type}. Fri: {type}. Sat: {type}. Sun: {type}. Why: {adjustments and rationale}.'
)
```

---

## Creating Weekly Plan Workflow

1. **Review context**: Check program and recent training
   - `fitness-mcp:overview(context='planning')` to see goals, program, recent logs
   - If program is stale/outdated, **load PROGRAM.md** to update first

2. **Propose week**: Layout 7 days with adjustments for constraints
   - Consider: Travel, work stress, recovery needs, goal priorities
   - Balance training types across the week
   - Account for rest/recovery days

3. **Get approval**: Modify as needed based on client feedback

4. **Save**: `fitness-mcp:upsert(kind='week', key='YYYY-week-NN', content='Mon:...')`

---

## Weekly Planning Principles

### Balance Training Across the Week

**Sequence matters:**
- Hard days hard, easy days easy (polarized approach)
- Separate interfering sessions (heavy legs before hard running = poor recovery)
- Group complementary work (mobility on easy days, skills on recovery days)

**Example sequencing:**
```
Mon: Heavy strength (fresh state)
Tue: Easy cardio (active recovery)
Wed: Power/skill work (quality work, moderate fatigue)
Thu: OFF or mobility (mid-week recovery)
Fri: High-intensity intervals (rested from Thu)
Sat: Volume work (time available, manageable fatigue)
Sun: Long easy (time available, builds aerobic base)
```

### Adjust for Constraints

**Common adjustments:**
- **Travel**: Reduce total volume, focus on maintenance, bodyweight alternatives
- **High work stress**: Lower intensity, focus on movement quality over load
- **Poor sleep/recovery**: Extra rest day, shift hard sessions later in week
- **Time constraints**: Shorter sessions, combine modalities (strength + conditioning)
- **Injury/pain**: Modify or skip affected movements, increase recovery work

**Template for constrained week:**
```
Mon: {Normal}. Tue: {Normal}. Wed: OFF - {constraint reason}. Thu: {Adjusted session}. Fri: {Normal}. Sat: {Compensate for Wed}. Sun: {Normal/Easy}. Why: {How you're managing the constraint}.
```

---

## Real-World Week Examples

### Standard Training Week
```
2025-week-43:
Mon: Upper strength 60min. Tue: Easy run 5mi. Wed: Lower strength 60min. Thu: Zone-2 run 45min. Fri: Upper strength 45min. Sat: Long run 10mi. Sun: OFF + mobility 20min. Why: Standard split during base phase. Progressing toward bench-225 and 5k-sub20 goals. Week 4 of 8-week block.
```

### Adjusted for Travel
```
2025-week-44:
Mon: Upper strength 60min. Tue: Easy run 5mi. Wed: Lower strength (home gym, limited equipment). Thu: OFF - flight to conference. Fri: Hotel bodyweight 30min. Sat: Easy run 3mi (jet lag). Sun: Full strength 75min (catch-up volume). Why: Thu-Sat travel disrupts normal routine. Maintaining consistency with modified sessions, compensating Sun.
```

### Deload Week
```
2025-week-45:
Mon: Light upper 40min (50% volume). Tue: Easy run 3mi. Wed: Light lower 40min (50% volume). Thu: OFF. Fri: Easy run 3mi. Sat: Mobility + skill work 30min. Sun: OFF. Why: Deload after 4-week block. Reducing volume/intensity for recovery before next progression. Maintaining movement patterns without fatigue.
```

### Peak Week (Before Event)
```
2025-week-46:
Mon: Strength maintenance 40min. Tue: Easy run 2mi. Wed: OFF. Thu: Race-pace 2mi (sharpening). Fri: OFF + mobility. Sat: 5K RACE. Sun: Easy recovery 2mi walk. Why: Tapering for Saturday race. Reduced volume, maintaining intensity. Fresh legs priority.
```

---

## Quick Reference

```
Creating new week:
1. Check program and recent training (overview context='planning')
2. Layout 7 days balancing work/rest/modalities
3. Note constraints and adjustments
4. Propose → get approval → save

Updating existing week:
- Same key = replaces old version
- Update when plans change mid-week
- Include "why" for changes
```

**Remember:** Week planning bridges program strategy (PROGRAM.md) and daily execution (WORKOUT.md). Balance the big picture with this week's reality.
