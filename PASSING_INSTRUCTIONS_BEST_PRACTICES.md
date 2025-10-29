# Best Practices for Passing Fitness Coach Instructions (October 2025)

## Overview

Your `FITNESS_COACH_INSTRUCTIONS_CONSOLIDATED.md` can be passed to AI assistants through several methods, each with different trade-offs:

## 1. MCP Resources (Best for MCP-enabled clients like Claude Desktop)

**Implementation**: Already added to your MCP server at `fitness://coach-instructions`

**How it works**:
- MCP clients discover and can access the resource via URI
- Instructions are preloaded into agent's working memory
- Updates automatically when you modify the file

**Usage in Claude Desktop**:
```json
{
  "mcpServers": {
    "fitness": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.mcp_server"],
      "cwd": "/home/samstitt/Dev/fitness_mcp"
    }
  }
}
```

Claude will automatically have access to the instructions via the resource.

## 2. Project Instructions (CLAUDE.md pattern)

**Best for**: Claude Code, GitHub Copilot, Cursor

**Implementation**:
- Keep as `CLAUDE.md` in project root (you already have this)
- Claude Code automatically reads and follows these instructions
- Works across all Claude interfaces that support project context

## 3. Custom Instructions (ChatGPT)

**Best for**: ChatGPT Plus/Team/Enterprise

**How to set up**:
1. Go to Settings → Personalization → Custom Instructions
2. In "What would you like ChatGPT to know about you?", paste:
   ```
   I use a fitness tracking MCP server with 4 core tools (upsert, overview, get, archive).
   Context: [paste key sections from FITNESS_COACH_INSTRUCTIONS_CONSOLIDATED.md]
   ```
3. In "How would you like ChatGPT to respond?", paste:
   ```
   Follow the two-phase pattern: propose plans first, save only after my approval.
   Use context-aware overview modes (planning, upcoming, knowledge, history).
   Always fetch ALL knowledge entries before programming workouts for safety.
   Keep entries concise with "why" context (100-400 chars typically).
   ```

**Limitations**: 1500 character limit per box, so you'll need to summarize key points.

## 4. System Prompts (API usage)

**Best for**: Using OpenAI/Anthropic APIs programmatically

```python
system_prompt = open('FITNESS_COACH_INSTRUCTIONS_CONSOLIDATED.md').read()

# OpenAI API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Create a workout plan"}
    ]
)

# Anthropic API
response = anthropic.messages.create(
    model="claude-3-opus-20240229",
    system=system_prompt,
    messages=[{"role": "user", "content": "Create a workout plan"}]
)
```

## 5. README Pattern (Universal)

**Best for**: Any AI tool that reads project files

Create a `README_AI_CONTEXT.md` that includes:
- Link to main instructions
- Quick reference for the 4 core tools
- Common workflows
- Safety reminders

## Recommendations by Use Case

### For Claude (Desktop/Web)
1. **Primary**: MCP Resource (already implemented)
2. **Fallback**: CLAUDE.md in project root
3. **Manual**: Paste relevant sections in conversation

### For ChatGPT
1. **Primary**: Custom Instructions (summarized version)
2. **Session-specific**: Paste full instructions at conversation start
3. **API**: Use as system prompt

### For Development (VSCode, Cursor, etc.)
1. **Primary**: CLAUDE.md pattern (widely supported)
2. **Secondary**: .ai/instructions.md (some tools look here)
3. **Inline**: Comments in code referencing the instructions

## Key Points to Always Include (Regardless of Method)

1. **Two-Phase Pattern**: Propose first, save after approval
2. **Context Modes**: planning, upcoming, knowledge, history
3. **Safety First**: Always fetch ALL knowledge before workouts
4. **Conciseness**: 100-400 chars with "why" context
5. **Tool Philosophy**: 4 tools, everything in content field

## Testing Your Setup

### MCP Resource Test
```bash
# Check if resource is available
echo '{"jsonrpc": "2.0", "method": "resources/list", "id": 1}' | uv run python -m src.mcp_server
```

### Quick Validation Prompts
Use these to verify the AI understands your instructions:

1. "What's your approach when I ask for a workout?"
   (Should mention: overview(context='planning'), propose first, save after approval)

2. "How do you handle it when I say 'I just did squats 5x5 at 225'?"
   (Should mention: log immediately with upsert)

3. "What context modes are available?"
   (Should list: planning, upcoming, knowledge, history, default)

## Maintaining Instructions

1. **Single Source of Truth**: Keep `FITNESS_COACH_INSTRUCTIONS_CONSOLIDATED.md` as master
2. **Version Control**: Track changes in git
3. **Update Propagation**: When you update, remember to:
   - Restart MCP server (for resource)
   - Update Custom Instructions (ChatGPT)
   - Commit changes (for CLAUDE.md)

## Common Pitfalls to Avoid

1. **Too Much Detail**: Don't paste entire instruction file in ChatGPT custom instructions (1500 char limit)
2. **Missing Safety**: Always include the "fetch all knowledge before workouts" rule
3. **Forgetting Context**: Include the context modes (planning, upcoming, etc.)
4. **No Examples**: Include 1-2 workflow examples for clarity