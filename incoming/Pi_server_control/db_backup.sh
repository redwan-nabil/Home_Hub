#!/bin/bash

# Define all containers that write to databases
CONTAINERS="matrix_server filebrowser_quantum firefly_app firefly_db forgejo uptime-kuma homeassistant ryot_library ryot_database immich_server immich_redis immich_postgres immich_machine_learning nextcloud-app-1 nextcloud-db-1 scrutiny n8n_course_setup mosquitto syncthing"

# Define Borg Repository path on the SD card
REPO="/mnt/sdcard_storage/borg_db_archive"
SQL_DUMP_DIR="/mnt/120gb_ssd/Container_Databases/immich_db_dump"

# Ensure the temporary SQL dump directory exists on the SATA SSD
sudo mkdir -p $SQL_DUMP_DIR

# 1. Dump Immich Database BEFORE stopping containers (Using sudo tee to fix permissions)
sudo docker exec -t immich_postgres pg_dumpall -c -U postgres | sudo tee "$SQL_DUMP_DIR/immich_latest.sql" > /dev/null

# 2. Stop the containers safely
sudo docker stop $CONTAINERS

# 3. Archive everything to the SD card using Borg (Deduplicated & Compressed)
sudo borg create --stats --compression zstd,3 \
    $REPO::"db-backup-{now:%Y-%m-%d_%H:%M}" \
    /mnt/120gb_ssd/Container_Databases/ \
    /mnt/120gb_ssd/docker_data/volumes/

# 4. Restart all containers immediately
sudo docker start $CONTAINERS

# 5. Prune old backups on the SD card (Keep 7 daily, 4 weekly)
sudo borg prune -v --list --keep-daily=7 --keep-weekly=4 $REPO
