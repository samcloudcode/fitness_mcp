# Add Beep Settings

## Add notification hooks to .claude/settings.local.json

Configure audio notifications for Claude Code events.

## Implementation

1. **Check existing settings**
   - Read `.claude/settings.local.json` if it exists
   - Preserve existing configuration (permissions, etc.)

2. **Add beep configuration**
   - Add notification hooks for audio feedback
   - Merge with existing hooks if present

## Configuration to Add

```json
{
  ...
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command '[console]::beep(700,150); Start-Sleep -Milliseconds 80; [console]::beep(900,150)'"
          }
        ]
      }
    ]
  }
}
```

## Output
Updates: `.claude/settings.local.json`

## Notes
- Creates .claude directory if needed
- Merges with existing settings preserving all configuration
- Uses `.claude/settings.local.json` (NOT `.claude/settings`)
- WSL-compatible PowerShell beep command