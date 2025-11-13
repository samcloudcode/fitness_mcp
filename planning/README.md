# Multi-Agent Planning System

This directory contains a multi-agent planning system for fitness programming, designed for cross-checking and review workflows across different LLM frameworks.

## Architecture Overview

The fitness_mcp repository has **three complementary components**:

### 1. MCP Server (`src/`)
**Purpose**: Data storage and retrieval infrastructure
**Technology**: Python, FastMCP, PostgreSQL, SQLAlchemy
**Interface**: 4 tools - `upsert`, `overview`, `get`, `archive`
**Use case**: Persistent storage for all fitness data (goals, programs, workouts, logs, metrics)

### 2. Skills (`skills/`)
**Purpose**: Single-LLM coaching workflows
**Technology**: Markdown instruction files for Claude Code
**Pattern**: Progressive disclosure (load what you need, when you need it)
**Use case**: Real-time coaching conversations with users

### 3. Planning System (`planning/`)
**Purpose**: Multi-agent artifact generation with cross-checking
**Technology**: Framework-agnostic agent instructions + domain protocols
**Pattern**: Agent collaboration with validation gates
**Use case**: High-quality training plan creation through multi-agent review

## Planning System vs Skills

| Aspect | Skills (skills/) | Planning System (planning/) |
|--------|------------------|------------------------------|
| **Design** | Single LLM following instructions | Multi-agent with cross-checking |
| **Quality** | Instruction-following | Validation gates + review |
| **Framework** | Claude Code specific | Framework-agnostic |
| **Output** | Conversational coaching | Structured artifacts |
| **Purpose** | Guide user interactions | Generate reviewed plans |

## Directory Structure

```
planning/
├── README.md                      # This file - system overview
├── instructions/                  # Agent execution frameworks
│   ├── create-program.md         # Program creation agent
│   ├── plan-week.md              # Week planning agent
│   ├── create-workout.md         # Workout creation agent
│   └── create-protocol.md        # Protocol creation agent
└── protocols/                     # Domain expertise library
    ├── exercise-selection.md     # Exercise selection criteria
    ├── progression.md            # Load/volume progression
    ├── recovery-management.md    # Recovery strategies
    ├── injury-prevention.md      # Safety and limitations
    └── movement-patterns.md      # Movement quality standards
```

## Agent Collaboration Pattern

Each agent follows a 4-phase execution framework:

### 1. Assessment Phase
- Gather context via MCP `overview()` and `get()` tools
- Load relevant protocols from `protocols/`
- Identify constraints and requirements

### 2. Planning Phase
- Draft plan based on protocols
- Cross-check against multiple protocol files
- Identify validation points

### 3. Validation Phase
- Run validation checks (protocol compliance)
- Review against quality standards
- Flag issues for revision

### 4. Execution Phase
- Save approved plan via MCP `upsert()` tool
- Log execution details
- Return artifact to user

## Using with Different LLM Frameworks

### Claude Code
```bash
# Load agent instruction
cat planning/instructions/create-program.md

# Load relevant protocols
cat planning/protocols/exercise-selection.md
cat planning/protocols/progression.md

# Execute with MCP tools available
```

### LangChain
```python
from langchain.agents import AgentExecutor
from langchain.tools import Tool

# Load instruction as system prompt
with open('planning/instructions/create-program.md') as f:
    instruction = f.read()

# Load protocols as context
protocols = []
for protocol_file in ['exercise-selection.md', 'progression.md']:
    with open(f'planning/protocols/{protocol_file}') as f:
        protocols.append(f.read())

# Create agent with MCP tools
agent = create_agent(instruction, protocols, mcp_tools)
```

### CrewAI
```python
from crewai import Agent, Task, Crew

# Create specialized agents
program_agent = Agent(
    role='Program Designer',
    goal='Create evidence-based training programs',
    backstory=open('planning/instructions/create-program.md').read(),
    tools=mcp_tools
)

review_agent = Agent(
    role='Program Reviewer',
    goal='Validate program safety and effectiveness',
    backstory=open('planning/protocols/injury-prevention.md').read(),
    tools=mcp_tools
)

# Create workflow with cross-checking
crew = Crew(agents=[program_agent, review_agent], tasks=[...])
```

### AutoGen
```python
from autogen import AssistantAgent, UserProxyAgent

# Create agents with protocols
program_agent = AssistantAgent(
    name="ProgramDesigner",
    system_message=open('planning/instructions/create-program.md').read(),
    llm_config=llm_config
)

# Load protocols for validation
protocols = {
    'exercise_selection': open('planning/protocols/exercise-selection.md').read(),
    'injury_prevention': open('planning/protocols/injury-prevention.md').read()
}
```

## MCP Tool Integration

All agents interact with the MCP server using 4 tools:

```python
# 1. Gather context
context = overview(context='planning')  # Get goals, program, week, recent logs

# 2. Get specific details
details = get(items=[{'kind': 'knowledge', 'key': 'knee-health'}])

# 3. Save artifacts
upsert(
    kind='program',
    key='current-program',
    content='Oct-Dec: Strength primary...'
)

# 4. Archive old items
archive(kind='program', key='old-program')
```

## Protocol Library Usage

Protocols are domain expertise files that agents reference during decision-making:

### exercise-selection.md
**When to use**: Choosing exercises for a program or workout
**Cross-checks**: Movement patterns, injury prevention

### progression.md
**When to use**: Determining load, volume, intensity progression
**Cross-checks**: Recovery management, injury prevention

### recovery-management.md
**When to use**: Planning rest days, deload weeks, volume management
**Cross-checks**: Progression, injury prevention

### injury-prevention.md
**When to use**: ALWAYS - safety is paramount
**Cross-checks**: Exercise selection, movement patterns, progression

### movement-patterns.md
**When to use**: Ensuring exercise variety and movement balance
**Cross-checks**: Exercise selection, injury prevention

## Quality Standards

All agents must:

1. **Always load injury-prevention protocol** before programming
2. **Cross-check at least 2 protocols** for each decision
3. **Validate against user's knowledge entries** (limitations, injuries)
4. **Include "why" context** in all saved artifacts
5. **Use validation gates** between phases
6. **Log all MCP tool calls** for debugging

## Anti-Patterns to Avoid

1. ❌ Creating artifacts without loading protocols
2. ❌ Skipping validation phase
3. ❌ Not checking user's injury history (knowledge entries)
4. ❌ Single-protocol decision making (no cross-checking)
5. ❌ Saving without user approval (unless user provided completed data)
6. ❌ Duplicating content from protocols into artifacts
7. ❌ Framework-specific code in instruction files

## Example Workflow

```bash
# User requests: "Create a 12-week strength program for rugby"

# 1. Program Creation Agent loads:
- instructions/create-program.md (execution framework)
- protocols/exercise-selection.md (choose exercises)
- protocols/progression.md (plan progression)
- protocols/injury-prevention.md (safety checks)
- protocols/movement-patterns.md (balance movements)

# 2. Agent Assessment Phase:
- overview(context='planning') → Get goals, current program, recent logs
- get(kind='knowledge') → Get all injury/limitation entries
- get(kind='preference') → Get equipment, schedule preferences

# 3. Agent Planning Phase:
- Draft program structure
- Cross-check exercise selection against movement patterns
- Cross-check progression against recovery management
- Validate against injury prevention protocol

# 4. Agent Validation Phase:
- Verify all user limitations addressed
- Check protocol compliance (2+ protocols per decision)
- Ensure "why" context included

# 5. Agent Execution Phase:
- Present to user for approval
- Save via: upsert(kind='program', key='current-program', content='...')
- Log execution details

# 6. Optional Review Agent:
- Load program from MCP
- Re-validate against protocols
- Flag any issues
```

## Getting Started

1. **Choose an agent** from `instructions/` based on your task
2. **Load relevant protocols** referenced in the agent instructions
3. **Connect to MCP server** for data access (`upsert`, `overview`, `get`, `archive`)
4. **Execute agent workflow** following the 4-phase framework
5. **Review output** against quality standards

## Contributing

When adding new agents or protocols:

1. **Agents** (`instructions/`) must include:
   - Clear purpose and when to use
   - List of protocols to load
   - 4-phase execution framework
   - Quality standards
   - Anti-patterns

2. **Protocols** (`protocols/`) must include:
   - Decision framework
   - Validation criteria
   - Cross-check points (which other protocols to reference)
   - Concrete examples

3. **Keep it framework-agnostic** - no framework-specific code in markdown files
