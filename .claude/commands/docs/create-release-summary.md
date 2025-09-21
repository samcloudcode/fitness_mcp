# Create Release Summary

## Date Range: $ARGUMENTS

Generate a comprehensive release summary analyzing all changes between the specified dates. Focus on user-visible impacts, categorized by type, with context from documentation and commit history.

## Research Process

1. **Git History Analysis**
   - Analyze commits in date range (local and remote)
   - Extract commit messages and PR descriptions
   - Identify merge commits and feature branches
   - Check for version tags within range

2. **Change Categorization**
   - Features (new functionality)
   - Enhancements (improved existing features)
   - Bug Fixes (resolved issues)
   - Performance improvements
   - Breaking changes
   - API/Endpoint changes
   - Documentation updates

3. **Documentation Context**
   - Look for migration guides or upgrade notes
   - Extract relevant issue/PR numbers for tracking

## Git Commands to Execute

```bash
# Get date range from arguments (format: YYYY-MM-DD)
START_DATE="$1"
END_DATE="$2"

# Fetch latest remote changes
git fetch --all --tags

# List all commits in date range (local + remote)
git log --all --since="$START_DATE" --until="$END_DATE" --format="%h|%an|%ad|%s" --date=short

# Show detailed commit messages with bodies
git log --all --since="$START_DATE" --until="$END_DATE" --format="COMMIT:%h%nAUTHOR:%an%nDATE:%ad%nSUBJECT:%s%nBODY:%b%n---"

# List merged PRs (if using GitHub flow)
git log --all --since="$START_DATE" --until="$END_DATE" --grep="Merge pull request" --format="%s"

# Show file changes summary
git diff --stat $(git rev-list --since="$START_DATE" --until="$END_DATE" --max-parents=0 HEAD | tail -1)..HEAD

# List all changed files grouped by type
git diff --name-status $(git rev-list --since="$START_DATE" --until="$END_DATE" --max-parents=0 HEAD | tail -1)..HEAD

# Check for version tags in range
git tag --list --sort=-creatordate --format="%(refname:short)|%(creatordate:short)|%(subject)" | grep -E "$START_DATE|$END_DATE"
```

## Analysis Framework

### User Impact Assessment
- **High Impact**: Breaking changes, new features, major bug fixes
- **Medium Impact**: Enhancements, performance improvements
- **Low Impact**: Minor fixes, documentation, refactoring

### Change Pattern Recognition
- Look for keywords: "feat:", "fix:", "perf:", "docs:", "breaking:", "api:"
- Identify feature flags or configuration changes
- Note dependency updates and their implications
- Track endpoint additions/modifications

## Output Template

```markdown
# Release Summary: [START_DATE] to [END_DATE]

## What's New
- **Feature 1**: Brief description of what users can now do
- **Feature 2**: Brief description of new capability
- **Enhancement**: What got better and why it matters

## Fixed Issues
- Issue description - what was broken is now working
- Another fix - brief impact description

## API Changes
- New endpoint: `GET /api/new-endpoint`
- Modified: `POST /api/endpoint` - now accepts additional parameters
- Deprecated: `OLD /api/endpoint` - use new version instead

## Breaking Changes
- **Action Required**: What needs to be updated
- Migration: Simple steps to adapt

## Statistics
- Commits: X | Contributors: X | Files Changed: X

---
*Full changelog: [link to detailed commits]*
```

## Automation Helpers

### PR/Issue Extraction
```bash
# Extract GitHub issue numbers
git log --all --since="$START_DATE" --until="$END_DATE" --grep="#[0-9]" -E --format="%s %b" | grep -oE "#[0-9]+" | sort -u

# Get PR descriptions (if using gh CLI)
gh pr list --state merged --search "merged:$START_DATE..$END_DATE" --json number,title,body,labels
```

### Change Classification
```python
# Pseudo-code for commit classification
commit_patterns = {
    'feature': r'^(feat|feature|add|new):',
    'fix': r'^(fix|bugfix|patch):',
    'perf': r'^(perf|performance|optimize):',
    'docs': r'^(docs|documentation):',
    'breaking': r'^(breaking|BREAKING CHANGE):',
    'api': r'^(api|endpoint):'
}
```

## Quality Checklist
- [ ] All commits in range analyzed
- [ ] Changes properly categorized
- [ ] User impact clearly described
- [ ] Breaking changes highlighted
- [ ] Migration paths documented
- [ ] Links to PRs/issues included
- [ ] Contributors acknowledged
- [ ] API changes documented
- [ ] Performance impacts quantified where possible

## Validation Commands
```bash
# Verify date range captures intended commits
git rev-list --count --since="$START_DATE" --until="$END_DATE" HEAD

# Check for any reverted commits
git log --since="$START_DATE" --until="$END_DATE" --grep="Revert" --oneline

# Ensure all branches included
git branch -r --merged | xargs -I {} git log {} --since="$START_DATE" --until="$END_DATE" --oneline
```

## Best Practices
1. **Focus on User Value**: Translate technical changes to user benefits
2. **Be Comprehensive**: Include all changes, not just major ones
3. **Provide Context**: Link to documentation and examples
4. **Highlight Actions**: Clearly state any required user actions
5. **Version Appropriately**: Follow semantic versioning implications

## Output
Save as: `releases/release-summary-[START_DATE]-to-[END_DATE].md`

## Success Metrics
Score the release summary (1-10) based on:
- Completeness of change capture
- Clarity of user impact
- Actionability of information
- Quality of categorization
- Usefulness for stakeholders

Remember: The goal is to create a release summary that serves both technical and non-technical stakeholders, clearly communicating what changed and why it matters.