#!/bin/bash

# Define all containers to stop during backup
CONTAINERS="kiwix filebrowser_quantum syncthing immich_server immich_postgres immich_redis immich_machine_learning homeassistant matrix_server firefly_app firefly_db forgejo uptime-kuma ryot_library ryot_database scrutiny n8n_course_setup mosquitto cloudflared"

# --- USB PENDRIVE VERIFICATION ---
USB_UUID="a69224ea-f1cc-4680-a4fe-8598eb5accc6"
MOUNT_POINT="/mnt/usb_backup"

# --- HOME ASSISTANT API CONFIGURATION ---
HA_TOKEN="REDACTED_BY_SYSADMIN"
HA_URL="http://192.168.0.40:8123/api/states/sensor.db_backup_status"

send_to_ha() {
    local state="$1"
    local message="$2"
    curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"state\": \"$state\", \"attributes\": {\"Message\": \"$message\", \"icon\": \"mdi:database-lock\"}}" \
         $HA_URL > /dev/null
}

send_to_ha "Running" "Checking USB mount and initializing database backup..."

# Ensure the physical USB drive is actually mounted before proceeding
if ! findmnt -rn -S UUID=$USB_UUID -T $MOUNT_POINT > /dev/null; then
    send_to_ha "Error" "USB drive not mounted. Aborted."
    exit 1
fi

REPO="$MOUNT_POINT/server_backup/Database_SSD_backup/borg_db_archive"
SQL_DUMP_DIR="/mnt/120gb_ssd/Container_Databases/immich_db_dump"

sudo mkdir -p $SQL_DUMP_DIR
sudo mkdir -p "$MOUNT_POINT/server_backup/Database_SSD_backup"

if [ ! -d "$REPO" ]; then
    sudo borg init -e none "$REPO"
fi

# 1. Dump Immich Database
send_to_ha "Running" "Dumping Immich PostgreSQL database..."
sudo docker exec -t immich_postgres pg_dumpall -c -U postgres | sudo tee "$SQL_DUMP_DIR/immich_latest.sql" > /dev/null

# 2. Stop containers safely
send_to_ha "Running" "Stopping Docker containers for safe file archival..."
sudo docker stop $CONTAINERS

# 3. Archive using Borg
send_to_ha "Running" "Archiving databases and volumes via Borg..."
sudo borg create --stats --compression zstd,3 \
    $REPO::"db-backup-{now:%Y-%m-%d_%H:%M}" \
    /mnt/120gb_ssd/Container_Databases/ \
    /mnt/120gb_ssd/docker_data/volumes/
Borg_Status=$?

# 4. Restart containers immediately
send_to_ha "Running" "Restarting Docker containers..."
sudo docker start $CONTAINERS

if [ $Borg_Status -ne 0 ]; then
    send_to_ha "Error" "Borg archive creation failed!"
    exit 1
fi

# 5. Prune old backups
send_to_ha "Running" "Pruning old database backups..."
sudo borg prune -v --list --keep-daily=7 --keep-weekly=4 $REPO

send_to_ha "Success" "Database backup completed and pruned successfully."
