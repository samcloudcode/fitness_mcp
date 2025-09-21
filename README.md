# Fitness MCP Project

MCP (Model Context Protocol) server for memory storage with full-text search capabilities using Supabase Postgres.

## Features

- 📝 **Memory Storage**: Store and retrieve memories with user context
- 🔍 **Full-Text Search**: Search across all memories using PostgreSQL's full-text search
- 🏷️ **Topic Categorization**: Organize memories by topics
- 🚀 **Production Ready**: Built with SQLAlchemy and FastMCP

## Project Structure

```
fitness_mcp/
├── src/
│   ├── mcp_server.py      # MCP server entry point
│   └── memory/            # Memory module
│       ├── __init__.py
│       ├── crud.py        # Database operations
│       └── db.py          # Database configuration
├── tests/                 # Test files
│   └── test_memory_server.py
├── migrations/            # Database migrations
│   └── 001_create_memories.sql
├── PRPs/                  # Project Reference Patterns
│   └── memory-server.md   # Memory server spec
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

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