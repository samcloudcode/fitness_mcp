# Fitness MCP Project

A collection of MCP (Model Context Protocol) servers for fitness and productivity applications.

## Projects

### 📝 [Memory MCP Server](./memory-mcp-server)
A persistent memory storage system with full-text search capabilities using Supabase Postgres.

**Features:**
- Store and retrieve memories with user context
- Full-text search across all memories
- Topic-based categorization
- Production-ready deployment

**Status:** ✅ Complete

## Project Structure

```
fitness_mcp/
├── memory-mcp-server/     # Memory storage MCP server
├── PRPs/                  # Project Reference Patterns
│   └── memory-server.md   # Memory server implementation spec
└── README.md             # This file
```

## Getting Started

Each MCP server is a standalone project. To get started with any server:

1. Navigate to the server directory
2. Follow the README instructions in that directory
3. Each server has its own dependencies and configuration

## Development Setup

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Supabase account (for database-backed servers)

### Common Commands

```bash
# Enter a project
cd memory-mcp-server

# Install dependencies
uv sync

# Run tests
uv run python test_server.py

# Start MCP server
uv run python -m src.mcp_server
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