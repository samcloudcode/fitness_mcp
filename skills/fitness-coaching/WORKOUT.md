# Workout Creation

**Load this file when:** Client asks for a workout or you need to create a plan for a specific training session.

**This file contains:**
- 7-step workout design workflow
- Plan creation and templates
- Data fetching requirements
- Logging completed workouts

---

## 7-Step Workout Design Workflow

When client asks for a workout, follow this complete process:

1. **Fetch all relevant info**: `fitness-mcp:overview(context='planning')` - get goals (priority order), program, week, recent plans (5 most recent), all knowledge, all preferences, recent logs (10 most recent)

2. **Ensure current-program is up to date**: Review program freshness (stale if 3+ months old). If strategy doesn't match current goals or recent feedback, **load PROGRAM.md** to update → propose → get approval → save

3. **Check week plan**: Ensure week is current and relevant. If outdated or strategy changed, **load WEEK.md** to update → propose → get approval → save

4. **Think deeply to create optimal workout**: Consider ALL context - knowledge (injuries/limitations), history (recent training), current level (logged performance), preferences (equipment/style). Assume 1hr duration unless client specifies otherwise.

5. **Propose and refine**: Present workout with rationale. Refine based on client feedback until they approve.

6. **Save, then guide**: **Only after approval** → `fitness-mcp:upsert(kind='plan', key='YYYY-MM-DD-{type}', ...)`. Then help guide execution (answer questions, provide cues, adjust on the fly).

7. **Log workout sessions**: After completion, use `fitness-mcp:upsert(kind='log', key='YYYY-MM-DD-{type}', content='...')` - maintains one log per workout that can be updated incrementally

---

## Data Fetching Rules (Safety First)

**NEVER program a workout without reviewing saved context first.**

### ALWAYS Fetch Before Programming:
- **Use `fitness-mcp:overview(context='planning')` first** - Gets everything in one call (goals, program, week, plan, knowledge, recent logs)
- **If needed, fetch full details:** `fitness-mcp:get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])` for truncated content
- **Recent training:** Already in planning context (2 weeks of logs)
- **Current program:** Already in planning context
- **Preferences:** Already in planning context

### Only Fetch More If:
- User asks for specific analysis ("show me my bench progress over 3 months")
- Investigating patterns requiring deeper history

**Better to over-fetch and be thorough than miss critical limitations. Injuries happen from incomplete context.**

---

## Plan - Today's Specific Workout

Planned workout for a specific date and training type:

```python
fitness-mcp:upsert(
    kind='plan',
    key='2025-10-22-strength',
    content='6am Upper: Bench 4x10 @ 185 RPE 8 (volume for bench-225), OHP 3x12 @ 115 (shoulder health + pressing volume), Rows 3x12 @ 70 (balance pressing). Why: Hypertrophy phase building muscle for strength later. OHP light due to previous shoulder tweak.'
)

fitness-mcp:upsert(
    kind='plan',
    key='2025-10-22-run',
    content='5pm Easy: 5mi @ 8:30/mi conversational. Why: Recovery run between tempo sessions. Keeps weekly volume up (sub-20-5k goal) without interfering with tomorrow lower body strength.'
)
```

**Key:** Date + type format `YYYY-MM-DD-{strength|run|mobility|yoga|etc}`

**Content must include:**
- Time/location if relevant ("6am", "gym", "track")
- Exercises with sets/reps/loads OR workout type with duration/pace
- Which goal(s) this plan supports (inline notes in parentheses)
- Why: Rationale for exercise selection, loading, approach, or any modifications

**Length:** 200-400 chars

**Real-world Examples:**
```
Push/Pull: HSPU 5x5 freestanding, archer pull-ups 4x6/side, ring dips 4x10-12, weighted pull-ups 4x5 @ +30kg (strength goal progression). Why: Fresh recovery state allows quality work for upper-body-strength goal. Full rest between sets prioritizes neural adaptation.

Track VO2 intervals: 4x3min @ 16-17 km/h (progressive), 90s recovery. Warmup 10min easy + strides. Why: Once-weekly high-intensity for sub-20-5k goal. VO2 adaptation without overreaching concurrent training load.

Morning mobility: 20min easy yoga/stretching, focus hip openers and shoulder mobility. Why: Pre-regatta recovery priority. Prepares body for sailing demands (hip-mobility goal) without adding training stress before competition.
```

**Why must connect to goals:**
- Reference specific goal keys inline or in Why section
- Explain HOW this workout moves toward that goal (volume, intensity, skill, recovery)
- Include today's specific rationale (fatigue state, phase, constraints)

**Avoid:**
- Day names (e.g., "Monday", "Today") - date key provides this
- Verbose labels (e.g., "Strength Session -") - key suffix provides this
- Relative time references (e.g., "tomorrow") - becomes stale immediately
- Generic reasons without goal connection (e.g., "good for fitness")

---

## Plan Template (Before Workout)

```python
fitness-mcp:upsert(
    kind='plan',
    key='YYYY-MM-DD-{type}',  # e.g., '2025-10-29-upper'
    content='[Time] {Type}: {Exercise 1 sets×reps @ load}, {Exercise 2}... Why: {how this helps goals + today\'s rationale}.'
)
```

---

## Logging Completed Workouts

After the workout is done, log what actually happened:

### Log Template (After Workout)

```python
fitness-mcp:upsert(
    kind='log',
    key='YYYY-MM-DD-{type}',  # e.g., '2025-10-29-upper'
    content='{Type} ({duration}): {Exercise 1 sets×reps @ load RPE}, {Exercise 2}... {Optional: how it felt}.'
)
```

### Logging Workflow

**User provides completed info:** Save immediately with `fitness-mcp:upsert(kind='log', key='YYYY-MM-DD-{type}', content='...')`

**Build incrementally:** Same key updates existing log (e.g., adding exercises as completed)

**Example:**
```
User: "Just did squats 5x5 at 225"
→ fitness-mcp:upsert(kind='log', key='2025-10-29-lower', content='Squats 5x5 @ 225lbs')

User: "Also did bench press 3x8 at 185" (same session)
→ fitness-mcp:upsert(kind='log', key='2025-10-29-lower', content='Squats 5x5 @ 225lbs, Bench 3x8 @ 185lbs')
```

---

## Creating Workout Plan - Quick Reference

1. **Review everything**: Goals, program, week, knowledge, recent logs (use `overview(context='planning')`)
2. **Propose workout**: Detailed exercises with rationale
3. **Get approval**: Adjust based on feedback
4. **Save**: `fitness-mcp:upsert(kind='plan', key='YYYY-MM-DD-{type}', content='...')`

**Remember:** Follow propose → approve → save pattern. Never save before client approves.
