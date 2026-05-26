#!/bin/bash
echo "Starting Nexus Hub Unified File Watcher (UTF-8 Optimized)..."

# ==========================================
# WATCHER 1: CCTV SSD (With Safety Excludes)
# ==========================================
inotifywait -m -r -e close_write -e moved_to -e create \
  --exclude '(Camera1|cctv|lost\+found)' "/mnt/cctv_ssd/" |
while read -r directory events filename; do
    echo "[CCTV SSD] Change detected: $filename. Syncing..."
    docker exec -e LANG=C.UTF-8 -u www-data nextcloud-app-1 php occ files:scan --path="redwansdrive/files/cctv_ssd"
done &

# ==========================================
# WATCHER 2: USB BACKUP PENDRIVE
# ==========================================
inotifywait -m -r -e close_write -e moved_to -e create "/mnt/usb_backup/" |
while read -r directory events filename; do
    echo "[USB BACKUP] Change detected: $filename. Syncing..."
    docker exec -e LANG=C.UTF-8 -u www-data nextcloud-app-1 php occ files:scan --path="redwansdrive/files/usb_backup"
done &

# ==========================================
# Keep the master script alive
# ==========================================
wait
