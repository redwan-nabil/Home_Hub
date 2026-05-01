import socket
import math
import time
import collections
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"
UDP_PORT = 5500
MQTT_BROKER = "192.168.0.40"
MQTT_TOPIC = "home/room/occupancy"

# --- DUAL-THRESHOLD RADAR (HYSTERESIS) ---
TRIGGER_THRESHOLD = 0.25     # HIGH: Hard to trigger (ignores empty room AC)
MAINTAIN_THRESHOLD = 0.08    # LOW: Easy to stay on (catches typing/sitting)
HOLD_TIME = 30               # Keep room "Occupied" for 30 seconds after last movement
WINDOW_SIZE = 5              # Shrink the buffer to catch fast movements without diluting

# --- SETUP ---
client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
    print(f"Connected to MQTT Broker at {MQTT_BROKER}")
except Exception as e:
    print(f"MQTT Connection Failed: {e}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

amplitude_buffer = collections.deque(maxlen=WINDOW_SIZE)
baseline_amp = None
is_occupied = False
last_motion_time = 0

print(f"Dual-Threshold Radar Online. Trigger: {TRIGGER_THRESHOLD} | Maintain: {MAINTAIN_THRESHOLD}")
print(f"Listening on UDP port {UDP_PORT}...")

# --- MAIN RADAR LOOP ---
try:
    while True:
        data, addr = sock.recvfrom(4096)
        line = data.decode('utf-8', errors='ignore').strip()

        if 'CSI_DATA' in line:
            try:
                # Extract the raw numbers between the brackets
                raw_csi_string = line[line.find("[")+1:line.find("]")]
                csi_values = [int(x) for x in raw_csi_string.split(',')]
                
                # Calculate the physical amplitude of the subcarriers
                amplitudes = [math.sqrt(csi_values[i]**2 + csi_values[i+1]**2) for i in range(0, len(csi_values), 2)]
                current_packet_avg = sum(amplitudes) / len(amplitudes)
                
                # Add to our moving average buffer
                amplitude_buffer.append(current_packet_avg)
                
                # Wait for the buffer to fill up before doing math
                if len(amplitude_buffer) < WINDOW_SIZE:
                    continue

                # Calculate the smoothed current state of the room
                smoothed_avg = sum(amplitude_buffer) / WINDOW_SIZE

                # Set the initial baseline of the empty room
                if baseline_amp is None:
                    baseline_amp = smoothed_avg
                    print("--- Initial Baseline Calibrated ---")
                    continue

                # Calculate Variance against the baseline
                variance = abs(smoothed_avg - baseline_amp) / baseline_amp

                if not is_occupied:
                    # ---> X-RAY VISION FOR EMPTY STATE <---
                    print(f"Scanning empty room... Variance: {variance:.3f}")
                    
                    # ROOM IS EMPTY: Look for a massive spike to prove entry
                    if variance > TRIGGER_THRESHOLD:
                        is_occupied = True
                        last_motion_time = time.time()
                        print(f"\n[>>>] HUMAN ENTERED! (Spike: {variance:.3f})")
                        client.publish(MQTT_TOPIC, "ON")
                    else:
                        # Slowly learn the AC background noise
                        baseline_amp = (baseline_amp * 0.999) + (smoothed_avg * 0.001)
                
                else:
                    # Calculate how long it's been since you last moved
                    time_since_motion = time.time() - last_motion_time
                    
                    # ---> X-RAY VISION FOR OCCUPIED STATE <---
                    print(f"Holding ON... Variance: {variance:.3f} | Timer: {HOLD_TIME - time_since_motion:.1f}s left")

                    # ROOM IS OCCUPIED: Look for tiny ripples to keep the lights on
                    if variance > MAINTAIN_THRESHOLD:
                        last_motion_time = time.time() # Reset the 30-second clock!
                    
                    if time_since_motion > HOLD_TIME:
                        is_occupied = False
                        print(f"\n[<<<] ROOM EMPTY. (No ripples > {MAINTAIN_THRESHOLD} for {HOLD_TIME}s)")
                        client.publish(MQTT_TOPIC, "OFF")
                        # Hard-reset the baseline to the empty room
                        baseline_amp = smoothed_avg 

            except Exception as e:
                # Ignore corrupted WiFi packets
                pass

except KeyboardInterrupt:
    print("Shutting down radar...")
    client.loop_stop()
    sock.close()
