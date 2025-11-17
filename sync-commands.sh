#!/bin/bash

# Sync fitness command files from planning/commands to .claude/commands/fitness
# This keeps the canonical source in planning/ while making them available as Claude Code commands

set -e  # Exit on error

SOURCE_DIR="planning/commands"
DEST_DIR=".claude/commands/fitness"

echo "Syncing fitness commands..."
echo "Source: $SOURCE_DIR"
echo "Destination: $DEST_DIR"
echo ""

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Copy all markdown files
for file in "$SOURCE_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Copying $filename..."
        cp "$file" "$DEST_DIR/$filename"
    fi
done

echo ""
echo "✓ Sync complete!"
echo ""
echo "Files in $DEST_DIR:"
ls -1 "$DEST_DIR"
