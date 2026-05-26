#!/bin/bash

# 1. Calculate NVMe Health (100 - percentage_used)
NVME_USED=$(sudo nvme smart-log /dev/nvme0n1 | grep "percentage_used" | awk '{print $3}' | tr -d '%')
NVME_HEALTH=$((100 - NVME_USED))

# 2. Get CCTV SSD Health (Bulletproof dynamic detection)
# Find which disk /mnt/cctv_ssd is on
CCTV_PART=$(findmnt -n -o SOURCE /mnt/cctv_ssd)
# Get the base drive name (e.g., /dev/sdc from /dev/sdc1)
CCTV_DRIVE=$(lsblk -no pkname $CCTV_PART)
# Run smartctl on the base drive
SDA_HEALTH=$(sudo smartctl -A /dev/$CCTV_DRIVE | grep -i "Available_Reservd_Space" | awk '{print $4}')

# 3. Write plain numbers directly into the Home Assistant config folder
echo $NVME_HEALTH > /home/redwannabil/homeassistant/nvme_health.txt
echo $SDA_HEALTH > /home/redwannabil/homeassistant/sda_health.txt
