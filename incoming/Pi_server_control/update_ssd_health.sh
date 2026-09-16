#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# ==========================================
# 1. Main NVMe Health (OS Drive)
# ==========================================
NVME_USED=$(sudo /usr/sbin/nvme smart-log /dev/nvme0n1 | grep -i "percentage_used" | cut -d ':' -f 2 | tr -d ' %')
if [[ "$NVME_USED" =~ ^[0-9]+$ ]]; then
    echo $((100 - NVME_USED)) > /home/redwannabil/homeassistant/nvme_health.txt
fi

# ==========================================
# 2. 120GB Database SSD Health
# ==========================================
# Ask the LUKS engine for the exact physical drive
SSD_PART=$(sudo cryptsetup status 120gb_ssd_vault 2>/dev/null | awk '/device:/ {print $2}')

if [ -n "$SSD_PART" ]; then
    SSD_DRIVE=$(lsblk -no pkname "$SSD_PART" 2>/dev/null | tr -d ' ')
    if [ -z "$SSD_DRIVE" ]; then SSD_DRIVE=$(basename "$SSD_PART"); fi
    
    # Try to get detailed wear leveling
    SSD_HEALTH=$(sudo smartctl -A /dev/$SSD_DRIVE 2>/dev/null | grep -i -E "Media_Wearout_Indicator|Wear_Leveling_Count|Percent_Lifetime_Remain|SSD_Life_Left" | head -n 1 | awk '{print $4}')
    SSD_HEALTH=$(echo "$SSD_HEALTH" | sed 's/^0*//' | tr -cd '0-9')
    
    # FALLBACK: If the SSD hides its wear level, check if it's PASSED
    if [ -z "$SSD_HEALTH" ] || [ "$SSD_HEALTH" -eq 0 ]; then
        if sudo smartctl -H /dev/$SSD_DRIVE 2>/dev/null | grep -q "PASSED"; then
            SSD_HEALTH=100
        else
            SSD_HEALTH=10
        fi
    fi
    echo "$SSD_HEALTH" > /home/redwannabil/homeassistant/sdc_health.txt
else
    echo 0 > /home/redwannabil/homeassistant/sdc_health.txt
fi

# ==========================================
# 3. External CCTV HDD Health (HDSentinel Math)
# ==========================================
HDD_PART=$(sudo cryptsetup status cctv_hdd 2>/dev/null | awk '/device:/ {print $2}')

if [ -n "$HDD_PART" ]; then
    HDD_DRIVE=$(lsblk -no pkname "$HDD_PART" 2>/dev/null | tr -d ' ')
    if [ -z "$HDD_DRIVE" ]; then HDD_DRIVE=$(basename "$HDD_PART"); fi
    
    # $NF guarantees we grab the absolute last column (RAW_VALUE) regardless of spacing
    REALLOC=$(sudo smartctl -A /dev/$HDD_DRIVE 2>/dev/null | grep -i "Reallocated_Sector" | awk '{print $NF}' | tr -cd '0-9')
    PENDING=$(sudo smartctl -A /dev/$HDD_DRIVE 2>/dev/null | grep -i "Current_Pending_Sector" | awk '{print $NF}' | tr -cd '0-9')
    
    REALLOC=${REALLOC:-0}
    PENDING=${PENDING:-0}
    
    # Deduct 1.5% for every dead sector, and 5% for every actively failing sector
    PENALTY_REALLOC=$(( (REALLOC * 15) / 10 ))
    PENALTY_PENDING=$(( PENDING * 5 ))
    HDD_HEALTH=$(( 100 - PENALTY_REALLOC - PENALTY_PENDING ))
    
    # Cap health between 1 and 100
    if [ "$HDD_HEALTH" -lt 1 ]; then HDD_HEALTH=1; fi
    if [ "$HDD_HEALTH" -gt 100 ]; then HDD_HEALTH=100; fi
    
    echo "$HDD_HEALTH" > /home/redwannabil/homeassistant/cctv_hdd_health.txt
else
    echo 0 > /home/redwannabil/homeassistant/cctv_hdd_health.txt
fi

# ==========================================
# 4. Fix Permissions for Home Assistant
# ==========================================
sudo chmod 666 /home/redwannabil/homeassistant/*.txt
