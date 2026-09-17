import time
import threading
import serial
import paho.mqtt.client as mqtt

# ==========================================
# CONFIGURATION
# ==========================================
MQTT_SERVER = "192.168.0.40"
MQTT_PORT = 1883
MQTT_USER = "redwanmqtt"
MQTT_PASS = "abcd2005-"

COMMAND_TOPIC = "home/redwannabil/sim/cmd"
STATE_TOPIC = "home/redwannabil/sim/state"

EMERGENCY_NUMBERS = ["+8801794684164", "+8801342570575"] # Replace with your targets[cite: 1]

# ==========================================
# HARDWARE INITIALIZATION
# ==========================================
# Uses the hardware mapped port /dev/serial0 at 9600 baud[cite: 1]
try:
    sim = serial.Serial('/dev/serial0', 9600, timeout=1)
    print("[SYSTEM] SIM800L Serial Port Opened Successfully.")
except Exception as e:
    print(f"[SYSTEM ERROR] Could not open serial port: {e}")

alarm_active = False

# ==========================================
# SIM MODULE AT COMMAND SEQUENCE
# ==========================================
def emergency_sos(message):
    """Executes consecutive SMS alerts and live call sequences over AT commands"""
    for number in EMERGENCY_NUMBERS:
        try:
            print(f"[SOS] Targeting: {number}")
            # 1. Initialize text message format[cite: 1]
            sim.write(b'AT+CMGF=1\r\n')
            time.sleep(0.5)
            
            # 2. Stage destination directory routing[cite: 1]
            sim.write(f'AT+CMGS="{number}"\r\n'.encode())
            time.sleep(0.5)
            
            # 3. Write payload text and append Hex 1A (Ctrl+Z) to send[cite: 1]
            sim.write(message.encode() + b'\x1A')
            time.sleep(4)
            print(f"[SOS] SMS dispatched to {number}. Initializing voice call link....")
            
            # 4. Dial emergency route line[cite: 1]
            sim.write(f"ATD{number};\r\n".encode())
            time.sleep(20) # Keep line open for 20 seconds to force loud ring vibration[cite: 1]
            
            # 5. Terminate voice channel link[cite: 1]
            sim.write(b"ATH\r\n")
            time.sleep(1)
        except Exception as e:
            print(f"[SIM ERROR] Failed executing emergency pipeline for {number}: {e}")

def reset_alarm_lock():
    global alarm_active
    time.sleep(60) # Protects system from duplicate trigger looping within 1 minute[cite: 1]
    alarm_active = False

def trigger_full_alarm(msg):
    global alarm_active
    if not alarm_active:
        alarm_active = True
        print(f"[ALARM ACTIVATE] Reason: {msg}")
        threading.Thread(target=reset_alarm_lock, daemon=True).start()
        threading.Thread(target=emergency_sos, args=(msg,), daemon=True).start()

# ==========================================
# MQTT CALLBACKS
# ==========================================
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"[MQTT] Connected with result code {reason_code}")
    if reason_code == 0:
        client.subscribe(COMMAND_TOPIC)
        client.publish(STATE_TOPIC, "READY", retain=True)

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"[CMD IN] Received: {payload}")

    if payload.startswith("SOS"):
        # You can pass a custom message like "SOS: Fire Detected!"
        custom_message = payload.replace("SOS:", "").strip()
        if not custom_message or custom_message == "SOS":
            custom_message = "EMERGENCY: Home Alarm Triggered!"
            
        client.publish(STATE_TOPIC, "CALLING", retain=True)
        trigger_full_alarm(custom_message)
        
        # Reset state to READY after 5 seconds
        time.sleep(5)
        client.publish(STATE_TOPIC, "READY", retain=True)

# ==========================================
# MAIN LOOP
# ==========================================
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="PiServer_SIM_Node")
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

print("[SYSTEM] Starting Pi MQTT SIM Service...")
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_forever()
