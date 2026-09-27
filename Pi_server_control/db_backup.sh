#!/bin/bash

# Define all containers that write to databases
CONTAINERS="matrix_server filebrowser_quantum firefly_app firefly_db forgejo uptime-kuma homeassistant ryot_library ryot_database immich_server immich_redis immich_postgres immich_machine_learning nextcloud-app-1 nextcloud-db-1 scrutiny n8n_course_setup mosquitto syncthing"

# 1. Stop the containers safely
sudo docker stop $CONTAINERS

# 2. Sync the databases to the SD card
sudo rsync -a --delete /mnt/120gb_ssd/Container_Databases/ /mnt/sdcard_storage/Database_Backups/

# 3. Restart all containers
sudo docker start $CONTAINERS
