#!/bin/bash

# 1. Check CPU Temperature
TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
TEMP_C=$((TEMP/1000))
if [ "$TEMP_C" -ge 60 ]; then
    /usr/local/bin/pi_alert "🔥 WARNING: Raspberry Pi is overheating! Current Temp: ${TEMP_C}°C"
fi

# 2. Check SD Card Read-Only status (Dying Card / Corruption)
# This looks at the root file system to see if it is locked in "ro" (read-only) mode.
if mount | grep " / " | grep -q "ro,"; then
    /usr/local/bin/pi_alert "🚨 CRITICAL: SD Card has switched to READ-ONLY mode! The drive is failing. Please replace hardware."
fi

# 3. Check Disk Space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -ge 60 ]; then
    /usr/local/bin/pi_alert "💾 STORAGE ALERT: Raspberry Pi SD card is ${DISK_USAGE}% full!"
fi
