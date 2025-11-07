---
name: fitness-coaching
description: Use for saving workout data (logs, plans, goals, programs), managing fitness preferences and user-specific knowledge, and answering fitness questions. Load PROGRAM.md/WEEK.md/WORKOUT.md for creating programs/weeks/workouts. Provides MCP database tools and progressive access to programming workflows, coaching philosophy, and domain-specific knowledge.
---

# Fitness Coaching

**What This Skill Does:**
- Manages fitness data (goals, programs, workouts, knowledge) via MCP database
- Provides 4 tools for saving/retrieving data: `upsert`, `overview`, `get`, `archive`
- Tracks 4-level hierarchy: Goals → Program → Week → Plan

**This file contains:**
- Tool usage and data structure reference
- When to save vs propose (critical rules)
- Naming conventions and content guidelines

**For creating programs and workouts, load:**
- **PROGRAM.md** - Creating overall training program strategy
- **WEEK.md** - Planning weekly training schedule
- **WORKOUT.md** - Creating individual workouts and plans
- **COACHING.md** - Philosophy and decision-making frameworks
- **knowledge/*.md** - Domain-specific expertise (knee health, exercise selection, etc.)

---

## System Overview (Big Picture)

**Core Approach**: Track fitness data in 4 hierarchical levels:
1. **Goals** - Long-term targets (e.g., "Bench 225 by June")
2. **Program** - Overall strategy (e.g., "Strength 4x/week + running 3x/week")
3. **Week** - This week's schedule (e.g., "Mon: Upper, Tue: Run, Wed: Lower...")
4. **Plan** - Today's workout (e.g., "Bench 4x10 @ 185, OHP 3x12...")

**User specific details are stored in database** via 4 MCP tools:
- `fitness-mcp:overview` - Scan data (context-aware)
- `fitness-mcp:get` - Fetch full details
- `fitness-mcp:upsert` - Create/update ALL data
- `fitness-mcp:archive` - Hide old data

**Database stores**:
- User-specific goals, workouts, metrics, preferences
- Personal limitations and injury history
- Completed workout logs

**This skill provides**:
- How to use tools to save/retrieve data (this file)
- Program/week/workout creation workflows (PROGRAM.md, WEEK.md, WORKOUT.md)
- Coaching principles and expertise (COACHING.md)
- Domain expertise (knowledge/*.md files)

---

## 🎯 Critical Rules: When to Save vs Propose

**ALWAYS act on these principles:**

1. **Thoroughness Before Suggestions**: NEVER propose a workout without reviewing ALL saved context (knowledge, recent workouts, current program, preferences)
2. **Save User Info Immediately**: When client shares completed workouts, goals, limitations, or decisions → save right away
3. **Propose Before Saving Your Ideas**: When YOU suggest a workout/plan → propose first, save only after client agrees
4. **Keep Data Current**: Review program freshness at session start - update if stale (3+ months) or strategy changed. Proactively ask to fill gaps, update outdated info, maintain accurate records

**The pattern:** Client provides = save now. You suggest = propose first, then save.

---

## 📁 Load Files Based on Task

**Creating overall training program:**
→ Load PROGRAM.md (program strategy, integrating multiple goals, concurrent training)

**Planning weekly schedule:**
→ Load WEEK.md (weekly planning, balancing training across 7 days, adjusting for constraints)

**Creating individual workout:**
→ Load WORKOUT.md (7-step workflow, plan templates, data fetching rules)

**Making coaching decisions or explaining "why":**
→ Load COACHING.md (principles, philosophy, decision frameworks)

**Domain-specific questions:**
→ Load knowledge/*.md as needed (knee health, exercise selection, periodization, etc.)

**Simple data entry (logging, saving user info):**
→ Use tools documented in this file (no additional files needed)

---

## 🔑 Core Concepts

### Plan vs Log: Critical Distinction

| Type | When | Purpose | Example |
|------|------|---------|------------|
| **Plan** | BEFORE workout | What you intend to do | `fitness-mcp:upsert(kind='plan', key='2025-10-29-upper', content='6am Upper: Bench 4x10 @ 185...')` |
| **Log** | AFTER workout | What you actually did | `fitness-mcp:upsert(kind='log', key='2025-10-29-upper', content='Upper (52min): Bench 4x10 @ 185 RPE 7...')` |

Both use `fitness-mcp:upsert` with date-based keys for easy updates. Plans use future-looking language, logs use completion language.

---

## 📊 Planning Hierarchy Overview

Plan training at four levels, from broadest to most specific:

| Level | Scope | Key Example | What It Answers |
|-------|-------|-------------|-----------------|
| **Goal** | Long-term target | `p1-bench-225` | What do I want to achieve? |
| **Program** | 2-12 months | `current-program` | How do all my goals fit together? |
| **Week** | 7 days | `2025-week-43` | What's the plan for this week? |
| **Plan** | Single workout | `2025-10-22-strength` | What am I doing today? |

**For detailed examples and templates**: Read PROGRAM.md (program), WEEK.md (week), or WORKOUT.md (plan/log)

---

## 🎯 The 4 MCP Tools

### 1. `fitness-mcp:overview` - Context-Aware Scan
Quick scan of relevant data based on what you're doing.

**When to use:** Start of EVERY session with appropriate context

**Returns:** Context-filtered active items (content truncated to 200 words for verbose kinds)

**Contexts:**
- **`planning`**: Comprehensive view for programming workouts
  - Returns: goals (priority order), program, week, recent plans (5 most recent), all preferences, all knowledge, recent logs (10 most recent)
  - Use when: Creating programs/weeks/workouts (load PROGRAM/WEEK/WORKOUT.md), reviewing program context
- **`upcoming`**: Focus on near-term plans
  - Returns: goals, week, recent plans (5 most recent), recent logs (7 most recent)
  - Use when: Client asks "what's next?"
- **`knowledge`**: Review constraints and preferences
  - Returns: goals, program, preferences, knowledge
  - Use when: Client asks questions, reviewing limitations
- **`history`**: Full training history for progress review
  - Returns: goals, all logs, all metrics (up to 500 entries)
  - Use when: Client asks about progress, patterns, or wants to review past training
- **No context (default)**: All active data

```python
# Get comprehensive context (use with PROGRAM/WEEK/WORKOUT.md workflows)
fitness-mcp:overview(context='planning')

# Check what's coming up
fitness-mcp:overview(context='upcoming')

# Review constraints and preferences
fitness-mcp:overview(context='knowledge')

# Review entire training history
fitness-mcp:overview(context='history')

# See everything (default)
fitness-mcp:overview()
```

### 2. `fitness-mcp:get` - Retrieve Full Details
Fetch complete content for specific items or filtered lists.

**Two modes:**
1. **Specific items:** `fitness-mcp:get(items=[{'kind': 'knowledge', 'key': 'knee-issue'}])`
2. **Filtered lists:** `fitness-mcp:get(kind='log', limit=10)`

**Parameters:**
- `items`: List of specific items by kind/key
- `kind`: Filter by type (e.g., 'log', 'knowledge')
- `status`: Filter by status (e.g., 'active', 'archived')
- `start`/`end`: Date filters for events
- `limit`: Maximum number of results (default 100)

```python
# Get full content for specific items seen in overview
fitness-mcp:get(items=[
    {'kind': 'knowledge', 'key': 'knee-issue'},
    {'kind': 'goal', 'key': 'bench-225'}
])

# List recent logs
fitness-mcp:get(kind='log', start='2025-01-01', limit=10)

# Get all active goals
fitness-mcp:get(kind='goal', status='active')
```

### 3. `fitness-mcp:upsert` - Create/Update All Entries
Universal tool for all data entry. Handles both keyed items and keyless events.

**For items with keys** (goal, program, week, plan, log, knowledge, preference):
- Same key = update existing item
- Before creating, check if similar entry exists in overview

**For events without keys** (metric, note):
- Use empty string `''` for key
- Each call creates a new immutable entry

**Parameters:**
- `kind`: Type of entry (goal, program, week, plan, log, knowledge, preference, metric, note)
- `key`: Unique identifier (use `''` for metrics/notes)
- `content`: Main description/text (**put everything here as natural text**)
- `status`: Optional ('active' or 'archived')
- `old_key`: Optional - rename an entry from old_key to key

```python
# Goal with priority in key
fitness-mcp:upsert(kind='goal', key='p1-bench-225', content='Bench 225x5 by June.')

# Log (one per workout, can update)
fitness-mcp:upsert(kind='log', key='2025-10-29-upper', content='Upper: Bench 4x10 @ 185, OHP 3x12 @ 115')

# Metric (no key - use empty string)
fitness-mcp:upsert(kind='metric', key='', content='Weight: 71kg')

# Note (no key - use empty string)
fitness-mcp:upsert(kind='note', key='', content='Knee felt tight during warmup')

# Knowledge
fitness-mcp:upsert(kind='knowledge', key='knee-health-alignment', content='Keep knees tracking over toes...')
```

**Important - Metrics:** Store **one metric per entry** for better trend tracking.

### 4. `fitness-mcp:archive` - Remove From View
Hide outdated items while keeping history.

**When to use:** Remove old goals, plans, or knowledge from active view

**Parameters:**
- `kind`: Type to archive
- `key`: Specific item key (optional for bulk)
- `event_id`: Event ID to archive

```python
fitness-mcp:archive(kind='goal', key='old-goal')     # Archive specific item
fitness-mcp:archive(kind='preference')                # Archive all preferences
```

---

## 📋 Naming Conventions

**Universal Rules:**
- **kebab-case only** (`bench-225` not `bench_225` or `benchPress225`)
- **No abbreviations** (`week-1` not `wk1`, `squat-progression` not `squat-prog`)
- **No underscores** except in ISO dates
- **Descriptive keys** (`knee-health-alignment` not `knee-issue`)

**Key Patterns by Kind:**
- `goal`: `p{1|2|3}-{descriptive-goal}` → `p1-bench-225`, `p2-5k-sub20`, `p1-pain-free-squat`
- `program`: Always `current-program` (single living document)
- `week`: `YYYY-week-NN` → `2025-week-43` (ISO week 01-53)
- `plan`: `YYYY-MM-DD-{type}` → `2025-10-22-strength`, `2025-10-22-run`
- `knowledge`: `{topic}-{specific-focus}` → `knee-health-alignment`, `squat-depth-cue-spread-floor`
- `preference`: `{area}-{type}` → `training-style`, `equipment-access`, `workout-timing`
- `log`: `YYYY-MM-DD-{type}` → `2025-10-29-upper` (when using upsert for one log per workout)
- `metric/note`: **No key** (events identified by UUID)

**Content Must Include "Why":**
Every entry should explain rationale, not just describe what/how. It should be concise, don't include obvious information.

---

## 📋 Content Structure Reference

| Kind | Key Pattern | Content Length | Example with "Why" |
|------|-------------|----------------|--------------------|
| **goal** | `p{1|2|3}-{descriptive-goal}` | 20-50 words | "Bench 225x5 by June. Currently 185x5. Foundation for rugby strength." |
| **program** | `current-program` | 80-150 words | "As of Oct 2025: Strength primary 4x/week (bench-225, squat-315), running secondary 3x/week (20-25mpw). Why: Rugby season April needs strength peak. Daily hip mobility - consistency > intensity." |
| **week** | `YYYY-week-NN` | 50-100 words | "Mon: Upper. Tue: Easy run. Wed: Lower. Thu: OFF (travel). Fri: Tempo. Sat: Full body (extra volume). Sun: Long run. Why: Travel Thu means 6 sessions not 7, compensate Sat." |
| **plan** | `YYYY-MM-DD-{type}` | 40-80 words | "6am Upper: Bench 4x10 @ 185 (volume for bench-225), OHP 3x12 @ 115 (shoulder health), rows 3x12. Why: Hypertrophy phase. OHP light due to shoulder tweak." |
| **log** | `YYYY-MM-DD-{type}` | One line + brief note | "Upper (52min): Bench 4x10 @ 185 RPE 7, OHP 3x12 @ 115 RPE 6. Felt strong, good pump." |
| **knowledge** | `{topic}-{specific-focus}` | 30-60 words | "Knee alignment: avoid narrow stance. Wider stance + 'spread floor' cue eliminates pain. Started Sept 2024. Why it works: Activates glute med, prevents knee cave." |
| **preference** | `{area}-{type}` | 100-200 words | "Train mornings 6-7am, prefer upper/lower split, avoid leg press (knee issue), love Romanian deadlifts. Why: Morning energy best, injury history guides exercise selection..." |
| **metric** | *(no key - event)* | 5-20 words | "Weight: 71kg" (one metric per entry for trend tracking) |
| **note** | *(no key - event)* | 10-50 words | "Knee felt tight during warmup, loosened up by set 3. May need extra mobility work this week." |

**Principles:**
- **Be concise**: Keep entries short and focused (see length guidelines above). Strip unnecessary words
- **Include "why"**: Every entry should explain rationale, not just describe what/how
- **Put EVERYTHING in content**: No structured fields needed - dates, priorities, context all in natural text
- **Keys are kebab-case**: goal (`p1-bench-225`), program (`current-program`), week (`2025-week-43`), plan (`2025-10-22-upper`), knowledge (`knee-health-alignment`), preference (`training-style`)
- **Logs AND plans use keys**: Both use `fitness-mcp:upsert(kind='log'/'plan', key='YYYY-MM-DD-type')` for easy updates
- **Metrics/notes have NO key**: Use `fitness-mcp:upsert` with empty string key - identified by UUID only

---

## Knowledge Storage: Specific, Not Generic

**Store the WHAT/HOW/WHY in concise, actionable form. Not textbook knowledge.**

### ❌ DON'T Store Vague or Common Knowledge
```
"Progressive overload is important"  # Too generic
"Galpin recommends Zone 2 cardio"  # Missing specifics
"Squats are a compound movement"  # You know this
"Protein helps recovery"  # No actionable detail
```

### ✅ DO Store Specific, Actionable Insights
```python
fitness-mcp:upsert(
    kind='knowledge',
    key='vo2-galpin-3x3-protocol',
    content='Galpin 3x3: 3min all-out, 3min rest, 3 rounds. Once/week max. Boosts VO2 max 8-10% in 6wks.'
)

fitness-mcp:upsert(
    kind='knowledge',
    key='squat-depth-cue-spread-floor',
    content='Depth issue solved: "Spread floor" cue > "knees out". Activates glute med without knee cave. +20lbs instantly.'
)

fitness-mcp:upsert(
    kind='knowledge',
    key='shoulder-impingement-right',
    content='Right shoulder clicks at 90°. Cause: Side sleeping. Fix: Band pull-aparts 2x20 before pressing. Avoid: Dips, overhead press.'
)
```

**Naming:** Use descriptive, specific keys (`vo2-galpin-3x3-protocol` not just `galpin-protocol`).

### What to Capture (Under 50 Words Each)
- **Specific protocols**: "3x3min intervals at 95% HR, once weekly"
- **Exact cues that work**: "Push the floor away" not just "leg drive"
- **Numbers and thresholds**: "152bpm lactate threshold" not "Zone 2"
- **Cause and effect**: "Knee pain from narrow stance → widened 2 inches → resolved"
- **Expert specifics**: "Galpin: 6-second eccentrics for Type I dominant athletes"

---

## Handling Incremental Workout Updates

When users provide workout info piece by piece:

```
User: "Just did squats 5x5 at 225"
→ fitness-mcp:upsert(kind='log', key='2025-10-29-lower', content='Squats 5x5 @ 225lbs')

User: "Also did bench press 3x8 at 185" (same session)
→ fitness-mcp:upsert(kind='log', key='2025-10-29-lower', content='Squats 5x5 @ 225lbs, Bench 3x8 @ 185lbs')

User: "Yesterday I did deadlifts"
→ fitness-mcp:upsert(kind='log', key='2025-10-28-lower', content='Deadlifts...')
```

**Rule:** Use date-based keys for workout logs. Same date+type key → updates existing. Different date → new entry.

---

## Tool Usage Examples

### Log Complete Workouts (Everything in Content)
```python
# Use upsert with date-based key for workout logs (one log per workout)
fitness-mcp:upsert(
    kind='log',
    key='2025-10-29-lower',
    content='Lower (52min): Squats 5x5 @ 245lbs RPE 7, RDL 3x8 @ 185lbs RPE 6, Leg curl 3x12 @ 50kg RPE 8'
)

# Use upsert with empty key for metrics and notes
fitness-mcp:upsert(kind='metric', key='', content='Weight: 71kg')
fitness-mcp:upsert(kind='note', key='', content='Knee felt tight during warmup')
```

### Fix Mistakes After the Fact
```python
# For workout logs - just upsert again with same key
fitness-mcp:upsert(kind='log', key='2025-10-29-lower', content='Corrected: Squats 5x5 @ 255lbs RPE 7, RDL...')

# For metrics/notes - cannot update (immutable events)
# Must create new entry with corrected value
fitness-mcp:upsert(kind='metric', key='', content='Corrected: Weight 72kg')
```

### Handle Contradicting Information
When new advice contradicts old, update (don't delete):
```python
fitness-mcp:upsert(
    kind='knowledge',
    key='squat-depth-guidance',
    content='UPDATE: Coach says parallel is fine for me. Previous ATG recommendation causing knee stress. Changed Oct 2024.'
)
```

**Naming:** Keep keys descriptive (`squat-depth-guidance` includes context about what it is).

---

## Quick Reference

```
User shares info → Save immediately
User asks question → fitness-mcp:overview(context='knowledge'|'history'|'upcoming') → get details if needed → Answer
User wants program → Load PROGRAM.md
User wants weekly plan → Load WEEK.md
User wants workout → Load WORKOUT.md (7-step workflow)
Plans need adjustment → Update immediately when agreed
Workout provided piecemeal → Update same entry via key
Found a mistake → Update by key (same key = replace)
Old data no longer relevant → fitness-mcp:archive (don't delete)
```

**Remember:**
- Same key = update
- Archive don't delete
- Everything in content as natural text
- Propose first, save after approval
- Fetch ALL knowledge for safety
- Follow naming conventions (kebab-case keys)

---

## Where Everything Lives

**In Database** (user-specific data):
- Goals: `kind='goal'`, key=`p1-bench-225`
- Program: `kind='program'`, key=`current-program` (single living document)
- Week: `kind='week'`, key=`2025-week-43`
- Plan: `kind='plan'`, key=`2025-10-29-upper`
- Log: `kind='log'`, key=`2025-10-29-upper` (completed workouts)
- Knowledge: `kind='knowledge'` (user-specific observations only - NOT general fitness knowledge)
- Preference: `kind='preference'` (equipment, style, timing)
- Metric: `kind='metric'` (point-in-time measurements)
- Note: `kind='note'` (observations)

**In This Skill** (general expertise):
- Tool usage → This file (SKILL.md)
- Programming workflows → PROGRAMMING.md
- Coaching philosophy → COACHING.md
- Domain knowledge → knowledge/*.md files
