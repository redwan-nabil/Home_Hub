import socket
import math
import csv
import time
import os

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"
UDP_PORT = 5500

# The label for the data you are about to record.
# Change this word before running the script! 
# Examples: "empty", "nabil_walking", "mom_walking", "hallway_walking"
CURRENT_LABEL = "empty" 

FILENAME = f"/app/data/{CURRENT_LABEL}_{int(time.time())}.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"CSI Recorder Online.")
print(f"Saving data for label: [{CURRENT_LABEL}] to {FILENAME}")
print("Press Ctrl+C to stop recording.")

# Ensure data directory exists
os.makedirs("/app/data", exist_ok=True)

try:
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row (Subcarrier 1-64, plus the label)
        header = [f"sub_{i}" for i in range(64)] + ["label"]
        writer.writerow(header)

        packet_count = 0
        while True:
            data, addr = sock.recvfrom(4096)
            line = data.decode('utf-8', errors='ignore').strip()

            if 'CSI_DATA' in line:
                try:
                    raw_csi_string = line[line.find("[")+1:line.find("]")]
                    csi_values = [int(x) for x in raw_csi_string.split(',')]
                    
                    # Calculate 64 amplitudes
                    amplitudes = [math.sqrt(csi_values[i]**2 + csi_values[i+1]**2) for i in range(0, len(csi_values), 2)]
                    
                    # Ensure we have exactly 64 subcarriers to avoid broken data
                    if len(amplitudes) == 64:
                        # Append the label to the end of the row
                        row_data = amplitudes + [CURRENT_LABEL]
                        writer.writerow(row_data)
                        
                        packet_count += 1
                        if packet_count % 100 == 0:
                            print(f"Recorded {packet_count} packets for [{CURRENT_LABEL}]...")

                except Exception:
                    pass

except KeyboardInterrupt:
    print(f"\nRecording stopped. Saved {packet_count} rows to {FILENAME}")
    sock.close()
