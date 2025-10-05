# Issue Tracking

The fitness MCP server now includes developer-only issue tracking functionality for backend bugs, features, and enhancements.

## Quick Start

### Report an Issue

```python
# Report a bug
report_issue(
    title="Overview times out with large datasets",
    description="get_overview() times out when user has >500 workouts",
    issue_type="bug",
    severity="high",
    context="Error: psycopg.OperationalError: timeout expired",
    tags="performance database"
)

# Request a feature
report_issue(
    title="Add weekly summary tool",
    description="Tool to generate weekly workout summary with volume/intensity stats",
    issue_type="feature",
    severity="low",
    tags="analytics reporting"
)

# Report an enhancement
report_issue(
    title="Improve search ranking algorithm",
    description="Current FTS doesn't weight recent entries appropriately",
    issue_type="enhancement",
    severity="medium"
)
```

### List Issues

```python
# Get all open issues
list_issues(status='open')

# Get only bugs
list_issues(status='open', issue_type='bug')

# Get critical issues
list_issues(severity='critical')

# Get all issues (including resolved)
list_issues(status=None, limit=200)
```

### Update or Resolve Issues

```python
# Update an issue status
upsert_item(
    kind='issue',
    key='overview-times-out-with-large-datasets',
    content='Updated description with more details...',
    status='in-progress',
    priority=1
)

# Resolve an issue
upsert_item(
    kind='issue',
    key='add-weekly-summary-tool',
    content='Implemented in PR #123',
    status='resolved'
)

# Mark as won't fix
upsert_item(
    kind='issue',
    key='some-old-request',
    content='Not implementing due to...',
    status='wontfix'
)
```

## Key Features

### Separated from Fitness Data
- ✅ Issues are **excluded from `get_overview()`** - won't clutter fitness tracking
- ✅ Issues don't appear in general searches unless explicitly filtered
- ✅ Dedicated tools (`report_issue`, `list_issues`) for issue management
- ✅ Same flexible storage (uses existing `entries` table, no schema changes)

### Flexible Metadata

Issues support structured metadata via `attrs`:

```python
{
    'issue_type': 'bug' | 'feature' | 'enhancement',
    'severity': 'critical' | 'high' | 'medium' | 'low',
    'title': 'Human-readable title'
}
```

### Status Tracking

Use standard status values:
- `open` - New issue (default)
- `in-progress` - Currently being worked on
- `resolved` - Fixed/implemented
- `wontfix` - Decided not to fix

### Priority Mapping

Severity automatically maps to priority:
- `critical` → priority 1
- `high` → priority 2
- `medium` → priority 3
- `low` → priority 4

## Implementation Details

### Database Storage

Issues are stored in the `entries` table with `kind='issue'`:

```sql
SELECT * FROM entries WHERE kind = 'issue' AND status = 'open';
```

### Key Generation

Issue keys are auto-generated from titles:
- Lowercase
- Spaces replaced with hyphens
- Non-alphanumeric removed
- Max 64 characters

Example: `"Overview Times Out"` → `"overview-times-out"`

### Full-Text Search

Issues are searchable like any other entry:

```python
# Search all issues
search_entries(query='timeout performance', kind='issue')
```

## Conventions

As documented in `describe_conventions()`:

```python
{
    'kinds': ['goal', 'plan', ...],  # User-facing kinds
    'developer_kinds': ['issue'],    # Developer-only kinds
    'attrs_hints': {
        'issue': {
            'issue_type': 'bug|feature|enhancement',
            'severity': 'critical|high|medium|low',
            'title': 'string'
        }
    },
    'notes': {
        'issue_kind': 'Developer-only kind for tracking backend issues.
                       Excluded from get_overview() and general fitness workflows.
                       Use report_issue() and list_issues() tools.'
    }
}
```

## Example Workflow

```python
# 1. Report bug during testing
bug = report_issue(
    title="FTS query slow on large datasets",
    description="Full-text search takes >5s with 1000+ entries",
    issue_type="bug",
    severity="high",
    context="Tested with 2000 workouts, query: 'running progression'",
    tags="performance fts search"
)

# 2. Track progress
upsert_item(
    kind='issue',
    key=bug['key'],
    status='in-progress',
    content=bug['content'] + "\n\nStarted investigation, likely missing index."
)

# 3. Resolve with details
upsert_item(
    kind='issue',
    key=bug['key'],
    status='resolved',
    content=bug['content'] + "\n\nFixed: Added composite GIN index on (user_id, fts)"
)

# 4. Review all open issues
open_issues = list_issues(status='open')
for issue in open_issues:
    print(f"{issue['attrs']['severity']}: {issue['attrs']['title']}")
```
