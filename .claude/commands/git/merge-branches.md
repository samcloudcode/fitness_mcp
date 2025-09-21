# Merge Branches

## Source → Target: $ARGUMENTS

Execute a clean branch merge with validation and conflict resolution. Focus on Python projects using uv.

## Pre-Merge Check

1. **Quick Assessment**
   ```bash
   # Check branch status
   git status

   # View branch divergence
   git log --graph --oneline -10 source-branch target-branch

   # Preview changed files
   git diff --name-only target-branch...source-branch
   ```

2. **Backup Current State**
   ```bash
   # Note current commits
   git rev-parse HEAD > .merge-backup

   # Create safety branch
   git branch backup-$(date +%Y%m%d-%H%M%S)
   ```

## Validation Before Merge

### Test Both Branches
```bash
# Test target branch
git checkout target-branch
uv run pytest tests/ -v
uv run ruff check
uv run mypy .

# Test source branch
git checkout source-branch
uv run pytest tests/ -v
uv run ruff check
uv run mypy .
```

## Execute Merge

### Standard Merge Process
```bash
# Update branches
git checkout target-branch
git pull origin target-branch

git checkout source-branch
git pull origin source-branch

# Perform merge
git checkout target-branch
git merge source-branch -m "Merge source-branch into target-branch"
```

### Handle Conflicts
```bash
# List conflicts
git status --short | grep "^UU"

# Edit conflicts
git diff --name-only --diff-filter=U | xargs $EDITOR

# After resolving
git add .
git commit
```

## Post-Merge Validation

### Run Full Test Suite
```bash
# Python tests
uv run pytest tests/ -v --cov

# Linting and formatting
uv run ruff check --fix
uv run ruff format

# Type checking
uv run mypy .

# Build check (if applicable)
uv build
```

## Cleanup

```bash
# Delete merged branch locally
git branch -d source-branch

# Delete from remote
git push origin --delete source-branch

# Clean up backup (after verification)
git branch -D backup-*
```

## Rollback if Needed

```bash
# Abort ongoing merge
git merge --abort

# Reset to backup
git reset --hard $(cat .merge-backup)

# Or revert completed merge
git revert -m 1 HEAD
```

## Quality Checklist
- [ ] Both branches tested independently
- [ ] Backup created
- [ ] Conflicts resolved properly
- [ ] Tests passing post-merge
- [ ] Code formatted with ruff
- [ ] Type checking passes
- [ ] Branch cleanup completed

Confidence Score: 8/10 (Simplified Python-focused merge workflow)

Remember: Test thoroughly before and after merge.