# Temporal Context & Progress Tracking Implementation

## Summary

Implemented temporal context for plans and progress tracking for goals based on critical feedback from fitness coach LLM. The solution follows the system's elegant design philosophy: **flexible storage, smart queries, computation on-read**.

## Changes Made

### 1. Temporal Context for Plans (HIGH Priority) ✅

**Problem:** Coaches couldn't immediately see "where are we in the plan?" - had to mentally calculate current week, progress, etc.

**Solution:** Compute temporal context on-read when plans have `start_date` and `duration_weeks` in attrs.

**Implementation:**
- Added `_compute_plan_temporal_context()` function in [crud.py](src/memory/crud.py#L437-L478)
- Enhanced `get_overview()` to compute and inject temporal fields for plans ([crud.py:530-547](src/memory/crud.py#L530-L547))
- **No schema changes** - uses existing `attrs` JSONB field

**Computed Fields:**
```python
{
    'current_week': 3,           # Which week (0-6 days = week 1, 7-13 = week 2, etc.)
    'total_weeks': 6,            # Total plan duration
    'weeks_remaining': 4,        # How many weeks left
    'progress_pct': 50,          # Progress percentage (0-100, capped)
    'temporal_status': 'active', # 'pending', 'active', or 'completed'
    'days_elapsed': 14           # Days since start_date
}
```

**Example Usage:**
```python
# LLM creates plan with temporal attrs
upsert_item(
    kind='plan',
    key='squat-progression',
    content='8-week linear progression...',
    attrs={
        'start_date': '2025-09-15',  # When plan begins
        'duration_weeks': 8           # Total duration
    }
)

# Overview automatically shows temporal context
overview = get_overview()
# plan will include: current_week=3, progress_pct=37, temporal_status='active'
```

### 2. Goal Progress Tracking (MEDIUM Priority) ✅

**Problem:** Goals were static targets with no visibility into progress from baseline to target.

**Solution:** Document attrs pattern for baseline/target, derive current progress from workout logs.

**Implementation:**
- Added documentation to [FITNESS_COACH_INSTRUCTIONS.md](FITNESS_COACH_INSTRUCTIONS.md#L285-L339)
- Updated `describe_conventions()` in [mcp_server.py](src/mcp_server.py#L772-L798)
- **No schema changes** - uses existing `attrs` JSONB field

**Pattern:**
```python
upsert_item(
    kind='goal',
    key='weighted-pullup-40kg',
    content='Weighted pull-up +40kg x5 reps',
    attrs={
        'baseline': {
            'value': '+30kg x7',
            'date': '2025-09-15',
            'notes': 'Tested 1RM conversion: ~35kg'
        },
        'target': {
            'value': '+40kg x5',
            'date': '2025-12-01'
        }
    }
)

# LLM derives current from recent workouts
recent = list_events(kind='workout', tag_contains='pull-up', limit=10)
# Analyzes: "Baseline: +30kg → Current: +35kg → Target: +40kg (50% there!)"
```

### 3. Contraindication Documentation (LOW Priority) ✅

**Problem:** Injury/limitation info scattered in free text, hard to systematically check.

**Solution:** Document structured tagging and attrs conventions for contraindications.

**Implementation:**
- Added contraindication section to [FITNESS_COACH_INSTRUCTIONS.md](FITNESS_COACH_INSTRUCTIONS.md#L341-L396)
- Updated `describe_conventions()` with contraindication patterns ([mcp_server.py:800-805](src/mcp_server.py#L800-L805))
- **No schema changes** - existing features, just better documentation

**Pattern:**
```python
upsert_item(
    kind='knowledge',
    key='shoulder-impingement-oct-2025',
    content='Right shoulder impingement: avoid overhead pressing >45°...',
    tags='contraindication shoulder overhead-press injury-active',
    attrs={
        'affected_exercises': ['overhead press', 'military press', 'HSPU'],
        'safe_alternatives': ['incline press', 'landmine press'],
        'retest_date': '2025-11-01',
        'severity': 'moderate'
    }
)

# LLM checks contraindications when programming
limitations = list_items(kind='knowledge', tag_contains='contraindication injury-active')
avoid_list = [ex for lim in limitations for ex in lim['attrs']['affected_exercises']]
```

### 4. Testing ✅

**Added:** [tests/test_temporal_context.py](tests/test_temporal_context.py)
- 9 unit tests for `_compute_plan_temporal_context()`
- 2 integration tests for overview temporal context
- All tests pass ✅

**Test Coverage:**
- Active plan midway through
- Plan just started
- Plan completed
- Plan pending (future start)
- Plans without temporal attrs
- Invalid date formats
- Week boundary calculations
- Overview integration

## Design Philosophy Maintained

✅ **Flexible storage, minimal structure** - No schema changes, uses existing `attrs` JSONB
✅ **Intelligence in query tools, not data** - Temporal context computed on-read, never stored
✅ **Optional fields over required structure** - Plans work with or without temporal attrs
✅ **Computation on-read, not stored** - `current_week`, `progress_pct` calculated from `start_date + today`
✅ **Elegant beats comprehensive** - Simple attrs patterns, no rigid validation

## What Was Rejected (Feature Creep)

❌ **Plan Adherence Tool** - LLM can compare plan-steps to logged workouts manually
❌ **Analytics/Reporting** - Not a storage layer concern
❌ **"Smart" Suggestions** - Premature optimization
❌ **Rigid Validation Schemas** - Contradicts flexible attrs design

## Files Modified

1. **[src/memory/crud.py](src/memory/crud.py)** - Added temporal context computation
2. **[FITNESS_COACH_INSTRUCTIONS.md](FITNESS_COACH_INSTRUCTIONS.md)** - Documented patterns for temporal, progress, contraindications
3. **[src/mcp_server.py](src/mcp_server.py)** - Updated `describe_conventions()` with new patterns
4. **[CLAUDE.md](CLAUDE.md)** - Added core concepts summary
5. **[tests/test_temporal_context.py](tests/test_temporal_context.py)** - New test suite

## Migration Notes

**No database migration required.** All changes use existing `attrs` JSONB field. Plans and goals created before this update work unchanged. To enable new features:

**For Plans:**
```python
# Add temporal attrs to existing plan
upsert_item(
    kind='plan',
    key='existing-plan',
    content='...',
    attrs={
        **existing_attrs,
        'start_date': '2025-09-15',
        'duration_weeks': 8
    }
)
```

**For Goals:**
```python
# Add baseline/target to existing goal
upsert_item(
    kind='goal',
    key='existing-goal',
    content='...',
    attrs={
        **existing_attrs,
        'baseline': {'value': 'starting point', 'date': '2025-09-15'},
        'target': {'value': 'goal', 'date': '2025-12-01'}
    }
)
```

## Key Insight from Feedback

> "The system is 85% there. The missing 15% is **context** - helping me understand what the data means without manual analysis every session."

This implementation adds that context while preserving the system's elegant, flexible design. Recent activity (workouts, metrics, notes) was already in overview - the real gaps were temporal orientation and goal progress visibility, both now solved through attrs conventions + computed fields.
