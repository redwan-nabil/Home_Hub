import subprocess
import re
import requests

# ==========================================
# HOME ASSISTANT CONFIGURATION
# ==========================================
HA_URL = "http://192.168.0.40:8123"
HA_TOKEN = "REDACTED_BY_SYSADMIN"
HEADERS = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}

def update_ha():
    try:
        # Run HDSentinel (Assuming script is run as root)
        output = subprocess.check_output(["/home/redwannabil/HDSentinel-armv8"]).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error running HDSentinel: {e}")
        return

    # Split output by device blocks to process each drive independently
    devices = output.split("HDD Device")
    
    for dev in devices[1:]:
        try:
            # 1. Extract Drive Path (e.g., nvme0, sdc) and Model
            dev_path_match = re.search(r': /dev/([a-zA-Z0-9]+)', dev)
            if not dev_path_match:
                continue
            dev_path = dev_path_match.group(1)
            
            model_match = re.search(r'HDD Model ID\s*:\s*(.*)', dev)
            model = model_match.group(1).strip() if model_match else f"Drive {dev_path.upper()}"
            
            # 2. Extract & Push Health
            health_match = re.search(r'Health\s*:\s*(\d+)\s*%', dev)
            if health_match:
                health_val = int(health_match.group(1))
                payload = {"state": health_val, "attributes": {"unit_of_measurement": "%", "friendly_name": f"{model} Health", "icon": "mdi:harddisk" if health_val > 50 else "mdi:harddisk-remove", "device_class": "battery"}}
                requests.post(f"{HA_URL}/api/states/sensor.drive_health_{dev_path}", headers=HEADERS, json=payload, timeout=5)

            # 3. Extract & Push Temperature
            temp_match = re.search(r'Temperature\s*:\s*(\d+)\s*°C', dev)
            if temp_match:
                payload = {"state": int(temp_match.group(1)), "attributes": {"unit_of_measurement": "°C", "friendly_name": f"{model} Temp", "device_class": "temperature"}}
                requests.post(f"{HA_URL}/api/states/sensor.drive_temp_{dev_path}", headers=HEADERS, json=payload, timeout=5)

            # 4. Extract & Push Performance
            perf_match = re.search(r'Performance\s*:\s*(\d+)\s*%', dev)
            if perf_match:
                payload = {"state": int(perf_match.group(1)), "attributes": {"unit_of_measurement": "%", "friendly_name": f"{model} Performance", "icon": "mdi:speedometer", "device_class": "battery"}}
                requests.post(f"{HA_URL}/api/states/sensor.drive_perf_{dev_path}", headers=HEADERS, json=payload, timeout=5)

            # 5. Extract & Push Power On Time
            power_match = re.search(r'Power on time\s*:\s*(.*)', dev)
            if power_match and power_match.group(1).strip():
                payload = {"state": power_match.group(1).strip(), "attributes": {"friendly_name": f"{model} Power On Time", "icon": "mdi:clock-outline"}}
                requests.post(f"{HA_URL}/api/states/sensor.drive_poweron_{dev_path}", headers=HEADERS, json=payload, timeout=5)

            # 6. Extract & Push Est. Lifetime
            life_match = re.search(r'Est\. lifetime\s*:\s*(.*)', dev)
            if life_match and life_match.group(1).strip():
                payload = {"state": life_match.group(1).strip(), "attributes": {"friendly_name": f"{model} Est. Lifetime", "icon": "mdi:heart-pulse"}}
                requests.post(f"{HA_URL}/api/states/sensor.drive_lifetime_{dev_path}", headers=HEADERS, json=payload, timeout=5)

            # 7. Extract & Push Total Written (SSDs only)
            written_match = re.search(r'Total written\s*:\s*(.*)', dev)
            if written_match and written_match.group(1).strip():
                payload = {"state": written_match.group(1).strip(), "attributes": {"friendly_name": f"{model} Total Written", "icon": "mdi:database-edit"}}
                requests.post(f"{HA_URL}/api/states/sensor.drive_written_{dev_path}", headers=HEADERS, json=payload, timeout=5)
                
        except Exception as e:
            pass

if __name__ == "__main__":
    update_ha()
