#!/bin/bash

STAGING_DIR="/home/redwannabil/portfolio_staging"
cd "$STAGING_DIR" || { echo "❌ Error: Could not change to $STAGING_DIR"; exit 1; }

git add --all

if ! git diff --cached --quiet; then
    echo "📦 Committing new script..."
    git commit -m "Auto-Staged new raw scripts via publish command"
    git push origin main
    echo "☁️ Push successful. The AI is now processing your file!"
else
    echo "⚠️ Git says there are no new changes to push."
fi
