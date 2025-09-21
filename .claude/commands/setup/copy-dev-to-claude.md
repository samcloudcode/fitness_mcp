# Copy Dev Prompts to Claude

## Copy agents, commands, and PRP templates from remote repository

Downloads and installs dev_prompts resources (agents, commands, PRPs) from the GitHub repository into the current project's `.claude` directory.

## Implementation

1. **Check .claude directory exists**
   - Verify `.claude` exists in current project
   - Error if missing

2. **Download from remote repository**
   - Clone or download specific directories from GitHub
   - Use sparse checkout or direct download to get only needed files

3. **Copy resources**
   - agents/ directory
   - commands/ directory
   - PRPs/ directory

## Script to Execute

```bash
# Save original directory
ORIGINAL_DIR=$(pwd)

# Check if .claude directory exists
if [ ! -d ".claude" ]; then
    echo "Error: .claude directory does not exist in current project"
    echo "Please create it first: mkdir .claude"
    exit 1
fi

# Temporary directory for cloning
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Clone only the needed directories using sparse checkout
git clone --filter=blob:none --sparse https://github.com/pamam-apps/dev_prompts.git
cd dev_prompts
git sparse-checkout set agents commands PRPs

# Copy to appropriate directories
cp -r agents "$ORIGINAL_DIR/.claude/"
cp -r commands "$ORIGINAL_DIR/.claude/"
cp -r PRPs "$ORIGINAL_DIR/"

# Cleanup
cd "$ORIGINAL_DIR"
rm -rf "$TEMP_DIR"

echo "✓ Copied agents and commands to .claude/, PRPs to project root"
echo "Contents of .claude/:"
ls -la .claude/
echo "PRPs directory:"
ls -la PRPs/
```

## Output
Creates/Updates:
- `.claude/agents/`
- `.claude/commands/`
- `PRPs/` (in project root)

## Notes
- Downloads from remote GitHub repository
- No local dev_prompts copy required
- Uses sparse checkout for efficiency
- Automatically cleans up temporary files