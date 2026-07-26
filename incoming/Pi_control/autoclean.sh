#!/bin/bash
# Raspberry Pi Auto-Clean Script
# Runs nightly to clear caches, logs, and unused Docker images

# 1. Clean APT Package Cache
apt autoremove -y
apt clean

# 2. Keep only the last 3 days of system logs
journalctl --vacuum-time=3d

# 3. Purge all unused Docker images and networks
docker system prune -a -f

# 4. Clear the local user cache
rm -rf /home/redwannabil/.cache/*

echo "Cleanup completed on $(date)"
