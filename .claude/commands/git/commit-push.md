# Commit and Push

## Target: $ARGUMENTS (optional branch/message)

Commit current changes and push to remote repository with comprehensive validation. Ensure all changes are properly staged, commit message follows conventions, and push succeeds.

## Pre-Commit Process

1. **Status Check**
   - Review all modified/untracked files
   - Identify what should be committed
   - Check for sensitive data (keys, tokens, passwords)
   - Verify no debug/test code remains

2. **Staging Strategy**
   - Add relevant files to staging area
   - Exclude temporary/build files
   - Review staged changes with `git diff --staged`
   - Ensure .gitignore is properly configured

3. **Branch Verification**
   - Confirm correct branch for changes
   - Check if branch is up-to-date with remote
   - Resolve any conflicts if needed

## Commit Generation

### Commit Message Structure
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

### Message Guidelines
- Subject: 50 chars max, imperative mood
- Body: Explain what and why, not how
- Reference issues/PRs if applicable
- Include breaking changes in footer

### Research for Context
- Review recent commit history for style
- Check CONTRIBUTING.md for conventions
- Look at similar commits in project

## Validation Steps

### Pre-Push Checks (Python Focus)
```bash
# Verify tests pass
uv run pytest tests/ -v

# Check linting/formatting
uv run ruff check --fix
uv run ruff format

# Type checking
uv run mypy .

# Ensure build succeeds (if applicable)
uv build

# Final diff review
git diff HEAD~1
```

### Push Process
```bash
# Push with upstream tracking
git push -u origin $(git branch --show-current)

# If rejected, pull and resolve
git pull --rebase origin $(git branch --show-current)
git push
```

## Error Recovery

### Common Issues
- **Push rejected**: Pull latest, resolve conflicts, retry
- **Pre-commit hooks fail**: Fix issues, amend commit
- **Large files**: Use Git LFS or exclude
- **Wrong branch**: Cherry-pick to correct branch

### Rollback Options
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Amend commit message
git commit --amend

# Force push (use cautiously)
git push --force-with-lease
```

## Post-Push Actions

- [ ] Verify push on remote (GitHub/GitLab)
- [ ] Check CI/CD pipeline status
- [ ] Create PR if feature branch
- [ ] Update related issues/tickets
- [ ] Notify team if breaking changes

## Quality Checklist
- [ ] No sensitive data committed
- [ ] Tests passing
- [ ] Code formatted/linted
- [ ] Commit message clear and descriptive
- [ ] Pushed to correct branch
- [ ] Remote updated successfully

Confidence Score: 9/10 (Standard git workflow with comprehensive validation)

Remember: Never force push to main/master. Always verify changes before pushing.