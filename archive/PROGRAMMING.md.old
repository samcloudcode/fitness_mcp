# Programming & Workout Design

This file contains detailed workflows and examples for creating training programs and designing workouts.

## Table of Contents
1. [Planning Hierarchy (4 Levels - Detailed)](#planning-hierarchy-4-levels---detailed)
2. [Content Templates](#content-templates)
3. [Planning Workflows](#planning-workflows)
4. [Step-by-Step Workflows](#step-by-step-workflows)
5. [Data Fetching Rules (Safety First)](#data-fetching-rules-safety-first)
6. [Preference Templates](#preference-templates)

---

## Planning Hierarchy (4 Levels - Detailed)

### 1. Goals - Target States with Priorities

**IMPORTANT: Goals come from the client.** Save immediately when client shares their goals. Don't create goals for them unless explicitly requested.

When client states their goals, save with current state and priority context:

```python
# Client says: "I want to bench 225 by June, I'm at 185 now"
fitness-mcp:upsert(
    kind='goal',
    key='p1-bench-225',  # p1 = highest priority
    content='Bench 225x5 by June. Currently 185x5. Foundation for rugby strength.'
)

# Client says: "I'm training for a 5K race in April"
fitness-mcp:upsert(
    kind='goal',
    key='p2-5k-sub20',  # p2 = medium priority
    content='5K under 20min by April. Company race.'
)

# Client mentions: "I can't squat deep without pain"
fitness-mcp:upsert(
    kind='goal',
    key='p1-pain-free-squat',  # p1 = high priority (pain/injury related)
    content='Full ATG squat without knee pain.'
)
```

**Key pattern:** `p{1|2|3}-{descriptive-goal}` (p1=highest priority)

**Content (all optional, include what's relevant):**
- Target outcome with deadline (e.g., "Bench 225x5 by June")
- Current state (e.g., "currently 185x5")
- Why it matters (rationale, motivation)

**Length:** 100-200 chars

### 2. Program - Overall Training Strategy

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

### 3. Week - This Week's Schedule

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

### 4. Plan - Today's Specific Workout

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

### Planning Best Practices

- **Goals**: Clear targets with deadlines, priorities, and rationale
- **Program**: Single `current-program` entry, update as strategy evolves
- **Week**: Create at start of week with that week's constraints/adjustments
- **Plan**: Create when scheduling specific workouts (can be day-of or planned ahead)
- **Same key = update**: Creating `current-program` again replaces the old version
- **Flexibility**: Plans are guides - log actual execution in `log` entries
- **Cross-training**: Program should explain how different training types interact
- **Include "why"**: Every level should explain rationale, not just describe what

---

## Content Templates

Ready-to-use templates for each kind. Copy, modify, and use with `fitness-mcp:upsert`.

### Goal Template
```python
fitness-mcp:upsert(
    kind='goal',
    key='p{1|2|3}-{descriptive-goal}',  # e.g., 'p1-bench-225', 'p2-5k-sub20'
    content='{Target outcome}. {Current state if relevant}. {Why if relevant}.'
)
```

### Program Template
```python
fitness-mcp:upsert(
    kind='program',
    key='current-program',
    content='As of {Month Year}: {Primary focus} {frequency}, {secondary focus} {frequency}. Why this balance: {rationale for approach}.'
)
```

### Week Template
```python
fitness-mcp:upsert(
    kind='week',
    key='YYYY-week-NN',  # e.g., '2025-week-43'
    content='Mon: {type}. Tue: {type}. Wed: {type}. Thu: {type}. Fri: {type}. Sat: {type}. Sun: {type}. Why: {adjustments and rationale}.'
)
```

### Plan Template (Before Workout)
```python
fitness-mcp:upsert(
    kind='plan',
    key='YYYY-MM-DD-{type}',  # e.g., '2025-10-29-upper'
    content='[Time] {Type}: {Exercise 1 sets×reps @ load}, {Exercise 2}... Why: {how this helps goals + today\'s rationale}.'
)
```

### Log Template (After Workout)
```python
fitness-mcp:upsert(
    kind='log',
    key='YYYY-MM-DD-{type}',  # e.g., '2025-10-29-upper'
    content='{Type} ({duration}): {Exercise 1 sets×reps @ load RPE}, {Exercise 2}... {Optional: how it felt}.'
)
```

### Knowledge Template
```python
fitness-mcp:upsert(
    kind='knowledge',
    key='{topic}-{specific-focus}',  # e.g., 'knee-health-alignment'
    content='{Specific observation}: {What works/doesn\'t}. Why: {rationale/mechanism}.'
)
```

### Preference Template
```python
fitness-mcp:upsert(
    kind='preference',
    key='{area}-{type}',  # e.g., 'training-style', 'equipment-access'
    content='{Specific preferences and constraints}. Why: {rationale for preferences}.'
)
```

### Metric Template (No Key)
```python
fitness-mcp:upsert(kind='metric', key='', content='{Metric}: {value}{unit}')  # e.g., 'Weight: 71kg'
```

### Note Template (No Key)
```python
fitness-mcp:upsert(kind='note', key='', content='{Observation about training, recovery, or feelings}')
```

---

## Planning Workflows

### Workout Design Workflow (7 Steps)

When client asks for a workout, follow this complete process:

1. **Fetch all relevant info**: `fitness-mcp:overview(context='planning')` - get goals (priority order), program, week, recent plans (5 most recent), all knowledge, all preferences, recent logs (10 most recent)

2. **Ensure current-program is up to date**: Review program freshness (stale if 3+ months old). If strategy doesn't match current goals or recent feedback, propose update → get approval → `fitness-mcp:upsert(kind='program', key='current-program', ...)`

3. **Check week plan**: Ensure week is current and relevant. If outdated or strategy changed, propose update → get approval → `fitness-mcp:upsert(kind='week', key='YYYY-week-NN', ...)`

4. **Think deeply to create optimal workout**: Consider ALL context - knowledge (injuries/limitations), history (recent training), current level (logged performance), preferences (equipment/style). Assume 1hr duration unless client specifies otherwise.

5. **Propose and refine**: Present workout with rationale. Refine based on client feedback until they approve.

6. **Save, then guide**: **Only after approval** → `fitness-mcp:upsert(kind='plan', key='YYYY-MM-DD-{type}', ...)`. Then help guide execution (answer questions, provide cues, adjust on the fly).

7. **Log workout sessions**: After completion, use `fitness-mcp:upsert(kind='log', key='YYYY-MM-DD-{type}', content='...')` - maintains one log per workout that can be updated incrementally

### Program/Week/Plan Creation Workflow

Follow the same propose → approve → save pattern for all planning levels:

#### Creating/Updating Program
1. **Review current state**: `fitness-mcp:overview(context='planning')` to see goals and current program
2. **Propose program**: Present overall strategy linking all goals
3. **Get approval**: Refine based on feedback
4. **Save**: `fitness-mcp:upsert(kind='program', key='current-program', content='As of...')`

#### Creating Weekly Plan
1. **Review context**: Check program and recent training
2. **Propose week**: Layout 7 days with adjustments for constraints
3. **Get approval**: Modify as needed
4. **Save**: `fitness-mcp:upsert(kind='week', key='YYYY-week-NN', content='Mon:...')`

#### Creating Workout Plan
1. **Review everything**: Goals, program, week, knowledge, recent logs
2. **Propose workout**: Detailed exercises with rationale
3. **Get approval**: Adjust based on feedback
4. **Save**: `fitness-mcp:upsert(kind='plan', key='YYYY-MM-DD-{type}', content='...')`

#### Logging Completed Workout
- **User provides completed info**: Save immediately with `fitness-mcp:upsert(kind='log', key='YYYY-MM-DD-{type}', content='...')`
- **Build incrementally**: Same key updates existing log (e.g., adding exercises as completed)

---

## Step-by-Step Workflows

### User Wants Workout
See **Workout Design Workflow** above for the complete 7-step process.

### User Provides Information

**ACTION FIRST: Save immediately, don't wait or discuss:**
- "I have bad knees" → `fitness-mcp:upsert(kind='knowledge', key='knee-health-alignment', content='...')`
- "My trainer says drive knees out" → `fitness-mcp:upsert(kind='knowledge', key='squat-knee-tracking-cue', content='...')`
- "Just did squats 5x5 @ 225" → `fitness-mcp:upsert(kind='log', key='2025-10-29-lower', content='Squats 5x5 @ 225lbs')`
- "I weigh 180" → `fitness-mcp:upsert(kind='metric', key='', content='Weight: 180lbs')`
- "My goal is bench 225" → `fitness-mcp:upsert(kind='goal', key='p1-bench-225', content='Bench 225x5 by [date].')`

### User Asks Question
1. **Call `fitness-mcp:overview` with appropriate context**
   - `fitness-mcp:overview(context='knowledge')` for questions about constraints, preferences, limitations
   - `fitness-mcp:overview(context='upcoming')` for questions about what's next
   - `fitness-mcp:overview(context='history')` for questions about progress, patterns, or past training
   - `fitness-mcp:overview()` for general questions
2. **Call `fitness-mcp:get`** - Pull full details for relevant items if truncated content needs expansion
3. **Answer** with specifics from saved data

**Examples:**
- "How has my squat progressed?" → `fitness-mcp:overview(context='history')` → Analyze log entries
- "What are my current limitations?" → `fitness-mcp:overview(context='knowledge')` → Review knowledge entries
- "What's scheduled for this week?" → `fitness-mcp:overview(context='upcoming')` → Check week/plan entries

### Program/Week/Plan Updates
See **Program/Week/Plan Creation Workflow** above.

**Remember:** The Two-Phase Rule always applies - propose first for YOUR suggestions, save immediately for CLIENT decisions.

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

## Preference Templates

Preferences define how you like to train (style, timing, equipment, recovery). All should include "Why" to explain rationale.

**Template:**
```
[Area description with specifics]. Why: [Rationale for these preferences].
```

**Examples:**
```
training-style:
Calisthenics-first approach: Prioritize bodyweight progressions over barbell work. Key movements: freestanding HSPU, archer ring push-ups, ring dips, weighted pull-ups. Use barbells/weights only when bodyweight doesn't provide adequate stimulus (legs, posterior chain). Why: Skill development, joint health, training enjoyment.

recovery-protocols:
Sauna: Post-workout 2-3x/week, 20-30min, avoid before strength. Cold exposure: Separate from strength by 4+ hours (may blunt adaptation), fine with endurance. Sleep: 7-8 hours priority. Nutrition: Not fasted for key sessions, protein within 2hr post-workout. Why: Evidence-based timing to support adaptation.

weekly-structure:
Train 6 days/week: Mon (VO2 intervals), Tue (home strength), Wed (yoga/mobility), Thu (zone-2), Fri (gym strength), Sat (long run/hike/acro), Sun (recovery/skill). Why: Polarized intensity distribution (hard days hard, easy days easy) with embedded recovery and skill work for sustainable progression.
```

**Avoid:**
- Markdown formatting (bold, bullets, headers) - use plain text
- Excessive newlines for visual formatting
- Redundant labels (e.g., "Recovery Preferences:" when key is `recovery-protocols`)
- Current state info (e.g., "currently 4x5") - belongs in goals, not preferences
