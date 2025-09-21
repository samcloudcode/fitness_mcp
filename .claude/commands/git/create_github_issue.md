# Create GitHub Issue

## Issue Description: $ARGUMENTS

Create a well-structured GitHub issue with appropriate context from the codebase. Keep analysis lightweight and focused on providing useful context rather than solutions.

## Quick Context Gathering

1. **Codebase Scan** (Keep it light)
   - Identify relevant files/modules mentioned
   - Note existing related issues if applicable
   - Check for similar closed issues
   - Review CLAUDE.md for project context

2. **Issue Classification**
   - Bug report
   - Feature request
   - Documentation update
   - Performance improvement
   - Security concern

## Issue Creation

### Issue Template Structure
```markdown
## Description
[Clear, concise problem statement or feature request]

## Context
[Relevant codebase information gathered]

## Current Behavior (if bug)
[What happens now]

## Expected Behavior
[What should happen]

## Environment (if relevant)
- OS: [e.g., Ubuntu 22.04]
- Version: [e.g., v1.2.3]
- Python: [version]
- uv: [version]

## Possible Areas to Investigate
[Brief suggestions without deep analysis]

## Related Information
- Related issues: #123, #456
- Related PRs: #789
- Documentation: [links]
```

### Title Guidelines
- Be specific and searchable
- Include component/module if applicable
- Format: `[Component] Brief description`
- Examples:
  - `[Auth] Login fails with special characters in password`
  - `[API] Add pagination to user endpoint`
  - `[Docs] Update installation instructions for Windows`

## Lightweight Research

### Quick Checks (30 seconds max each)
```bash
# Search for similar issues
gh issue list --search "keyword"

# Check recent related commits
git log --oneline --grep="keyword" -10

# Quick file relevance scan for Python
grep -l "keyword" **/*.py | head -5

# Check for related tests
find tests/ -name "*.py" -exec grep -l "keyword" {} \; | head -5
```

### Suggestions Format
Instead of solutions, provide:
- "Consider checking [file] for [reason]"
- "May be related to [component]"
- "Similar pattern in [location]"
- "Documentation at [URL] might be relevant"

## Issue Submission

### Using GitHub CLI
```bash
# Create issue with title and body
gh issue create --title "$TITLE" --body "$BODY"

# With labels
gh issue create --title "$TITLE" --body "$BODY" --label "bug,priority-high"

# Assign to milestone
gh issue create --title "$TITLE" --body "$BODY" --milestone "v2.0"

# Interactive mode for selection
gh issue create
```

### Labels to Consider
- **Type**: bug, enhancement, documentation, question
- **Priority**: critical, high, medium, low
- **Status**: needs-triage, ready, in-progress
- **Component**: frontend, backend, api, database

## Quality Checklist
- [ ] Title is clear and searchable
- [ ] Description explains the issue/request
- [ ] Context provided (but not over-researched)
- [ ] Reproduction steps included (for bugs)
- [ ] No sensitive information exposed
- [ ] Appropriate labels added
- [ ] Related issues/PRs linked

## Output
- Issue URL: `https://github.com/[owner]/[repo]/issues/[number]`
- Issue Number: #[number] for reference

## Keep It Light
- Research time: < 2 minutes total
- Focus on context, not solutions
- Suggest areas, don't implement fixes
- Link to docs, don't copy them

Confidence Score: 8/10 (Straightforward issue creation with balanced context)

Remember: The goal is to create a useful issue quickly, not to solve it.