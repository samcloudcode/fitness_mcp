# Project Structure & Organization

## Directory Layout

```
memory-mcp-server/              # Root of the MCP server project
├── src/                       # Python source code
│   ├── __init__.py
│   ├── db.py                  # SQLAlchemy models & database connection
│   ├── crud.py                # Database CRUD operations
│   └── mcp_server.py          # FastMCP server implementation
│
├── migrations/                # Database migrations (manual)
│   └── 001_create_memories.sql
│
├── supabase/                  # Supabase CLI configuration
│   ├── config.toml           # Supabase project config
│   └── migrations/           # Supabase-managed migrations
│       └── 20240101000000_create_memories.sql
│
├── .env                      # Environment variables (git-ignored)
├── .env.example              # Example environment template
├── .gitignore                # Git ignore rules
├── pyproject.toml            # Python project & dependencies
├── Dockerfile                # Container for deployment
├── README.md                 # User documentation
├── test_server.py            # Integration tests
└── test_integration.py       # MCP client tests
```

## Key Decisions

### 1. Environment Variables (.env)
- **Location**: Keep at app level (memory-mcp-server/)
- **Why**: Project-specific credentials should stay with the project
- **Security**: Already in .gitignore, use .env.example as template

### 2. Supabase Configuration
- **Location**: Keep at app level (memory-mcp-server/supabase/)
- **Why**: Database configuration is specific to this MCP server
- **Management**: Use `supabase` CLI from within the project directory

### 3. Dependencies
- **Tool**: Using `uv` package manager
- **Install**: `uv sync` to install from pyproject.toml
- **Add new**: `uv add package-name`

### 4. Database Connection
- **Auto-load**: The server automatically loads .env via python-dotenv
- **Format**: Using pooled connections for better performance
- **URL Encoding**: Password special characters must be URL-encoded

## Running the Server

```bash
# From memory-mcp-server/ directory:

# Install dependencies
uv sync

# Set up environment
cp .env.example .env
# Edit .env with your Supabase credentials

# Run the server
uv run python -m src.mcp_server

# Or run tests
uv run python test_server.py
```

## Deployment

### Local Development
- Use .env file for credentials
- Run with `uv run` for dependency management

### Production
- Set DATABASE_URL environment variable
- Uses Dockerfile for containerization

## Best Practices

1. **Never commit .env** - It's in .gitignore for security
2. **Use pooled connections** - Better for serverless/container environments
3. **URL-encode passwords** - Required for special characters
4. **Keep migrations versioned** - Both in migrations/ and supabase/migrations/
5. **Test locally first** - Use test_server.py before deployment