#!/bin/bash
while true; do
    # 1. Read the fan speed
    sh -c 'cat /sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input 2>/dev/null || echo 0' > /home/redwannabil/homeassistant/fan_speed.txt
    
    # 2. Read the Power Draw (Native Python Math)
    python3 -c 'import subprocess; pmic=subprocess.check_output(["vcgencmd","pmic_read_adc"]).decode("utf-8"); c={}; v={}; [c.update({l.split()[0].replace("_A",""): float(l.split("=")[1].replace("A","").replace("V",""))}) if "current" in l else v.update({l.split()[0].replace("_V",""): float(l.split("=")[1].replace("A","").replace("V",""))}) for l in pmic.split("\n") if "=" in l]; print(round((sum(c[n]*v[n] for n in c if n in v) * 1.1451) + 0.5879, 2))' > /home/redwannabil/homeassistant/power_draw.txt
    
    # Wait 15 seconds and do it again
    sleep 15
done
