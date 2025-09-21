# Add Branch and Run Scripts

## Setup development scripts and VS Code tasks

Configure branch worktree creation and app runner scripts with VS Code integration.

## Implementation

1. **Create scripts directory**
   - Check/create `scripts/` directory
   - Add executable scripts

2. **Add VS Code tasks**
   - Create `.vscode/tasks.json`
   - Configure task runners

## Files to Create

### scripts/create-branch-worktree.sh
```bash
#!/bin/bash

# Ensure we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Error: Not in a git repository"
  exit 1
fi

# Get the repository root
repo_root=$(git rev-parse --show-toplevel)

# Prompt for branch name
read -p "Enter new branch name: " branch_name

# Validate branch name (basic validation)
if [[ -z "$branch_name" ]]; then
  echo "Error: Branch name cannot be empty"
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$branch_name"; then
  echo "Warning: Branch '$branch_name' already exists"
  read -p "Do you want to use the existing branch? (y/n): " use_existing
  if [[ "$use_existing" != "y" ]]; then
    exit 1
  fi
fi

# Create branch directory
branch_path="$repo_root/tree/$branch_name"

# Handle branch names with slashes (like "feature/foo")
if [[ "$branch_name" == */* ]]; then
  dir_path=$(dirname "$branch_path")
  mkdir -p "$dir_path"
fi

# Make sure parent directory exists
mkdir -p "$(dirname "$branch_path")"

# Check if a worktree already exists
if [ -d "$branch_path" ]; then
  echo "Error: Worktree directory already exists: $branch_path"
  exit 1
fi

# Create branch and worktree
if git show-ref --verify --quiet "refs/heads/$branch_name"; then
  echo "Creating worktree for existing branch '$branch_name'..."
  git worktree add "$branch_path" "$branch_name" || { echo "Error: Failed to create worktree"; exit 1; }
else
  echo "Creating new branch '$branch_name' and worktree..."
  git worktree add -b "$branch_name" "$branch_path" || { echo "Error: Failed to create worktree"; exit 1; }
fi

# Generate random Peacock color for the worktree
peacock_colors=(
  "#832561"  # Angular Red
  "#215732"  # Vue Green
  "#61dafb"  # React Blue
  "#007ACC"  # TypeScript Blue
  "#68217a"  # Visual Studio Purple
  "#DD0531"  # C++ Red
  "#005f87"  # Go Blue
  "#e37933"  # Svelte Orange
  "#42b883"  # Vue Green (alt)
  "#f0db4f"  # JavaScript Yellow
  "#3178c6"  # TypeScript Blue (alt)
  "#cb3837"  # npm Red
  "#ff6b6b"  # Coral
  "#4ecdc4"  # Turquoise
  "#45b7d1"  # Sky Blue
  "#96ceb4"  # Sage Green
  "#feca57"  # Honey
  "#ff9ff3"  # Pink
  "#48dbfb"  # Cyan
  "#0abde3"  # Ocean Blue
)

# Select random color
random_index=$((RANDOM % ${#peacock_colors[@]}))
selected_color="${peacock_colors[$random_index]}"

# Create .vscode directory in the new worktree
mkdir -p "$branch_path/.vscode"

# Create settings.json with Peacock color
cat > "$branch_path/.vscode/settings.json" << EOF
{
  "workbench.colorCustomizations": {
    "activityBar.activeBackground": "$selected_color",
    "activityBar.background": "$selected_color",
    "activityBar.foreground": "#ffffff",
    "activityBar.inactiveForeground": "#ffffff99",
    "activityBarBadge.background": "#ffffff",
    "activityBarBadge.foreground": "#000000",
    "titleBar.activeBackground": "$selected_color",
    "titleBar.activeForeground": "#ffffff",
    "titleBar.inactiveBackground": "${selected_color}99",
    "titleBar.inactiveForeground": "#ffffff99",
    "statusBar.background": "$selected_color",
    "statusBar.foreground": "#ffffff",
    "statusBarItem.hoverBackground": "${selected_color}dd"
  },
  "peacock.color": "$selected_color"
}
EOF

echo "Success! New worktree created at: $branch_path"
echo "Applied Peacock color: $selected_color"
echo "To start working on this branch, run: cd \"$branch_path\""

# Open the new worktree in VS Code (WSL)
if command -v code >/dev/null 2>&1; then
  echo "Opening in VS Code (new window)..."
  code -n "$branch_path" || echo "Warning: 'code' command failed to open VS Code."
else
  echo "Note: VS Code CLI ('code') not found in WSL. Make sure it's installed in PATH via VS Code."
fi
```

### scripts/run-app.sh
```bash
#!/bin/bash

# Use first argument as port, default to 8000
PORT=${1:-8000}

echo "Starting application on port $PORT..."
echo "API Docs: http://localhost:$PORT/docs"
echo "ReDoc: http://localhost:$PORT/redoc"

# Run the FastAPI application with hot reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT
```

### .vscode/tasks.json
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Create Branch Worktree",
      "type": "shell",
      "command": "${workspaceFolder}/scripts/create-branch-worktree.sh",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": true,
        "panel": "shared",
        "showReuseMessage": false,
        "clear": true
      },
      "problemMatcher": [],
      "icon": {
        "id": "git-branch",
        "color": "terminal.ansiGreen"
      }
    },
    {
      "label": "Run Application",
      "type": "shell",
      "command": "${workspaceFolder}/scripts/run-app.sh",
      "args": ["${input:port}"],
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared",
        "showReuseMessage": false
      },
      "problemMatcher": [],
      "icon": {
        "id": "server-process",
        "color": "terminal.ansiBlue"
      }
    }
  ],
  "inputs": [
    {
      "id": "port",
      "type": "promptString",
      "description": "Port number for the application",
      "default": "8000"
    }
  ]
}
```

## Output
Creates:
- `scripts/create-branch-worktree.sh` (executable)
- `scripts/run-app.sh` (executable)
- `.vscode/tasks.json`

## Features
- Git worktree management with random Peacock colors
- Application runner with configurable port
- VS Code task integration with icons
- Auto-opens new worktree in VS Code

## Notes
- Make scripts executable: `chmod +x scripts/*.sh`
- Worktrees created in `tree/` directory
- VS Code tasks accessible via Command Palette (Ctrl+Shift+P)