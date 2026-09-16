#!/bin/bash

# ==============================================================================
# RPI 5 UNIFIED BACKUP PIPELINE v5.0 (SPLIT-DRIVE PLUG & PLAY ARCHITECTURE)
# ==============================================================================

LOGFILE="/home/redwannabil/master_backup.log"
DATE=$(date +"%Y-%m-%d_%H-%M")

# --- DIRECTORIES ---
BASE_USB_DIR="/mnt/usb_backup/server_backup"
OS_DIR="$BASE_USB_DIR/RPI_OS_backup"
DB_DIR="$BASE_USB_DIR/Database_SSD_backup"
HA_DIR="$BASE_USB_DIR/HA_Backup"
NC_DIR="$BASE_USB_DIR/Nextcloud_Admin_backup"

SSD_DB_SOURCE="/mnt/120gb_ssd/Container_Databases"
HA_SOURCE="/home/redwannabil/homeassistant"
NC_SOURCE="/home/redwannabil/nextcloud"

# --- TELEGRAM SETTINGS ---
TOKEN="REDACTED_BY_SYSADMIN"
CHAT_ID="REDACTED_BY_SYSADMIN"

# ==============================================================================

send_msg() {
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id="REDACTED_BY_SYSADMIN"
}

# ==============================================================================
# 🧠 THE CPU GOVERNOR (Docker-Aware)
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
            sudo pkill -STOP -x "dd" 2>/dev/null
            sudo pkill -STOP -x "gzip" 2>/dev/null
            sudo pkill -STOP -x "tar" 2>/dev/null
            sudo pkill -STOP -x "rclone" 2>/dev/null
            PAUSED=1
        elif [ "$SAFE" -eq 1 ] && [ "$PAUSED" -eq 1 ]; then
            sudo pkill -CONT -x "dd" 2>/dev/null
            sudo pkill -CONT -x "gzip" 2>/dev/null
            sudo pkill -CONT -x "tar" 2>/dev/null
            sudo pkill -CONT -x "rclone" 2>/dev/null
            PAUSED=0
        fi
        sleep 10
    done
}

# Start the Governor and make sure it dies when the script finishes
governor_loop &
GOVERNOR_PID=$!
trap "kill $GOVERNOR_PID 2>/dev/null" EXIT

# ==============================================================================
# PIPELINE EXECUTION
# ==============================================================================

echo "======================================================" >> "$LOGFILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') : --- UNIFIED BACKUP STARTED ---" >> "$LOGFILE"
send_msg "🚀 *Backup Pipeline Started:* Preparing split-architecture system..."

# --- STEP 0: PREPARE FOLDERS & CLEANUP ---
sudo mkdir -p "$OS_DIR" "$DB_DIR" "$HA_DIR" "$NC_DIR"

sudo apt autoremove -y >> "$LOGFILE" 2>&1
sudo apt clean >> "$LOGFILE" 2>&1
sudo rm -f /tmp/print_*.pdf /tmp/scanned_*.pdf /home/redwannabil/*.pdf >> "$LOGFILE" 2>&1
sudo journalctl --vacuum-time=3d >> "$LOGFILE" 2>&1
sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

# --- STEP 1: THROTTLED OS NVMe BACKUP ---
echo "$(date '+%Y-%m-%d %H:%M:%S') : [1/4] Starting Throttled NVMe OS Backup..." >> "$LOGFILE"
OS_FILENAME="Pi_OS_$DATE.img.gz"

sudo sh -c "dd if=/dev/nvme0n1 bs=4M | pv -q -L 8m | gzip > $OS_DIR/$OS_FILENAME" >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    send_msg "💽 *Local USB Success:* Pi OS image saved safely!"
else
    send_msg "❌ *FATAL ERROR:* Pi OS backup failed!"
    exit 1
fi

# --- STEP 2: SSD DATABASE BACKUP (NEW) ---
echo "$(date '+%Y-%m-%d %H:%M:%S') : [2/4] Starting SSD Database Backup..." >> "$LOGFILE"
DB_FILENAME="SSD_Databases_$DATE.tar.gz"

# Temporarily stop all Docker containers so the databases are safe to copy
sudo systemctl stop docker docker.socket >> "$LOGFILE" 2>&1

sudo tar -czvf "$DB_DIR/$DB_FILENAME" -C /mnt/120gb_ssd Container_Databases >> "$LOGFILE" 2>&1
DB_BKP_STATUS=$?

# Instantly wake Docker back up
sudo systemctl start docker >> "$LOGFILE" 2>&1

if [ $DB_BKP_STATUS -eq 0 ]; then
    send_msg "💽 *Local USB Success:* 120GB SSD Databases safely archived!"
else
    send_msg "❌ *FATAL ERROR:* 120GB SSD Database backup failed!"
    exit 1
fi

# --- STEP 3: HOME ASSISTANT FOLDER BACKUP ---
echo "$(date '+%Y-%m-%d %H:%M:%S') : [3/4] Starting Home Assistant Backup..." >> "$LOGFILE"
HA_FILENAME="HA_Backup_$DATE.tar.gz"

sudo tar -czvf "$HA_DIR/$HA_FILENAME" "$HA_SOURCE" >> "$LOGFILE" 2>&1
if [ $? -eq 0 ] || [ $? -eq 1 ]; then
    send_msg "💽 *Local USB Success:* Home Assistant config saved!"
fi

# --- STEP 4: NEXTCLOUD ADMIN BACKUP ---
echo "$(date '+%Y-%m-%d %H:%M:%S') : [4/4] Starting Nextcloud Settings Backup..." >> "$LOGFILE"
NC_FILENAME="Nextcloud_Admin_$DATE.tar.gz"

sudo tar --exclude='*/data/*' -czvf "$NC_DIR/$NC_FILENAME" "$NC_SOURCE" >> "$LOGFILE" 2>&1
if [ $? -eq 0 ] || [ $? -eq 1 ]; then
    send_msg "💽 *Local USB Success:* Nextcloud Admin saved!"
fi

# --- STEP 5: CLOUD UPLOAD (G-DRIVE) ---
echo "$(date '+%Y-%m-%d %H:%M:%S') : Uploading to Google Drive..." >> "$LOGFILE"

# Clean old cloud backups
sudo rclone delete --config="/home/redwannabil/.config/rclone/rclone.conf" gdrive:Server_Backups/HA_Backup/ --min-age 48h >> "$LOGFILE" 2>&1
sudo rclone delete --config="/home/redwannabil/.config/rclone/rclone.conf" gdrive:Server_Backups/NC_Backup/ --min-age 48h >> "$LOGFILE" 2>&1
sudo rclone delete --config="/home/redwannabil/.config/rclone/rclone.conf" gdrive:Server_Backups/Database_Backup/ --min-age 48h >> "$LOGFILE" 2>&1

# Upload the new backups
nice -n 19 ionice -c 3 sudo rclone copy --config="/home/redwannabil/.config/rclone/rclone.conf" "$HA_DIR/$HA_FILENAME" gdrive:Server_Backups/HA_Backup/ >> "$LOGFILE" 2>&1
nice -n 19 ionice -c 3 sudo rclone copy --config="/home/redwannabil/.config/rclone/rclone.conf" "$NC_DIR/$NC_FILENAME" gdrive:Server_Backups/NC_Backup/ >> "$LOGFILE" 2>&1
nice -n 19 ionice -c 3 sudo rclone copy --config="/home/redwannabil/.config/rclone/rclone.conf" "$DB_DIR/$DB_FILENAME" gdrive:Server_Backups/Database_Backup/ >> "$LOGFILE" 2>&1

send_msg "☁️ *Cloud Sync Success:* HA, Nextcloud & Databases safely uploaded!"

# --- STEP 6: EXACTLY 3 LOCAL USB RETENTION ---
echo "$(date '+%Y-%m-%d %H:%M:%S') : Cleaning old local USB backups (Keeping 3 most recent)..." >> "$LOGFILE"

ls -t "$OS_DIR"/*.img.gz 2>/dev/null | tail -n +4 | xargs -I {} sudo rm -f "{}" >> "$LOGFILE" 2>&1
ls -t "$DB_DIR"/*.tar.gz 2>/dev/null | tail -n +4 | xargs -I {} sudo rm -f "{}" >> "$LOGFILE" 2>&1
ls -t "$HA_DIR"/*.tar.gz 2>/dev/null | tail -n +4 | xargs -I {} sudo rm -f "{}" >> "$LOGFILE" 2>&1
ls -t "$NC_DIR"/*.tar.gz 2>/dev/null | tail -n +4 | xargs -I {} sudo rm -f "{}" >> "$LOGFILE" 2>&1

send_msg "🏁 *PIPELINE COMPLETE:* All automated split-architecture backup tasks finished safely."
echo "$(date '+%Y-%m-%d %H:%M:%S') : --- PIPELINE FINISHED SUCCESSFULLY ---" >> "$LOGFILE"

exit 0
