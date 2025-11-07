# SKILL Documentation Philosophy

**Purpose:** Design principles and rationale for the fitness-coaching skill file structure.

---

## Core Principle: Progressive Disclosure

Following Anthropic's best practices, the fitness-coaching skill uses **progressive disclosure** to optimize context window usage:
- Load minimal information upfront
- Provide navigation to detailed content
- Let the LLM pull what it needs when it needs it

---

## File Separation of Concerns

**Critical Distinction:** SKILL.md contains everything needed to **use the tools and save data**. Only load sub-files when **creating programs/weeks/workouts** (PROGRAM.md, WEEK.md, WORKOUT.md) or making **coaching decisions** (COACHING.md).

### SKILL.md - Main Entry Point & Data Reference
- **Role:** Tool usage, data structure, and critical behavioral rules
- **Contains:**
  - MCP tool documentation (upsert, get, overview, archive)
  - Data entry guidelines (what makes a good log, goal, knowledge entry)
  - Naming conventions and content structure
  - When to save vs propose (critical behavioral rules)
  - How to save user information (incremental updates, contradicting info)
- **Purpose:** Complete reference for working with the database - no sub-files needed for data entry
- **Length:** Detailed but focused (~430 lines) - appropriate for its role as THE reference
- **What STAYS in SKILL.md:**
  - Knowledge Storage section (teaches data quality, not programming workflow)
  - Incremental Updates (demonstrates tool usage for saving)
  - Content Structure Reference (data guidelines)
  - Tool examples showing upsert mechanics

### PROGRAM.md - Overall Program Creation
- **Role:** Creating and updating the overall training program strategy
- **Contains:** Program creation workflow, integrating multiple goals, concurrent training management, program templates
- **When to load:** When creating or updating `current-program` entry
- **Purpose:** Ensures comprehensive program strategy that links all goals together
- **What belongs here:** How multiple goals fit together, training frequencies, modality interactions

### WEEK.md - Weekly Schedule Planning
- **Role:** Creating weekly training schedules
- **Contains:** Week planning workflow, balancing training across 7 days, adjusting for constraints, week templates
- **When to load:** When creating or updating weekly schedule (`2025-week-NN` entry)
- **Purpose:** Translates program strategy into weekly structure with real-world adjustments
- **What belongs here:** Daily schedule creation, managing constraints (travel, fatigue), week-to-week planning

### WORKOUT.md - Individual Workout Creation
- **Role:** Creating specific workout plans
- **Contains:** 7-step workout design workflow, plan templates, data fetching rules, logging workflows
- **When to load:** REQUIRED before creating any individual workout plan
- **Purpose:** Ensures thorough, safe workout programming with proper context
- **What belongs here:** How to design a single workout, exercise selection, plan creation, logging completed workouts

### COACHING.md - Philosophy & Decision-Making
- **Role:** Coaching principles, decision frameworks, and communication style
- **Contains:** Goal-driven programming, energy management, when to explain "why", tone and approach
- **When to load:** When making coaching decisions or explaining rationale
- **Purpose:** Guides qualitative coaching decisions and client interactions
- **What belongs here:** How to prioritize goals, communication style with clients, when to explain reasoning

### knowledge/*.md - Domain Expertise
- **Role:** Specific topic deep-dives
- **Contains:** Knee health, exercise selection, periodization, etc.
- **When to load:** On-demand for specific questions or concerns
- **Purpose:** Provides specialized expertise without cluttering main files

---

## Information Architecture

```
User Request
    ↓
SKILL.md (Always loaded - establishes context)
    ├─ Identifies task type
    ├─ Shows critical rules (save vs propose)
    └─ Navigates to detail files

Task-Based Loading:
    ├─ Creating program? → Load PROGRAM.md
    ├─ Planning week? → Load WEEK.md
    ├─ Designing workout? → Load WORKOUT.md (REQUIRED for workouts)
    ├─ Coaching decision? → Load COACHING.md
    ├─ Domain question? → Load knowledge/*.md
    └─ Simple data entry? → Use SKILL.md tools only
```

---

## Key Design Decisions

### 1. SKILL.md as Tool & Data Reference
- Keeps ALL tool documentation, naming conventions, content guidelines
- Includes data entry guidelines (what makes good entries, how to update incrementally, handling contradictions)
- Does NOT contain program/week/workout creation workflows (deferred to PROGRAM/WEEK/WORKOUT.md)
- Does NOT contain coaching philosophy/tone (deferred to COACHING.md)
- **Rationale:** LLM needs immediate access to "how to save data" but can load "how to create programs/weeks/workouts" on-demand
- **Key point:** Knowledge Storage section teaches data quality (stays in SKILL.md), not programming workflow

### 2. Early File Navigation (Lines 67-85)
- Task-based loading guide immediately after Critical Rules
- Clear triggers for which file to load (program → PROGRAM.md, week → WEEK.md, workout → WORKOUT.md)
- **Rationale:** LLM sees navigation context BEFORE attempting tasks, preventing them from trying to create workouts without loading WORKOUT.md

### 3. Clear Intro Section (Lines 8-21)
- Establishes what the skill does
- Lists what THIS file contains
- Points to other files for complex tasks
- **Rationale:** Sets expectations upfront - "You're in the data reference; load other files for workflows"

### 4. Critical Rules Remain Prominent (Lines 52-61)
- Behavioral rules stay in SKILL.md (not deferred)
- "When to save vs propose" is fundamental to ALL interactions
- **Rationale:** These rules prevent errors regardless of task type

---

## User Experience Flow

### LLM Reading SKILL.md:
1. Sees intro → "This skill manages fitness data via 4 tools"
2. Sees "For creating programs/workouts: Load PROGRAM.md, WEEK.md, WORKOUT.md"
3. Reads Critical Rules → Understands save vs propose pattern
4. Sees task-based navigation → Clear triggers for which file to load
5. Continues reading → Gets complete tool/data reference
6. When needed → Loads specific file for the task (PROGRAM/WEEK/WORKOUT/COACHING/knowledge)

### Example Workflow:
```
User: "Create me a workout for today"

LLM reads SKILL.md intro → Sees "Creating individual workout: Load WORKOUT.md"
    ↓
Loads WORKOUT.md → Gets 7-step workout design workflow
    ↓
Step 1: Call overview(context='planning') → Gets goals, program, knowledge
    ↓
Follows remaining steps → Proposes workout (doesn't save yet per Critical Rules)
    ↓
User approves → Saves using upsert tool (documented in SKILL.md)
```

---

## Why This Structure Works

### Optimizes Context Window:
- SKILL.md loaded once, provides comprehensive data/tool reference
- Detail files loaded only when task requires them
- Prevents loading workflow documentation for simple data entry

### Task-Oriented:
- LLM can quickly identify "I need X → Load Y"
- Clear triggers for when to load each file
- Reduces decision-making overhead

### Separation of Concerns:
- Data operations (SKILL.md) separated from creation workflows (PROGRAM/WEEK/WORKOUT.md)
- Program strategy (PROGRAM.md) separated from weekly planning (WEEK.md) separated from workout design (WORKOUT.md)
- Workflows separated from philosophy (COACHING.md)
- General expertise separated from domain specifics (knowledge/*.md)

### Prevents Errors:
- "REQUIRED: Load WORKOUT.md first" prevents incomplete workout planning
- Granular file loading reduces cognitive load (only load what you need)
- Critical Rules prevent saving before approval
- Data safety emphasized (always fetch ALL knowledge before programming)

---

## Alignment with Anthropic Best Practices

✅ **Progressive Disclosure** - Table of contents pattern, load detail on-demand
✅ **Conciseness** - SKILL.md under 500 lines, focused scope
✅ **One-Level-Deep References** - All files referenced directly from SKILL.md
✅ **Clear Description** - Frontmatter explains when to use the skill
✅ **Context Window as Public Good** - Only load what's needed for current task
✅ **Task-Oriented Navigation** - Explicit triggers for loading each file

---

## Design Principles Summary

1. **Progressive disclosure over front-loading** - Don't dump everything in SKILL.md
2. **Task-based navigation over alphabetical** - Help LLM find what it needs for current task
3. **Early navigation over buried references** - Show file structure before tool details
4. **Data reference in SKILL.md, workflows in detail files** - Separate "what to do" from "how to use tools"
5. **Critical rules stay central** - Behavioral patterns that apply to all tasks live in SKILL.md
6. **Context window efficiency** - Load only what you need: PROGRAM.md for programs, WEEK.md for weeks, WORKOUT.md for workouts - not for simple logging

---

*This philosophy guides all documentation decisions for the fitness-coaching skill and should be consulted when making structural changes.*
