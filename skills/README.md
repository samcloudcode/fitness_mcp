# Fitness Coaching Skill

Evidence-based fitness coaching with tools for tracking workouts, goals, programs, and progress.

## Structure

```
fitness-coaching/
├── SKILL.md                          # Entry point - tools, storage, big picture
├── PROGRAMMING.md                    # Detailed programming workflows
├── COACHING.md                       # Coaching philosophy
└── knowledge/                        # Domain-specific reference knowledge
    └── KNEE-HEALTH.md               # Mechanisms & principles for knee health programming
```

## Progressive Disclosure Pattern

**SKILL.md** (always loaded):
- System overview and big picture
- All 4 tools (overview, get, upsert, archive)
- Data storage guidelines
- Naming conventions
- Quick reference
- Navigation to detail files

**PROGRAMMING.md** (load when designing workouts):
- Complete planning hierarchy with examples
- Content templates
- Workout design workflows
- Data fetching safety rules

**COACHING.md** (load when making coaching decisions):
- Goal-driven programming
- Efficiency and specificity balance
- Energy management principles

**knowledge/*.md** (load specific topics as needed):
- Load when relevant to current programming task
- Example: KNEE-HEALTH.md when user has knee issues

## Usage

Claude will automatically load this skill when:
- Designing workouts or training programs
- Creating or updating fitness goals
- Logging completed workouts
- Answering fitness questions
- Managing training progress

## Database vs Skills

**Database stores (user-specific)**:
- Goals, programs, weekly plans
- Workout logs and metrics
- Personal limitations and injuries
- Equipment access and preferences

**Skills provide (general expertise)**:
- Programming workflows and templates
- Coaching philosophy and principles
- Domain knowledge (exercise selection, periodization, etc.)

## Installation

Already installed in project at `.claude/skills/fitness-coaching/`

No additional setup required - Claude Code will discover and load automatically.
