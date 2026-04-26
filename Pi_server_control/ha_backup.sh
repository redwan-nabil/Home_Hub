#!/bin/bash
LOGFILE="/home/redwannabil/ha_backup.log"
DATE=$(date +"%Y-%m-%d_%H-%M")
FILENAME="HA_Backup_$DATE.tar.gz"

HA_DIR="/home/redwannabil/homeassistant"
USB_DIR="/mnt/usb_backup/ha_backups"

# Telegram Credentials (REPLACE WITH YOUR ACTUAL TOKEN!)
TOKEN="REDACTED_BY_SYSADMIN"
CHAT_ID="REDACTED_BY_SYSADMIN"

# Notification Function
send_msg() {
    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d chat_id="REDACTED_BY_SYSADMIN"
    -d text="$1" -d parse_mode="Markdown" > /dev/null
}

# Log the start
echo "$(date '+%Y-%m-%d %H:%M:%S') : --- HA BACKUP STARTED ---" >> "$LOGFILE"

# 1. Ensure USB Backup folder exists
mkdir -p "$USB_DIR"

# 2. Compress the Home Assistant folder to the USB Drive
echo "$(date '+%Y-%m-%d %H:%M:%S') : Zipping files to USB..." >> "$LOGFILE"
# nice and ionice ensure this compression doesn't slow down Nextcloud or HA while running
sudo sh -c "nice -n 19 ionice -c 3 tar -czvf $USB_DIR/$FILENAME $HA_DIR" >> "$LOGFILE" 2>&1

if [ $? -ne 0 ]; then
    send_msg "❌ *HA Backup Failed:* Error compressing files on $(hostname)"
    echo "$(date '+%Y-%m-%d %H:%M:%S') : Compression Failed." >> "$LOGFILE"
    exit 1
fi

# 3. Local Cleanup (Keep last 7 days on pendrive)
echo "$(date '+%Y-%m-%d %H:%M:%S') : Cleaning old local backups..." >> "$LOGFILE"
find "$USB_DIR" -name "HA_Backup_*.tar.gz" -type f -mtime +7 -delete >> "$LOGFILE" 2>&1

# 4. Cloud Cleanup (Delete HA files older than 1 day to save space)
echo "$(date '+%Y-%m-%d %H:%M:%S') : Cleaning old cloud backups..." >> "$LOGFILE"
rclone delete --config="/home/redwannabil/.config/rclone/rclone.conf" gdrive:HomeAssistant_Backups/ --min-age 1d >> "$LOGFILE" 2>&1

# 5. Upload to Google Drive
echo "$(date '+%Y-%m-%d %H:%M:%S') : Uploading to Google Drive..." >> "$LOGFILE"
nice -n 19 ionice -c 3 rclone copy --config="/home/redwannabil/.config/rclone/rclone.conf" "$USB_DIR/$FILENAME" gdrive:HomeAssistant_Backups/ >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    send_msg "✅ *Home Assistant Backup Successful!*%0A📁 Saved to USB: $FILENAME%0A☁️ Uploaded to Google Drive."
    echo "$(date '+%Y-%m-%d %H:%M:%S') : Upload Successful." >> "$LOGFILE"
else
    send_msg "⚠️ *HA Backup Alert:* Google Drive upload failed! Check Quota or logs."
    echo "$(date '+%Y-%m-%d %H:%M:%S') : Rclone Upload Failed." >> "$LOGFILE"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') : --- HA BACKUP COMPLETED ---" >> "$LOGFILE"
