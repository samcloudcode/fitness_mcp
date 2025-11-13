# Fitness MCP Project

A comprehensive fitness programming system combining three components:
1. **MCP Server** - Data storage and retrieval infrastructure
2. **Skills Folder** - Claude Code coaching workflows
3. **Planning System** - Multi-agent training plan generation

## Features

- 🗄️ **MCP Server**: 4 simple tools (`upsert`, `overview`, `get`, `archive`) for fitness data storage
- 🔍 **Full-Text Search**: PostgreSQL FTS across all entries
- 🎓 **Skills**: Exportable Claude Code skills for real-time coaching
- 🤖 **Planning System**: Multi-agent workflows with validation gates for high-quality plan generation
- 📊 **Framework-Agnostic**: Planning system works with Claude Code, LangChain, CrewAI, AutoGen, etc.
- 🏋️ **Domain Protocols**: Evidence-based exercise selection, progression, recovery, injury prevention

## Project Structure

```
fitness_mcp/
├── src/                        # MCP Server (data infrastructure)
│   ├── mcp_server.py          # 4 tools: upsert, overview, get, archive
│   └── memory/
│       ├── crud.py            # Database operations
│       └── db.py              # PostgreSQL models
├── skills/                     # Skills Folder (Claude Code coaching)
│   └── fitness-coaching/
│       ├── SKILL.md           # Entry point
│       ├── PROGRAM.md         # Program creation workflows
│       ├── WEEK.md            # Week planning workflows
│       ├── WORKOUT.md         # Workout creation workflows
│       └── knowledge/         # Domain-specific expertise
├── planning/                   # Planning System (multi-agent)
│   ├── README.md              # Planning system architecture
│   ├── instructions/          # Agent execution frameworks
│   │   ├── create-program.md # Program creation agent
│   │   ├── plan-week.md      # Week planning agent
│   │   ├── create-workout.md # Workout creation agent
│   │   └── create-protocol.md# Protocol creation agent
│   └── protocols/             # Domain expertise library
│       ├── exercise-selection.md
│       ├── progression.md
│       ├── recovery-management.md
│       ├── injury-prevention.md
│       └── movement-patterns.md
├── tests/                      # Test suite
├── migrations/                 # Database migrations
├── CLAUDE.md                   # Project guidance for Claude Code
└── README.md                   # This file
```

## Three-Component Architecture

### 1. MCP Server (`src/`)
**Purpose**: Data storage and retrieval infrastructure

- 4 FastMCP tools: `upsert`, `overview`, `get`, `archive`
- PostgreSQL database with unified entry-based architecture
- Stores goals, programs, weeks, plans, workouts, logs, metrics, knowledge, preferences
- All components use this for data persistence

**Use when**: Storing/retrieving user fitness data

### 2. Skills Folder (`skills/`)
**Purpose**: Single-LLM coaching workflows for Claude Code

- Markdown instruction files with progressive disclosure
- Real-time coaching conversations
- Exportable to other repositories
- Works within Claude Code environment

**Use when**: Having coaching conversations, need instruction-following approach

### 3. Planning System (`planning/`)
**Purpose**: Multi-agent artifact generation with cross-checking

- Agent instructions with 4-phase execution (assess → plan → validate → execute)
- Domain protocols for evidence-based decision-making
- Framework-agnostic (works with Claude Code, LangChain, CrewAI, AutoGen)
- Validation gates and review workflows

**Use when**: Generating high-quality training plans, need multi-agent review, want framework flexibility

See [planning/README.md](planning/README.md) for detailed planning system documentation.

## Documentation Guide

### Core Documentation
- **[README.md](README.md)** (this file) - Project overview and quick start
- **[CLAUDE.md](CLAUDE.md)** - Complete developer guide, architecture, and Claude Code instructions
- **[FITNESS_COACH_INSTRUCTIONS_SIMPLE.md](FITNESS_COACH_INSTRUCTIONS_SIMPLE.md)** - Comprehensive LLM instructions for using MCP server

### Component Documentation
- **[skills/README.md](skills/README.md)** - Skills folder overview and philosophy
- **[skills/fitness-coaching/SKILL.md](skills/fitness-coaching/SKILL.md)** - Main skill entry point
- **[planning/README.md](planning/README.md)** - Multi-agent planning system architecture

### Additional Resources
- **[skills/SKILL_PHILOSOPHY.md](skills/SKILL_PHILOSOPHY.md)** - Progressive disclosure design principles
- **[skills/KNOWLEDGE-WRITING-GUIDE.md](skills/KNOWLEDGE-WRITING-GUIDE.md)** - Best practices for domain knowledge files
- **[CLAUDE_SKILLS_RESEARCH.md](CLAUDE_SKILLS_RESEARCH.md)** - Research notes on Anthropic skills architecture

## Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL database (Supabase or local)

### Setup

1. **Clone the repository**
```bash
git clone <your-repo>
cd fitness_mcp
```

2. **Install dependencies**
```bash
uv sync
```

3. **Configure database**
Create a `.env` file with your database URL:
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

4. **Run migrations**
Execute the SQL migration in your database:
```bash
psql $DATABASE_URL < migrations/001_create_memories.sql
```

### Usage

**Run tests:**
```bash
uv run python tests/test_memory_server.py
```

**Start the MCP server:**
```bash
uv run python -m src.mcp_server
```

**Or use the script entry point:**
```bash
uv run memory-server
```

## MCP Protocol

All servers implement the [Model Context Protocol](https://github.com/anthropics/model-context-protocol) for seamless integration with AI assistants like Claude.

## Contributing

Each server follows these conventions:
- Python 3.11+ with type hints
- SQLAlchemy for database operations
- FastMCP for MCP protocol implementation
- Environment-based configuration
- Comprehensive test coverage

## License

MIT