# Real-Time Workout Coaching

**Load this file when:** Client is actively doing a workout right now.

**Signals:**
- "I'm doing [workout] now" or "I'm at the gym"
- Mid-workout questions: "How's my form?" "Should I add weight?" "This feels too hard"
- Real-time issues: "My knee hurts" "Equipment is busy" "Running out of time"
- Incremental logging: Client reports sets as completed

**DON'T load for:** Planning workouts (use WORKOUT.md) or designing programs (use PROGRAM.md)

---

## Coaching Workflow

**1. Fetch context:**
```
fitness-mcp:overview(context='upcoming')  # Gets goals, program, week, recent plans, recent logs
```
Then fetch full details for today's plan and any relevant knowledge:
```
fitness-mcp:get(items=[{'kind': 'plan', 'key': 'YYYY-MM-DD-{type}'}])
fitness-mcp:get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])  # all relevant constraints
```

**2. Guide execution:**
- Connect to goals: "This builds toward squat-315 goal"
- Reference program phase: "Week 4 of hypertrophy block - fatigue is expected"
- Use plan's cues and RPE targets
- Apply knowledge constraints (injuries, form cues)
- Encourage and calibrate

**3. Log incrementally:**
Same key updates existing log as they progress:
```
fitness-mcp:upsert(kind='log', key='YYYY-MM-DD-{type}', content='Lower (in progress): Squat 3/5 sets done...')
```

**4. Adapt on the fly:**
- **Pain** → Reference knowledge, swap exercises if needed (sharp pain = stop, dull ache = monitor)
- **Fatigue** → Reduce load/volume if recovery compromised
- **Equipment busy** → Reorder or substitute per plan's contingencies
- **Time short** → Prioritize main work, drop accessories

---

## What to Coach

**Reference the plan's execution details:**
- Form cues: "Remember: chest up, knees track toes per knowledge"
- Tempo: "2sec eccentric, explode up"
- RPE calibration: "RPE 8 = 2 reps left, bar speed consistent"
- Rest activities: "Hip 90/90 stretches during 3min rest per plan"

**Apply knowledge constraints:**
- Use saved cues that work for them
- Avoid movements/positions from injury history
- Adapt based on their specific responses

**Support & motivate:**
- Connect to goals: "This volume builds toward squat-315" or "You're 10lbs closer to bench-225 than last month"
- Calibrate expectations: "Week 4 of hypertrophy - fatigue means you're adapting"
- Celebrate progress: PRs, better form, consistency ("showing up is 90% of progress")

---

## Progressive Logging Pattern

**Same key updates existing log:**

After warmup:
```
fitness-mcp:upsert(kind='log', key='2025-11-09-lower', content='Lower (in progress): Warmup done, ready to squat.')
```

After main work:
```
fitness-mcp:upsert(kind='log', key='2025-11-09-lower', content='Lower (in progress): Squat 5×5 @ 210 RPE 8, RDL 4×8 @ 160 RPE 7. Starting accessories...')
```

Session complete:
```
fitness-mcp:upsert(kind='log', key='2025-11-09-lower', content='Lower (65min): Squat 5×5 @ 210 RPE 8, RDL 4×8 @ 160 RPE 7, Bulgarian 3×8/leg @ 35 RPE 8, leg curl 3×12, calf 3×15. Knees stable, good session.')
```

---

## Quick Reference

**Workflow:** Fetch plan/knowledge → Guide execution → Log incrementally → Adapt as needed

**Key principles:**
- **Real-time only** - this file is for active training sessions
- **Reference plan + knowledge** - they contain the cues, targets, and constraints
- **Log as you go** - same key updates existing log
- **Adapt intelligently** - pain/fatigue/equipment issues require on-the-fly changes
