#!/bin/bash

# 1. PREVENT SYSTEM FREEZE & REDUCE HEAT
ionice -c 3 -p $$
renice -n 19 -p $$
export GOMAXPROCS=1

# Configuration
NAS_DIR="/mnt/nas_6tb_vault"
BACKUP_DIR="/mnt/backup"
REPO="$BACKUP_DIR/repo"
export RESTIC_PASSWORD_FILE="/root/.restic-pass"

# Home Assistant Configuration
HA_TOKEN="REDACTED_BY_SYSADMIN"
HA_URL="http://127.0.0.1:8123/api/states/sensor.nas_backup_status"

send_to_ha() {
    local state="$1"
    local message="$2"
    curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"state\": \"$state\", \"attributes\": {\"Message\": \"$message\", \"icon\": \"mdi:harddisk\"}}" \
         $HA_URL > /dev/null
}

# 2. MOUNT THE BACKUP DRIVE
mount $BACKUP_DIR > /dev/null 2>&1
sleep 3

if ! df -h | grep -q "$BACKUP_DIR"; then
    send_to_ha "Error" "Failed to mount backup drive! Aborted."
    exit 1
fi

# Natively trigger the OS to wake up and access the NAS directory
ls $NAS_DIR > /dev/null 2>&1
sleep 2

if ! df -h | grep -q "$NAS_DIR"; then
    send_to_ha "Error" "NAS drive is not mounted! Aborted."
    umount $BACKUP_DIR
    exit 1
fi

send_to_ha "Running" "Backup and verification in progress..."

# 3. INCREMENTAL BACKUP
restic -r $REPO backup $NAS_DIR > /tmp/backup.log 2>&1
if [ $? -ne 0 ]; then
    send_to_ha "Error" "Restic backup failed. Check /tmp/backup.log."
    umount $BACKUP_DIR
    exit 1
fi

# 4. PRUNE OLD BACKUPS
restic -r $REPO forget --keep-last 1 --prune >> /tmp/backup.log 2>&1

# 5. BIT-ROT SCAN & AUTO-REPAIR
SLICE=$(($(date +%-d) % 30))
CORRUPTED_FILES=$(sudo /usr/local/bin/nas-verify.py $SLICE 2>/dev/null)

if [ -n "$CORRUPTED_FILES" ]; then
    for file in $CORRUPTED_FILES; do
        restic -r $REPO restore latest --path "$file" --target / >> /tmp/backup.log 2>&1
    done
    send_to_ha "Warning" "Backup OK. Bit-Rot detected on slice $SLICE and auto-repaired."
else
    send_to_ha "Success" "Backup complete. Slice $SLICE checked cleanly."
fi

# 6. UNMOUNT & SLEEP
umount $BACKUP_DIR
