#!/bin/bash

# ==============================================================================
# ASYNCHRONOUS LAPTOP SYNC v4.5 (ARCHIVE + GOVERNOR + MUTEX + CODE 24 SAFE)
# ==============================================================================

# --- 🔒 MUTEX LOCK: PREVENT DUPLICATES ---
exec 9>"/tmp/laptop_sync.lock"
if ! flock -n 9; then
    exit 0 
fi

LOGFILE="/home/redwannabil/laptop_sync.log"
BASE_USB_DIR="/mnt/usb_backup/server_backup"
MOUNT_PT="/mnt/laptop_sync"
TRACKING_FILE="$BASE_USB_DIR/.last_sync_time"

# --- TELEGRAM SETTINGS ---
TOKEN="REDACTED_BY_SYSADMIN"
CHAT_ID="REDACTED_BY_SYSADMIN"

# --- LAPTOP SETTINGS ---
LAPTOP_IPS=("192.168.0.116" "192.168.0.50")
SMB_USER="PiBackup"               
SMB_PASS="REDACTED_BY_SYSADMIN"
SHARE_NAME="RPI Server all backup" 

# ==============================================================================

send_msg() {
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id="REDACTED_BY_SYSADMIN"
}

# ==============================================================================
# 🧠 THE CPU GOVERNOR (Docker-Aware & Silent)
# ==============================================================================
governor_loop() {
    local PAUSED=0
    while true; do
        LOAD=$(cat /proc/loadavg | awk '{print $1}')
        
        # Only look for active, aggressive docker commands
        DOCKER_BUSY=$(pgrep -f "docker compose|docker build|docker run" > /dev/null && echo 1 || echo 0)

        SPIKE=$(awk -v load="$LOAD" -v dbusy="$DOCKER_BUSY" 'BEGIN {if (load > 3.0 || dbusy == 1) print 1; else print 0}')
        SAFE=$(awk -v load="$LOAD" -v dbusy="$DOCKER_BUSY" 'BEGIN {if (load < 1.5 && dbusy == 0) print 1; else print 0}')

        if [ "$SPIKE" -eq 1 ] && [ "$PAUSED" -eq 0 ]; then
            sudo pkill -STOP -x "rsync" 2>/dev/null
            PAUSED=1
        elif [ "$SAFE" -eq 1 ] && [ "$PAUSED" -eq 1 ]; then
            sudo pkill -CONT -x "rsync" 2>/dev/null
            PAUSED=0
        fi
        sleep 10
    done
}

# 1. Find the newest backup file on the USB drive
NEWEST_BACKUP=$(find "$BASE_USB_DIR" -type f \( -name "*.img.gz" -o -name "*.tar.gz" \) -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)

if [ -z "$NEWEST_BACKUP" ]; then
    exit 0
fi

# 2. Check if we already synced this exact backup
if [ -f "$TRACKING_FILE" ]; then
    if [ "$NEWEST_BACKUP" -ot "$TRACKING_FILE" ]; then
        exit 0
    fi
fi

# 3. Check if Laptop is Online
ONLINE_IP=""
for IP in "${LAPTOP_IPS[@]}"; do
    if nc -z -w 3 "$IP" 445 > /dev/null 2>&1; then
        ONLINE_IP="$IP"
        break
    fi
done

if [ -z "$ONLINE_IP" ]; then
    exit 0
fi

# 4. LAPTOP IS ONLINE - START SYNC
send_msg "🚨 Redwan's predator is online. Backup files sync. Do not turn off the laptop untill finish!"

# Start the Governor
governor_loop &
GOVERNOR_PID=$!
trap "kill $GOVERNOR_PID 2>/dev/null" EXIT

sudo mkdir -p "$MOUNT_PT"
sudo mount -t cifs "//$ONLINE_IP/$SHARE_NAME" "$MOUNT_PT" -o username="$SMB_USER",password="REDACTED_BY_SYSADMIN"

if mountpoint -q "$MOUNT_PT"; then
    
    nice -n 19 ionice -c 3 sudo rsync -av --bwlimit=3000 "$BASE_USB_DIR/" "$MOUNT_PT/" >> "$LOGFILE" 2>&1
    SYNC_STATUS=$?
    
    # FIX: Accept 0 (Perfect) or 24 (Vanished files due to cleanup)
    if [ $SYNC_STATUS -eq 0 ] || [ $SYNC_STATUS -eq 24 ]; then
        touch "$TRACKING_FILE"
        send_msg "✅ Backup files sync done from RPI to Redwan's predator."
    else
        send_msg "⚠️ Laptop Sync finished with errors (Rsync Code: $SYNC_STATUS). Check logs."
    fi
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') : Cleaning old backups on Laptop..." >> "$LOGFILE"
    sudo find "$MOUNT_PT/RPI_OS_backup" -name "*.img.gz" -type f -mtime +3 -delete >> "$LOGFILE" 2>&1
    sudo find "$MOUNT_PT/HA_Backup" -name "*.tar.gz" -type f -mtime +3 -delete >> "$LOGFILE" 2>&1
    sudo find "$MOUNT_PT/Nextcloud_Admin_backup" -name "*.tar.gz" -type f -mtime +3 -delete >> "$LOGFILE" 2>&1

    sudo umount "$MOUNT_PT"
fi

exit 0
