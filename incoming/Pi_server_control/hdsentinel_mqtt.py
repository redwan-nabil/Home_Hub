import subprocess
import re
import json
import paho.mqtt.client as mqtt

# ==========================================
# MQTT CONFIGURATION (CHANGE THESE!)
# ==========================================
MQTT_BROKER = "192.168.0.40"
MQTT_PORT = 1883
MQTT_USER = "redwanmqtt"
MQTT_PASS = "abcd2005-"

def update_ha():
    # 1. Connect to the MQTT Broker
    client = mqtt.Client()
    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
        
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"MQTT Connection Failed: {e}")
        return

    # 2. Run HD Sentinel securely
    try:
        output = subprocess.check_output(["sudo", "/home/redwannabil/HDSentinel-armv8"]).decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error running HDSentinel: {e}")
        client.loop_stop()
        return

    # 3. Process each drive
    devices = output.split("HDD Device")
    for dev in devices[1:]:
        try:
            dev_path_match = re.search(r': /dev/([a-zA-Z0-9]+)', dev)
            if not dev_path_match: continue
            dev_path = dev_path_match.group(1)
            
            model_match = re.search(r'HDD Model ID\s*:\s*(.*)', dev)
            model = model_match.group(1).strip() if model_match else f"Drive {dev_path.upper()}"

            # Extract data points
            state = {}
            if m := re.search(r'Health\s*:\s*(\d+)\s*%', dev): state["health"] = int(m.group(1))
            if m := re.search(r'Temperature\s*:\s*(\d+)\s*°C', dev): state["temp"] = int(m.group(1))
            if m := re.search(r'Performance\s*:\s*(\d+)\s*%', dev): state["perf"] = int(m.group(1))
            if m := re.search(r'Power on time\s*:\s*(.*)', dev): state["poweron"] = m.group(1).strip()
            if m := re.search(r'Est\. lifetime\s*:\s*(.*)', dev): state["lifetime"] = m.group(1).strip()
            if m := re.search(r'Total written\s*:\s*(.*)', dev): state["written"] = m.group(1).strip()

            # Define the exact HA Entities (Matches your existing Dashboard YAML)
            sensors = [
                {"id": "health", "name": f"{model} Health", "unit": "%", "icon": "mdi:harddisk" if state.get("health", 0) > 50 else "mdi:harddisk-remove", "class": "battery"},
                {"id": "temp", "name": f"{model} Temp", "unit": "°C", "icon": "mdi:thermometer", "class": "temperature"},
                {"id": "perf", "name": f"{model} Performance", "unit": "%", "icon": "mdi:speedometer", "class": "battery"},
                {"id": "poweron", "name": f"{model} Power On Time", "unit": None, "icon": "mdi:clock-outline", "class": None},
                {"id": "lifetime", "name": f"{model} Est. Lifetime", "unit": None, "icon": "mdi:heart-pulse", "class": None},
                {"id": "written", "name": f"{model} Total Written", "unit": None, "icon": "mdi:database-edit", "class": None}
            ]

            # 4. Publish Auto-Discovery Configurations (Retained permanently)
            for s in sensors:
                if s["id"] in state:
                    config_topic = f"homeassistant/sensor/hdsentinel_{dev_path}/{s['id']}/config"
                    payload = {
                        "name": s["name"],
                        "object_id": f"drive_{s['id']}_{dev_path}", # Forces EXACT entity ID match (e.g. sensor.drive_health_nvme0)
                        "unique_id": f"hdsentinel_{dev_path}_{s['id']}",
                        "state_topic": f"hdsentinel/{dev_path}/state",
                        "value_template": f"{{{{ value_json.{s['id']} }}}}",
                        "device": {"identifiers": [f"hdsentinel_{dev_path}"], "name": f"Storage: {dev_path.upper()}", "manufacturer": "Hard Disk Sentinel"}
                    }
                    if s["unit"]: payload["unit_of_measurement"] = s["unit"]
                    if s["icon"]: payload["icon"] = s["icon"]
                    if s["class"]: payload["device_class"] = s["class"]
                    
                    # Push config with Retain=True
                    client.publish(config_topic, json.dumps(payload), retain=True)

            # 5. Publish the actual Live Data (Retained permanently)
            client.publish(f"hdsentinel/{dev_path}/state", json.dumps(state), retain=True)

        except Exception as e:
            pass

    # Clean up connection
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    update_ha()
