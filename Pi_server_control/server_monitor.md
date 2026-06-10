# Pi Server Control - `server_monitor.py`

## Overview
The `server_monitor.py` script is a Python-based monitoring tool designed for Raspberry Pi servers. It provides real-time monitoring and display of system metrics, environmental conditions, network status, and Docker container health. The script utilizes an OLED display to present the data in a user-friendly manner, making it ideal for quick status checks.

---

## Features
1. **System Monitoring**:
   - CPU usage percentage.
   - RAM usage (used/total).
   - Raspberry Pi temperature.
   - Disk usage (used/total).
   - Disk read/write speeds.

2. **Environmental Monitoring**:
   - Temperature and humidity readings from a DHT11 sensor.
   - Feels-like temperature fetched from a Home Assistant (HA) instance.

3. **Network Monitoring**:
   - Internet connection status.
   - Network interface type (WiFi/ETH) and SSID (for WiFi).
   - Ping latency to Google's public DNS (8.8.8.8).
   - Network upload and download speeds.

4. **Docker Container Health Check**:
   - Monitors the status of key Docker containers (e.g., `homeassistant`, `nextcloud`, `mosquitto`, `cloudflare`, `pihole`).
   - Alerts if any critical container is down.

5. **Date and Time Display**:
   - Current time and date in a user-friendly format.
   - Hijri (Islamic) date fetched from the Aladhan API.
   - Bangla calendar date displayed in both Bangla and English transliterations.

6. **OLED Display**:
   - Displays real-time data on a 128x64 OLED screen using the `adafruit_ssd1306` library.
   - Auto-refreshes every second.
   - Cycles through multiple pages of information every 15 seconds.

7. **Background Data Fetching**:
   - Runs a background thread to fetch and update data from sensors, APIs, and system commands.
   - Updates data every 5 seconds for real-time accuracy.

8. **Energy Efficiency**:
   - Automatically turns off the OLED display between 12:30 AM and 5:00 AM to conserve power.

---

## Requirements
### Hardware
- Raspberry Pi (any model with GPIO support).
- DHT11 Temperature and Humidity Sensor (connected to GPIO 17).
- 128x64 OLED Display (I2C interface).

### Software
- Python 3.x.
- Required Python libraries:
  - `adafruit_ssd1306`
  - `adafruit_dht`
  - `Pillow`
  - `psutil`
  - `requests`
  - `bangla`
- Home Assistant instance with API access.

---

## Installation

1. **Install Required Libraries**:
   Install the necessary Python libraries using `pip`:
   ```bash
   pip install adafruit-circuitpython-ssd1306 adafruit-circuitpython-dht pillow psutil requests bangla
   ```

2. **Enable I2C on Raspberry Pi**:
   Ensure I2C is enabled on your Raspberry Pi:
   ```bash
   sudo raspi-config
   ```
   Navigate to `Interfacing Options > I2C` and enable it.

3. **Connect Hardware**:
   - Connect the DHT11 sensor to GPIO 17.
   - Connect the OLED display to the I2C pins (SCL and SDA).

4. **Clone the Repository**:
   Clone the `Pi_server_control` repository:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

5. **Configure Home Assistant**:
   - Update the `HA_URL` and `HA_TOKEN` variables in the script with your Home Assistant instance's URL and long-lived access token.
   - Ensure the `HA_FEELS_LIKE` sensor is correctly configured in Home Assistant.

6. **Run the Script**:
   Execute the script:
   ```bash
   python3 server_monitor.py
   ```

---

## Usage

### OLED Display Pages
The OLED display cycles through the following pages every 15 seconds:
1. **System Metrics**:
   - CPU usage.
   - RAM usage.
   - Raspberry Pi temperature.

2. **Disk Usage**:
   - OS disk usage.
   - Disk read/write speeds.

3. **Network Status**:
   - Network interface type and SSID.
   - Upload and download speeds.
   - Ping latency.

4. **Environmental Data**:
   - Server room temperature (DHT11).
   - Humidity level (DHT11).
   - Feels-like temperature (from Home Assistant).

5. **Docker Health**:
   - Status of critical Docker containers.

### Footer
The footer alternates every 15 seconds between:
- Hijri (Islamic) date.
- Bangla calendar date (in Bangla and English transliterations).

---

## Configuration

### Home Assistant Integration
To enable Home Assistant integration:
1. Obtain a long-lived access token from your Home Assistant instance.
2. Replace the `HA_URL` and `HA_TOKEN` variables in the script with your instance's URL and token.
3. Ensure the `HA_FEELS_LIKE` sensor is configured in Home Assistant.

### Docker Monitoring
The script monitors the following Docker containers by default:
- `homeassistant`
- `nextcloud`
- `mosquitto`
- `cloudflare`
- `pihole`

To modify the list of monitored containers, update the `background_tasks` function in the script.

---

## Notes
1. **Error Handling**:
   - The script includes error handling for API requests, sensor readings, and system commands. If an error occurs, the corresponding data will display as `--` or an appropriate fallback message.

2. **Energy Efficiency**:
   - The OLED display turns off between 12:30 AM and 5:00 AM to conserve power.

3. **Bangla Date**:
   - The Bangla date is displayed using the `bangla` library. If the library fails to fetch the date, it will display `--`.

4. **Hijri Date**:
   - The Hijri date is fetched from the Aladhan API. If the API is offline, the script will display `API Offline`.

---

## Troubleshooting

### Common Issues
1. **OLED Display Not Working**:
   - Ensure the I2C interface is enabled on your Raspberry Pi.
   - Verify the OLED display is connected to the correct pins.

2. **DHT11 Sensor Not Responding**:
   - Check the wiring of the DHT11 sensor.
   - Ensure the sensor is connected to GPIO 17.

3. **Home Assistant API Errors**:
   - Verify the `HA_URL` and `HA_TOKEN` values in the script.
   - Ensure the Home Assistant instance is reachable from the Raspberry Pi.

4. **Docker Monitoring Issues**:
   - Ensure the Docker daemon is running on the Raspberry Pi.
   - Verify the container names match those in the script.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
- [Adafruit CircuitPython Libraries](https://github.com/adafruit)
- [Bangla Python Library](https://github.com/torifat/bangla)
- [Aladhan API](https://aladhan.com/)
- [Pillow Library](https://pillow.readthedocs.io/)