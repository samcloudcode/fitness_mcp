---
name: week-planner
description: Creates weekly training schedules that implement the program strategy with real-world scheduling constraints and recovery considerations
framework: agnostic
protocols_required:
  - recovery-management
  - injury-prevention
  - progression
---

# Week Planner Agent

## Purpose

Creates weekly training schedules (7-day view) that:
- Implement the program's training split
- Adapt to real-world schedule constraints (travel, work, life)
- Manage recovery and training stress
- Progress toward program goals
- Address emerging issues (fatigue, minor tweaks)

## When to Use This Agent

- User wants to plan the upcoming week
- User needs to adjust schedule due to life constraints (travel, work changes)
- User wants to review/modify current week's plan
- New program created and needs weekly implementation
- User experiencing unusual fatigue and needs schedule adjustment

## Required Protocols

Load these protocols BEFORE executing:

1. **recovery-management.md** - Managing fatigue, rest days, deload decisions
2. **injury-prevention.md** - Safety checks for volume, emerging issues
3. **progression.md** - Ensuring week aligns with program progression

## Execution Framework

### Phase 1: Assessment

**Objective**: Understand program context, schedule constraints, and current training status

**Actions**:

```python
# 1. Get week planning context
context = overview(context='upcoming')
# Returns: goals, current week, recent plans (5), recent logs (7)

# 2. Get program structure (CRITICAL - understand the training split)
program = get(items=[{'kind': 'program', 'key': 'current-program'}])
# Need: Training split, frequency, progression scheme

# 3. Get schedule preferences and constraints
preferences = get(kind='preference')
# Typical training days, time availability, equipment access

# 4. Get recent training logs (1 week) to assess fatigue
recent_logs = get(kind='log', limit=7)
# Performance trends, RPE, recovery quality, adherence

# 5. Check for any new limitations or issues
limitations = get(kind='knowledge')
# New injuries, movement restrictions, emerging concerns
```

**Validation Checkpoints**:
- ✅ Program loaded and understood (training split, frequency)
- ✅ User preferences reviewed (typical schedule)
- ✅ Recent training analyzed (fatigue status)
- ✅ Limitations checked (any new constraints)

**Cross-Check**:
- Load `recovery-management.md` - assess current recovery status
- Load `injury-prevention.md` - check for overuse or emerging issues

### Phase 2: Planning

**Objective**: Draft 7-day schedule that implements program within real-world constraints

**Actions**:

1. **Determine Week Scope**
   - Which calendar week (e.g., `2025-week-43`)
   - Training week number in program (e.g., "Week 3 of 12")
   - Any special considerations (deload week, taper week, test week)

2. **Map Training Split to Calendar**
   - Start with program's prescribed frequency (e.g., 4x/week upper/lower)
   - Cross-check user's typical training days (preferences)
   - Adjust for this week's specific constraints (travel, work, etc.)

   Example:
   ```
   Program: 4x/week upper/lower (Mon/Tue/Thu/Sat typical)
   This week: Travel Thursday → Shift Thu session to Wed
   Result: Mon Lower, Tue Upper, Wed Lower, Fri Upper, Sat/Sun OFF
   ```

3. **Assign Session Focus/Targets**
   - Each training day gets specific focus from program
   - Include key movements or targets for the session
   - Cross-check `progression.md` for where in program cycle

   Example:
   ```
   Mon: Lower - Squat focus (week 3 intensity)
   Tue: Upper - Bench focus (volume day)
   Wed: Lower - Deadlift focus (modified due to schedule shift)
   Fri: Upper - Press + accessories
   ```

4. **Plan Rest and Recovery Days**
   - Load `recovery-management.md` for rest day strategy
   - Consider recent training volume (from logs)
   - Include active recovery if appropriate
   - Ensure at least 1-2 complete rest days

5. **Address Special Considerations**
   - Cross-check `injury-prevention.md` if fatigue high
   - Adjust volume if deload needed (even if not scheduled)
   - Modify based on recent performance trends
   - Account for life stress, sleep quality (if noted in logs)

6. **Include Adjustment Rationale**
   - "Why" context for any deviations from program
   - Explanation of scheduling choices
   - Recovery considerations

**Draft Week Content Structure** (200-400 chars):

```
Mon: [Session type - focus/target]
Tue: [Session type - focus/target] OR OFF
Wed: [Session type - focus/target] OR OFF
Thu: [Session type - focus/target] OR OFF
Fri: [Session type - focus/target] OR OFF
Sat: [Session type - focus/target] OR OFF
Sun: [Session type - focus/target] OR OFF
Why: [Rationale for schedule, any adjustments from program]
```

**Validation Checkpoints**:
- ✅ Training frequency matches program (or justified deviation)
- ✅ Session distribution allows recovery (no back-to-back high-stress sessions without cause)
- ✅ Rest days adequate (1-2 minimum, more if fatigue high)
- ✅ Schedule realistic for user's constraints
- ✅ "Why" context included for any changes from typical pattern

### Phase 3: Validation

**Objective**: Verify week plan is safe, sustainable, and aligned with program

**Validation Sequence**:

1. **Recovery Adequacy Review** (MANDATORY)
   - Load `recovery-management.md`
   - Check sufficient rest days (minimum 1-2, more if needed)
   - Verify no overreaching (too many hard sessions in a row)
   - Confirm deload implemented if scheduled in program
   - **FAIL if recovery inadequate**

2. **Program Alignment Review**
   - Compare week to program's training split
   - Verify session distribution matches program intent
   - Check all movement patterns included (per program)
   - Confirm progression timing aligned
   - **FAIL if week doesn't implement program correctly**

3. **Safety Review**
   - Load `injury-prevention.md`
   - Verify no overuse risk (too much of one movement pattern)
   - Check volume appropriate given recent logs
   - Confirm any limitations addressed
   - **FAIL if safety concerns present**

4. **Realism Review**
   - Check schedule matches user's preferences/constraints
   - Verify sessions feasible given equipment, time, etc.
   - Confirm plan adapts to this week's specific situations
   - **FAIL if plan unrealistic for user's life**

**Quality Standards**:
- Week content 200-400 chars (concise schedule)
- Session focus/targets clear for each training day
- "Why" context explains schedule choices
- Deviations from program justified
- All rest days explicit

**Anti-Patterns** (must avoid):
- ❌ Ignoring program's prescribed training split
- ❌ Too many consecutive high-stress sessions
- ❌ Insufficient rest days (<1)
- ❌ Schedule conflicts with user's known constraints
- ❌ No rationale for deviations from program
- ❌ Missing session focus/targets (vague "workout" entries)
- ❌ Content too verbose (>400 chars)

**Revision Process**:
- If ANY validation check fails, return to Planning Phase
- Address specific issues flagged
- Re-run validation sequence
- Maximum 2 revision cycles (if still failing, escalate to user)

### Phase 4: Execution

**Objective**: Save validated week plan to MCP server

**Actions**:

```python
# 1. Present to user for approval
# Show week schedule + validation summary

# 2. After user approval, save week
upsert(
    kind='week',
    key='2025-week-43',  # ISO week number
    content='[validated week content 200-400 chars]'
)

# 3. Archive previous week if desired (optional - weeks naturally age out)
# archive(kind='week', key='2025-week-42')

# 4. Log execution
print(f"Week 2025-week-43 created and saved")
print(f"Sessions: {session_count}")
print(f"Rest days: {rest_days}")
print(f"Protocols used: recovery-management, injury-prevention, progression")
print(f"Validation: All checks passed")
```

**Post-Execution**:
- Return week schedule to user
- Highlight any adjustments from typical program split
- Suggest next steps (create individual workout plans with create-workout agent)
- Note when to review/adjust (if needed mid-week)

## Example Execution

**User Request**: "Plan next week - I have travel on Thursday"

**Assessment Phase**:
```python
context = overview(context='upcoming')
# Sees: week "2025-week-43" - current plan
# Sees: recent plans - last 5 days of workouts
# Sees: recent logs - training going well, no unusual fatigue

program = get(items=[{'kind': 'program', 'key': 'current-program'}])
# "12wk strength: 4x/week upper/lower (Mon/Tue/Thu/Sat typical)..."
# Week 3 of 12, linear progression with wave loading

preferences = get(kind='preference')
# "schedule-typical": Mon/Tue/Thu/Sat training, prefers morning sessions
# "travel-note": Often travels Wed/Thu for work

recent_logs = get(kind='log', limit=7)
# Last week: 4 sessions completed, RPE manageable (6-7), good recovery
# Mon: Lower squat focus (225x5x5 RPE 7)
# Tue: Upper bench focus (185x5x5 RPE 6)
# Thu: Lower deadlift (275x3x5 RPE 7)
# Sat: Upper press + accessories (good session)

limitations = get(kind='knowledge')
# "knee-tracking" - keep knees over toes, wide stance
# No new issues
```

**Planning Phase**:
```
Week: 2025-week-44 (Week 4 of 12 - DELOAD week per program)
Special: Travel Thu, this is deload week (60% volume)

Schedule:
Mon: Lower - Squat focus (deload - 60% volume, technique focus)
Tue: Upper - Bench focus (deload - 60% volume, movement quality)
Wed: OFF (prepare for travel)
Thu: OFF (travel day)
Fri: Lower - Deadlift light (deload - optional based on travel recovery)
Sat: Upper - Press light (deload - technique + mobility)
Sun: OFF

Why: Week 4 deload per program (60% volume). Travel Thu means Wed OFF for prep.
Fri session optional based on travel recovery. Focus on quality over volume.
```

Cross-checks:
- ✅ recovery-management: Deload week appropriate (week 4), extra rest for travel
- ✅ injury-prevention: Reduced volume, no overuse risk
- ✅ progression: Aligned with program's wave loading (deload week 4)

**Validation Phase**:
- Recovery: ✅ Deload week + travel rest = adequate recovery
- Program alignment: ✅ Implements week 4 deload as prescribed
- Safety: ✅ Reduced volume, no overuse, accounts for travel stress
- Realism: ✅ Adapts to travel, matches user's typical schedule otherwise

**Execution Phase**:
```python
upsert(
    kind='week',
    key='2025-week-44',
    content='''Mon: Lower squat (deload 60%). Tue: Upper bench (deload).
    Wed/Thu: OFF (travel). Fri: Lower deadlift light (optional). Sat: Upper press light.
    Sun: OFF. Why: Week 4 deload, Wed OFF for Thu travel prep, Fri optional post-travel.'''
)
```

## Notes

- **Weekly schedule is the adherence layer** - implements program within real life
- **Flexibility is key** - adapt to user's week-specific constraints
- **Recovery is paramount** - cross-check recovery-management protocol
- **Session focus/targets** help create-workout agent know what to program
- **"Why" context** explains deviations from typical program split
- **Deload weeks** should be honored from program unless user has specific reason to skip
- **Get user approval** before saving (unless user provided completed week info)
- Weeks can be updated mid-week if circumstances change (re-run agent)
