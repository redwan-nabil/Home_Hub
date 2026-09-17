import os
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

import json
import time
from gpiozero import DigitalInputDevice
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
PIR_PIN = 26
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = "redwanmqtt"
MQTT_PASSWORD = "REDACTED_BY_SYSADMIN"

DEVICE_ID = "pi5_pir_sensor"
STATE_TOPIC = f"homeassistant/binary_sensor/{DEVICE_ID}/state"
CONFIG_TOPIC = f"homeassistant/binary_sensor/{DEVICE_ID}/config"

# --- SOFT CALIBRATION SETTINGS ---
# We poll the sensor every 0.2 seconds.
POLL_INTERVAL = 0.2           

# Must detect motion 2 times in a row (~0.4s) to ignore 1-millisecond Wi-Fi noise spikes.
MOTION_CONFIRM_COUNT = 2      

# Must detect NO motion 25 times in a row (~5.0 seconds) to safely declare room empty.
CLEAR_CONFIRM_COUNT = 25      

# --- MQTT SETUP ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="pi5_gpio_daemon")
if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()

discovery_payload = {
    "name": "Pi 5 Room Motion",
    "unique_id": DEVICE_ID,
    "state_topic": STATE_TOPIC,
    "device_class": "motion",
    "payload_on": "ON",
    "payload_off": "OFF",
    "device": {
        "identifiers": ["pi5_gpio_node"],
        "name": "Raspberry Pi 5 Sensors",
        "model": "Raspberry Pi 5 Model B",
        "manufacturer": "Raspberry Pi Foundation"
    }
}
client.publish(CONFIG_TOPIC, json.dumps(discovery_payload), retain=True)

# --- SMART SENSOR LOGIC ---
# pull_up=False forces the pin to explicitly read 0V (OFF) when idle
pir = DigitalInputDevice(PIR_PIN, pull_up=False)

current_state = "OFF"
high_counter = 0
low_counter = 0

# Force initial state to OFF to clear Home Assistant cache
client.publish(STATE_TOPIC, "OFF", qos=1)
print("Calibration complete. Polling sensor...")

try:
    while True:
        # Read the raw physical pin value
        is_active = pir.value

        if is_active:
            high_counter += 1
            low_counter = 0
            
            # If it stays high long enough, trigger ON
            if high_counter >= MOTION_CONFIRM_COUNT and current_state == "OFF":
                current_state = "ON"
                client.publish(STATE_TOPIC, "ON", qos=1)
                print(">>> Motion Confirmed!")
                
        else:
            low_counter += 1
            high_counter = 0
            
            # If it stays low long enough, trigger OFF
            if low_counter >= CLEAR_CONFIRM_COUNT and current_state == "ON":
                current_state = "OFF"
                client.publish(STATE_TOPIC, "OFF", qos=1)
                print("--- Room Cleared.")
                
        time.sleep(POLL_INTERVAL)
        
except KeyboardInterrupt:
    print("Exiting...")
