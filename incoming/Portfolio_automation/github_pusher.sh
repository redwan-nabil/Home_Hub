#!/bin/bash

# Define the absolute path to the staging directory
STAGING_DIR="/home/redwannabil/portfolio_staging"

# Move into the directory
cd "$STAGING_DIR" || { echo "❌ Error: Could not change to $STAGING_DIR"; exit 1; }

# Force add all files, even if they are in new subdirectories
git add --all

# Check if there are actually changes to commit
if ! git diff --cached --quiet; then
    echo "📦 Changes detected. Committing and pushing..."
    git commit -m "Auto-Staged new raw scripts via publish command"
    git push origin main
    echo "☁️ Push successful."
else
    echo "⚠️ Git says there are no new changes to push. Did the scrubber fail?"
fi
