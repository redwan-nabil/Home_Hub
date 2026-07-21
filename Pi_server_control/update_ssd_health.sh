#!/bin/bash

# Force the script to load all system paths just in case
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# ==========================================
# 1. Main NVMe Health (OS Drive)
# ==========================================
# Using absolute path to /usr/sbin/nvme
NVME_USED=$(sudo /usr/sbin/nvme smart-log /dev/nvme0n1 | grep -i "percentage_used" | cut -d ':' -f 2 | tr -d ' %')

# Only update the Home Assistant file if NVME_USED is actually a number
if [[ "$NVME_USED" =~ ^[0-9]+$ ]]; then
    NVME_HEALTH=$((100 - NVME_USED))
    echo $NVME_HEALTH > /home/redwannabil/homeassistant/nvme_health.txt
fi

# ==========================================
# 2. External CCTV SSD Health
# ==========================================
# Use absolute paths for findmnt and lsblk
CCTV_PART=$(/usr/bin/findmnt -n -o SOURCE /mnt/cctv_ssd)

# Check if the dying CCTV drive has completely disconnected from the USB bus again
if [ -n "$CCTV_PART" ]; then
    CCTV_DRIVE=$(/usr/bin/lsblk -no pkname $CCTV_PART)
    
    # Using absolute path to /usr/sbin/smartctl
    SDA_HEALTH=$(sudo /usr/sbin/smartctl -A /dev/$CCTV_DRIVE | grep -i -E "Media_Wearout_Indicator|Wear_Leveling_Count|Percent_Lifetime_Remain|SSD_Life_Left" | head -n 1 | awk '{print $4}')
    
    # Only update if we successfully grabbed a number
    if [[ "$SDA_HEALTH" =~ ^[0-9]+$ ]]; then
        echo $SDA_HEALTH > /home/redwannabil/homeassistant/sda_health.txt
    fi
else
    # If the drive has physically crashed/disconnected, write 0 so you know it's dead
    echo 0 > /home/redwannabil/homeassistant/sda_health.txt
fi
