# CSI-Project: `bridge.py`

## Overview
The `bridge.py` script is a dual-threshold radar system designed to detect room occupancy using Channel State Information (CSI) data from WiFi signals. It processes incoming UDP packets containing CSI data, calculates amplitude variations, and determines whether a room is occupied or empty. The occupancy status is then published to an MQTT broker for integration with smart home systems.

## Features
- **Dual-Threshold Radar (Hysteresis):** Implements a two-level threshold system for detecting human presence and maintaining occupancy status.
- **Baseline Calibration:** Automatically calibrates the baseline amplitude for an empty room to adapt to environmental noise.
- **MQTT Integration:** Publishes occupancy status (`ON` for occupied, `OFF` for empty) to an MQTT broker for external use.
- **Moving Average Buffer:** Smooths out amplitude variations using a sliding window to improve detection accuracy.
- **Automatic Noise Adaptation:** Continuously adjusts the baseline to account for background noise (e.g., air conditioning).

## Configuration
The script includes several configurable parameters:

### Network Settings
- `UDP_IP`: IP address to listen for incoming UDP packets. Default: `0.0.0.0` (all interfaces).
- `UDP_PORT`: Port number to bind for UDP communication. Default: `5500`.
- `MQTT_BROKER`: IP address of the MQTT broker. Default: `192.168.0.40`.
- `MQTT_TOPIC`: MQTT topic to publish occupancy status. Default: `home/room/occupancy`.

### Radar Thresholds
- `TRIGGER_THRESHOLD`: Variance threshold to detect initial human entry. Default: `0.25`.
- `MAINTAIN_THRESHOLD`: Variance threshold to maintain occupancy status. Default: `0.08`.
- `HOLD_TIME`: Time (in seconds) to keep the room "occupied" after the last detected movement. Default: `30`.
- `WINDOW_SIZE`: Size of the moving average buffer for amplitude smoothing. Default: `5`.

## Dependencies
The script requires the following Python libraries:
- `socket`: For UDP communication.
- `math`: For amplitude calculations.
- `time`: For time-based operations.
- `collections`: For managing the moving average buffer.
- `paho-mqtt`: For MQTT communication.

Install dependencies using:
```bash
pip install paho-mqtt
```

## How It Works
1. **UDP Listener:** The script listens for incoming UDP packets containing CSI data.
2. **Amplitude Calculation:** Extracts CSI values, calculates subcarrier amplitudes, and computes the average amplitude for each packet.
3. **Baseline Calibration:** Establishes a baseline amplitude for an empty room during initialization.
4. **Variance Analysis:** Compares smoothed amplitude values against the baseline to detect occupancy changes.
5. **Occupancy Detection:**
   - If the room is empty, a large variance triggers the "occupied" state.
   - If the room is occupied, small ripples in variance reset the occupancy timer.
6. **MQTT Publishing:** Publishes `ON` or `OFF` messages to the configured MQTT topic based on occupancy status.

## Usage
1. **Run the Script:**
   Execute the script using Python:
   ```bash
   python bridge.py
   ```
2. **Monitor Output:**
   - The script logs its status to the console, including baseline calibration, variance values, and occupancy changes.
   - Example output:
     ```
     Connected to MQTT Broker at 192.168.0.40
     Dual-Threshold Radar Online. Trigger: 0.25 | Maintain: 0.08
     Listening on UDP port 5500...
     --- Initial Baseline Calibrated ---
     Scanning empty room... Variance: 0.012
     [>>>] HUMAN ENTERED! (Spike: 0.300)
     Holding ON... Variance: 0.100 | Timer: 29.5s left
     [<<<] ROOM EMPTY. (No ripples > 0.08 for 30s)
     ```

3. **MQTT Integration:**
   - Subscribe to the configured MQTT topic (`home/room/occupancy`) using an MQTT client to receive occupancy updates.
   - Example messages:
     - `ON`: Room is occupied.
     - `OFF`: Room is empty.

## Error Handling
- **Corrupted Packets:** The script ignores malformed or corrupted CSI data packets.
- **MQTT Connection Failure:** Logs an error message if the MQTT broker connection fails.

## Shutdown
To safely terminate the script:
- Press `Ctrl+C` to stop the radar.
- The script will close the MQTT connection and UDP socket before exiting.

## Future Improvements
- Add support for multiple rooms by handling multiple UDP ports and MQTT topics.
- Implement advanced machine learning models for more accurate occupancy detection.
- Add support for encrypted MQTT communication (TLS).
- Provide a graphical user interface (GUI) for configuration and monitoring.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Developed by the CSI-Project team.