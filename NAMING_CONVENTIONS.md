# Naming Conventions

Strict naming and content structure rules for the fitness MCP server. These conventions ensure data consistency, searchability, and clarity.

---

## Key Naming Rules (Items with Identity)

### General Format: `{category}-{specific-name}`

**Universal Rules:**
- **Kebab-case only** (lowercase with hyphens)
- **No underscores** (except in ISO date format)
- **No abbreviations** (write `week-1` not `wk1`)
- **Descriptive over cryptic** (`bench-progression` not `bench-prog`)
- **Exercise names first** for progressions (`squat-8wk-linear` not `linear-squat`)

---

## By Kind: Key Patterns

### `goal` - What you want to achieve

**Pattern:** `{exercise/outcome}-{target}` or `{activity-domain}`

**Examples:**
- ✅ `bench-225` - Bench press 225lbs
- ✅ `squat-315` - Squat 315lbs
- ✅ `one-arm-pullup` - Achieve one-arm pull-up
- ✅ `5k-sub20` - Run 5k under 20 minutes
- ✅ `bulletproof-knee-health` - Pain-free knees with excellent mechanics
- ✅ `mountain-biking` - Get back on trails regularly

**Anti-patterns:**
- ❌ `5k-pr` → Use `5k-sub20` (specific target)
- ❌ `benchPress225` → Use `bench-225` (kebab-case)
- ❌ `bench_press_goal` → Use `bench-225` (no underscores, no redundant "goal")

---

### `program` - Overall training strategy

**Pattern:** `current-program` (single living document)

**Examples:**
- ✅ `current-program` - The one and only overall training strategy

**Anti-patterns:**
- ❌ `program-oct-2025` → Use `current-program` (single entry, update as needed)
- ❌ `strength-program` → Use `current-program` (one program covers all goals)
- ❌ `hybrid-program` → Use `current-program` (don't create multiple programs)

**Content:** 80-150 words explaining which goals are prioritized, how training types balance, why this approach, cross-training considerations.

---

### `week` - This week's training schedule

**Pattern:** `YYYY-week-NN` (ISO week format, 01-53)

**Examples:**
- ✅ `2025-week-43` - Week 43 of 2025 (ISO week)
- ✅ `2025-week-01` - Week 1 of 2025
- ✅ `2025-week-52` - Week 52 of 2025

**Anti-patterns:**
- ❌ `week-oct-20` → Use `2025-week-43` (ISO week number)
- ❌ `2025-10-20-week` → Use `2025-week-43` (ISO week format)
- ❌ `wk43-2025` → Use `2025-week-43` (no abbreviations, year first)

**Content:** 50-100 words with daily schedule, deviations from program (travel/fatigue/injury), rationale for adjustments, context about phase.

---

### `session` - Specific planned workout

**Pattern:** `YYYY-MM-DD-{type}` where type is training modality

**Examples:**
- ✅ `2025-10-22-strength` - Strength session on Oct 22, 2025
- ✅ `2025-10-22-run` - Running session on Oct 22, 2025
- ✅ `2025-01-16-mobility` - Mobility session on Jan 16, 2025
- ✅ `2025-01-16-yoga` - Yoga session on Jan 16, 2025

**Anti-patterns:**
- ❌ `2025-10-22` → Use `2025-10-22-strength` (include training type)
- ❌ `oct-22-strength` → Use `2025-10-22-strength` (ISO date format)
- ❌ `2025-10-22-upper` → Use `2025-10-22-strength` (type, not split name)

**Content:** 40-80 words with time, exercises/workout details, sets/reps or duration/pace, which goals this supports, rationale for choices.

---

### `knowledge` - Personal insights, protocols, and learnings

**Pattern:** `{topic}-{specific-focus}`

**Examples:**
- ✅ `knee-health-alignment` - Knee alignment practices
- ✅ `ankle-mobility-protocols` - Ankle mobility protocols
- ✅ `collagen-vitamin-c-protocol` - Collagen supplementation protocol
- ✅ `meniscus-tear-history-2024` - Meniscus tear injury history
- ✅ `squat-depth-update-oct-2024` - Updated squat depth guidance
- ✅ `concurrent-training-management` - Managing concurrent training

**Anti-patterns:**
- ❌ `mcp-knee-health` → Use `knee-health-alignment` (no "mcp" prefix)
- ❌ `knee-health` (duplicate entries) → Use specific keys like `knee-health-alignment`, `knee-health-mechanics`
- ❌ `kb-ankle-mob` → Use `ankle-mobility-protocols` (no abbreviations)

---

### `preference` - Training preferences and constraints

**Pattern:** `{area}-{type}`

**Examples:**
- ✅ `training-style` - Overall training style preference
- ✅ `weekly-structure` - Weekly training structure
- ✅ `workout-timing` - Preferred workout times
- ✅ `equipment-access` - Available equipment
- ✅ `mobility-practices` - Preferred mobility work
- ✅ `recovery-protocols` - Recovery preferences

**Anti-patterns:**
- ❌ `pref-1` → Use `training-style` (descriptive, not numbered)
- ❌ `workout_timing` → Use `workout-timing` (kebab-case)

---

### `principle` - Training principles and concepts

**Pattern:** `{concept-name}`

**Examples:**
- ✅ `progressive-overload` - Progressive overload principle
- ✅ `autoregulation` - Training autoregulation
- ✅ `deload-protocol` - Deload strategies
- ✅ `80-20-polarization` - 80/20 training polarization
- ✅ `exercise-ordering-fast-first` - Exercise ordering principles
- ✅ `connective-tissue-adaptation` - Tendon/connective tissue adaptation

**Anti-patterns:**
- ❌ `prog-overload` → Use `progressive-overload` (no abbreviations)
- ❌ `deload` → Use `deload-protocol` (be specific about what it is)

---

### `current` - Current state/metrics/status

**Pattern:** `{metric-name}` or `{exercise}-{metric}`

**Examples:**
- ✅ `bodyweight` - Current bodyweight
- ✅ `vo2-max-estimate` - Current VO2 max estimate
- ✅ `hrv-recovery` - Current HRV status
- ✅ `squat-max` - Current squat 1RM
- ✅ `deadlift-max` - Current deadlift working weights
- ✅ `weighted-pullup-performance` - Current weighted pull-up capacity
- ✅ `5k-pace-estimate` - Estimated 5k race pace

**Anti-patterns:**
- ❌ `5k-pace` → Use `5k-pace-estimate` (clarify it's an estimate)
- ❌ `bw` → Use `bodyweight` (no abbreviations)

---

### `strategy` - Long-term or short-term strategies

**Pattern:** `{timeframe}` or `{timeframe}-{focus}`

**Examples:**
- ✅ `long-term` - Long-term strategy
- ✅ `short-term` - Short-term strategy
- ✅ `q1-2025-strength` - Q1 2025 strength focus
- ✅ `2025-hybrid-athlete` - 2025 hybrid athlete development

**Anti-patterns:**
- ❌ Multiple entries with same `long-term` or `short-term` key → Use more specific keys or update existing

---

## Events (No Key Required)

Events (`workout`, `metric`, `note`) use **NO KEY** - they are identified by UUID and timestamped via `occurred_at`.

**Content is free-form** but should follow content structure rules below.

---

## Content Structure Rules

All content should start with a **concise summary**, followed by optional structured details.

### `goal`

**Format:** `{Target} ({Current state}). Priority: {High/Med/Low}. Why: {Rationale}`

**Example:**
```
Bench 225x5 by June (currently 185x5). Priority: High. Why: Foundation for rugby - need upper body strength for scrums and tackles.
```

**Length:** 20-50 words

---

### `program`

**Format:** `{Timeframe} strategy: {Training balance across goals}. Why: {Rationale for approach}`

**Example:**
```
Oct-Dec strategy: Strength primary (bench-225, squat-315 goals) 4x/week, running secondary 3x/week (20-25mpw maintains base for sub-20-5k). Daily hip mobility (hip-mobility goal). Why: Rugby season April needs strength peak. Hip work daily because consistency > intensity for mobility.
```

**Length:** 80-150 words

---

### `week`

**Format:** `{Daily schedule}. Why: {Rationale for this week's adjustments/context}`

**Example:**
```
Mon: Upper strength. Tue: Easy run 5mi. Wed: Lower strength. Thu: OFF (traveling). Fri: Tempo run 4mi. Sat: Full body (extra volume). Sun: Long run 8mi. Why: Thu travel means 6 sessions not 7. Compensating with Sat volume increase. Week 2 of current strength phase.
```

**Length:** 50-100 words

---

### `session`

**Format:** `{Time} {Focus}: {Exercises/workout details}. Why: {Rationale for choices}`

**Example:**
```
6am Upper: Bench 4x10 @ 185 RPE 8 (volume for bench-225 goal), OHP 3x12 @ 115 (shoulder health), Rows 3x12 @ 70 (balance pressing). Why: Hypertrophy phase building muscle for later strength work. OHP light due to previous shoulder tweak.
```

**Length:** 40-80 words

---

### `knowledge`

**Format:**
```
{Topic}: {Specific finding/protocol}

{Details/Context}: ...
```

**Example:**
```
Knee alignment: Wider stance + "spread floor" cue eliminates pain.

Context: Narrow stance caused medial knee stress. Changed Sept 2024 after meniscus recovery.
```

**Key principle:** Store **user-specific observations only**, not general fitness knowledge the LLM already knows.

**Length:** 20-50 words (concise, actionable)

---

### `preference`

**Format:**
```
{Preference statement}

{Details}: ...
```

**Example:**
```
Calisthenics-first approach: Prioritize bodyweight progressions over barbell work.

Home: rings, pull-up bar, dumbbells. Office gym: full equipment Wed/Thu.
```

**Length:** 100-200 words (can be more detailed)

---

### `principle`

**Format:**
```
{Principle name}: {Core concept}

{Application}: ...
```

**Example:**
```
Progressive overload: Gradual increases in load, volume, or intensity.

Application: +5lbs/week on compounds, +1-2 reps on calisthenics progressions.
```

**Length:** 50-100 words

---

### `current`

**Format:** `{Current value/status with context}`

**Examples:**
```
180 lbs
```

```
Back squat: Max 80kg, training @ 60kg for 4x6 (70-75% intensity)
```

**Length:** 5-30 words

---

### `strategy`

**Format:** `{Strategic direction statement}`

**Example:**
```
Develop hybrid athlete profile: strong, mobile, and enduring. Balance strength mesocycles with consistent endurance base (80/20 polarization).
```

**Length:** 30-100 words

---

### Events: `workout`, `metric`, `note`

**Format:** Natural language, one-line summaries for workouts

**workout example:**
```
Lower (52min): Squats 5x5 @ 245lbs RPE 7, RDL 3x8 @ 185lbs RPE 6, Leg curl 3x12 @ 50kg RPE 8
```

**metric example:**
```
Bodyweight: 180 lbs, 15% bodyfat
```

**note example:**
```
Felt fatigued today, reduced training volume by 20%. HRV was 65ms (low).
```

---

## Quick Reference Table

| Kind | Key Pattern | Content Start | Length |
|------|-------------|---------------|--------|
| `goal` | `{exercise/outcome}-{target}` | Target (Current). Priority: X. Why: | 20-50 words |
| `program` | `current-program` | Timeframe strategy: Training balance. Why: | 80-150 words |
| `week` | `YYYY-week-NN` | Daily schedule. Why: | 50-100 words |
| `session` | `YYYY-MM-DD-{type}` | Time Focus: Exercises. Why: | 40-80 words |
| `knowledge` | `{topic}-{specific-focus}` | Topic: Finding. Why it works: | 30-60 words |
| `preference` | `{area}-{type}` | Preference statement. Why: | 100-200 words |
| `principle` | `{concept-name}` | Principle: Concept | 50-100 words |
| `current` | `{metric-name}` | Current value | 5-30 words |
| `strategy` | `{timeframe}` or `{timeframe}-{focus}` | Strategic direction | 30-100 words |
| `workout` | **(no key)** | Session: Exercises | One line |
| `metric` | **(no key)** | Metric: Value | 5-20 words |
| `note` | **(no key)** | Observation | 10-50 words |

---

## Data Cleanup Checklist

Use this checklist when reviewing existing data:

- [ ] **Keys use kebab-case** (no underscores, no camelCase)
- [ ] **No abbreviations** in keys (`week-01` not `wk1`)
- [ ] **program key is `current-program`** (single living document)
- [ ] **week uses ISO week format** (`2025-week-43`)
- [ ] **session includes date and type** (`2025-10-22-strength`)
- [ ] **No duplicate keys** within same kind
- [ ] **Content includes "why"** (rationale, not just what/how)
- [ ] **Content length appropriate** for kind (see table above)
- [ ] **No generic knowledge** (user-specific observations only)
- [ ] **Events (workout/metric/note) have NULL keys**

---

## Migration Guide

When renaming existing entries:

1. **Identify problematic keys** (abbreviations, underscores, duplicates)
2. **Create new entries** with proper keys using `upsert`
3. **Archive old entries** using `archive(kind, key)`
4. **Verify no data loss** by checking `get(kind)`

Example migration:
```python
# Old: knowledge with key "mcp-knee-health" (vague, prefixed)
# New: Split into specific entries
upsert(kind='knowledge', key='knee-health-alignment', content='...')
upsert(kind='knowledge', key='knee-health-mechanics', content='...')
archive(kind='knowledge', key='mcp-knee-health')
```

---

## Validation Rules (Future Enhancement)

Consider adding pre-save validation in MCP tools:

1. **Key format validation** - Regex check for kebab-case
2. **Content length warnings** - Alert if content exceeds recommended length
3. **Duplicate key detection** - Warn before overwriting existing item
4. **Required fields** - Ensure all required fields present

---

## Philosophy: Everything in Content

**Put EVERYTHING in the content field as natural text.**

- Dates, deadlines: "Due: 2025-12-31" in content
- Tags: "Tags: injury-prevention, squat-form" in content
- Relationships: "Part of squat-progression plan" in content
- Progress: "Week 3 of 8" in content

**Why?** Simplicity, searchability, and flexibility. No need for complex structured data.
