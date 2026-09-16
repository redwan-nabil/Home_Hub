import time
import paho.mqtt.client as mqtt
from gpiozero import Buzzer

# ==========================================
# CONFIGURATION
# ==========================================
MQTT_SERVER = "192.168.0.40"
MQTT_PORT = 1883
MQTT_USER = "redwanmqtt"
MQTT_PASS = "abcd2005-"

COMMAND_TOPIC = "home/redwannabil/buzzer/cmd"
STATE_TOPIC = "home/redwannabil/buzzer/state"

# Initialize Buzzer on GPIO 17
buzzer = Buzzer(17)

# ==========================================
# MQTT CALLBACKS
# ==========================================
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"[MQTT] Connected with result code {reason_code}")
    if reason_code == 0:
        client.subscribe(COMMAND_TOPIC)
        client.publish(STATE_TOPIC, "OFF", retain=True)
    else:
        print("Connection failed! Please check MQTT_USER and MQTT_PASS.")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[CMD IN] {payload}")

    if payload == "ON":
        buzzer.on()                 # Solid continuous tone
        client.publish(STATE_TOPIC, "ON", retain=True)
    
    elif payload == "PULSE":
        buzzer.beep(0.5, 0.5)       # Continuous pulsing siren
        client.publish(STATE_TOPIC, "PULSE", retain=True)
    
    elif payload == "OFF":
        buzzer.off()
        client.publish(STATE_TOPIC, "OFF", retain=True)
    
    elif payload == "BEEP":
        # Non-blocking quick beep for doors
        buzzer.beep(on_time=0.1, off_time=0.1, n=1, background=True)

# ==========================================
# MAIN LOOP
# ==========================================
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Pi5_Buzzer_Node")
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

print("[SYSTEM] Starting Pi MQTT Buzzer Service...")
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_forever()
