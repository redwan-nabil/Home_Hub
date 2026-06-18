#!/bin/bash
while true; do
    # Read the fan speed and write it directly to the Home Assistant config folder
    sh -c 'cat /sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input 2>/dev/null || echo 0' > /home/redwannabil/homeassistant/fan_speed.txt

    # Wait 15 seconds and do it again
    sleep 15
done
