# Pi Server Control - `server_monitor.py`

## 🚀 Release Notes

### Updates in the New Version:
1. **Enhanced Security Features**:
   - Added a high-speed security watchdog thread to monitor environmental conditions and seismic activity.
   - Integrated MPU6050 accelerometer for earthquake detection and magnitude calculation.
   - Implemented a full alarm system with support for:
     - Telegram alerts.
     - Gmail notifications.
     - SMS-based emergency SOS alerts.
     - Buzzer triggering for local alarms.

2. **Hardware Integration**:
   - Replaced DHT11 sensor with BME280 sensor for more accurate temperature, humidity, and pressure readings.
   - Integrated MPU6050 accelerometer for real-time motion and vibration detection.

3. **Improved Networking and Docker Monitoring**:
   - Enhanced network interface and internet connectivity detection.
   - Improved Docker container health monitoring with detailed status updates.

4. **Multi-Language Support**:
   - Added support for Bangla date conversion using the `bangla` library (if available).
   - Added fallback messages for missing Bangla library.

5. **Hijri Date Calculation**:
   - Improved Hijri date calculation using the Aladhan API.
   - Added support for automatic date rollover after Maghrib prayer.

6. **Data Synchronization with Home Assistant**:
   - Added real-time updates for environmental and seismic data to Home Assistant sensors.

7. **OLED Display Enhancements**:
   - Redesigned OLED display layout with dynamic page flipping.
   - Added new pages for earthquake alerts and environmental data.
   - Improved text alignment and formatting for better readability.

8. **Code Refactoring**:
   - Modularized the code into logical sections for better readability and maintainability.
   - Added error handling for external API calls and hardware interactions.

---

## README

### Overview
`server_monitor.py` is a Python-based monitoring and alerting script designed for Raspberry Pi servers. It integrates with various hardware sensors and APIs to monitor environmental conditions, seismic activity, and server health. The script also provides real-time data visualization on an OLED display and supports multiple alerting mechanisms, including email, Telegram, and SMS.

---

### Features
1. **Environmental Monitoring**:
   - Temperature, humidity, and pressure monitoring using the BME280 sensor.
   - Real-time data synchronization with Home Assistant.

2. **Seismic Activity Detection**:
   - Real-time earthquake detection using the MPU6050 accelerometer.
   - Earthquake magnitude calculation using the Richter scale.
   - Configurable earthquake alarm system with support for:
     - Telegram alerts.
     - Gmail notifications.
     - SMS-based emergency SOS alerts.
     - Local buzzer activation.

3. **Server Health Monitoring**:
   - CPU, RAM, and disk usage monitoring.
   - Network interface and internet connectivity status.
   - Docker container health checks.

4. **Multi-Language Support**:
   - Bangla date conversion (requires `bangla` library).
   - Hijri date calculation using the Aladhan API.

5. **OLED Display**:
   - Real-time data visualization on a 128x64 OLED display.
   - Dynamic page flipping with multiple views:
     - System performance (CPU, RAM, temperature).
     - Disk usage and I/O statistics.
     - Network status and internet connectivity.
     - Environmental data (temperature, humidity, pressure).
     - Earthquake alerts and seismic status.
     - Docker container health.

6. **Background Data Synchronization**:
   - Periodic updates from external APIs (e.g., Aladhan for Hijri dates).
   - Real-time data updates to Home Assistant sensors.

---

### Requirements
- **Hardware**:
  - Raspberry Pi with I2C and SPI interfaces enabled.
  - BME280 sensor for temperature, humidity, and pressure monitoring.
  - MPU6050 accelerometer for seismic activity detection.
  - SSD1306 OLED display (128x64 resolution).
  - GSM module for SMS-based emergency alerts (optional).

- **Python Libraries**:
  - `psutil`
  - `bangla` (optional for Bangla date support)
  - `requests`
  - `smtplib`
  - `Pillow`
  - `adafruit-circuitpython-bme280`
  - `adafruit-circuitpython-ssd1306`
  - `mpu6050`

---

### Installation
1. **Install Required Libraries**:
   ```bash
   pip3 install psutil requests Pillow adafruit-circuitpython-bme280 adafruit-circuitpython-ssd1306 mpu6050
   ```

2. **Enable I2C and SPI on Raspberry Pi**:
   - Run `sudo raspi-config`.
   - Navigate to `Interfacing Options` and enable both I2C and SPI.

3. **Install Bangla Library (Optional)**:
   ```bash
   pip3 install bangla
   ```

4. **Configure Home Assistant**:
   - Update the `HA_URL`, `HA_TOKEN`, and `HA_FEELS_LIKE` variables in the script with your Home Assistant details.

5. **Configure Alerting Systems**:
   - Update the following variables in the script:
     - `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for Telegram alerts.
     - `GMAIL_USER`, `GMAIL_APP_PASSWORD`, and `ALERT_RECIPIENTS` for Gmail notifications.
     - `EMERGENCY_NUMBERS` for SMS-based emergency alerts.

---

### Usage
1. **Run the Script**:
   ```bash
   python3 server_monitor.py
   ```

2. **OLED Display Pages**:
   - The OLED display cycles through the following pages every 15 seconds:
     1. System performance (CPU, RAM, temperature).
     2. Disk usage and I/O statistics.
     3. Network status and internet connectivity.
     4. Environmental data (temperature, humidity, pressure).
     5. Earthquake alerts and seismic status.
     6. Docker container health.

3. **Alerts**:
   - The script automatically triggers alerts for critical events, such as:
     - Fire detection (temperature spike).
     - Earthquake detection (magnitude ≥ 4.5).
     - Docker container failures.

---

### Configuration
- **Adjusting Thresholds**:
  - Fire detection temperature threshold: `if (current_temp - baseline_temp) > 5.0`.
  - Earthquake detection magnitude threshold: `if richter >= 4.5`.

- **Customizing Pages**:
  - Modify the `lines` array in the OLED display loop to customize the displayed information.

- **Adding New Alerts**:
  - Use the `trigger_full_alarm` function to add new alerting mechanisms.

---

### Troubleshooting
1. **Bangla Library Missing**:
   - If the Bangla library is not installed, the script will display "Bangla Lib Missing" for the Bangla date.

2. **API Errors**:
   - If the Aladhan API is unavailable, the Hijri date will display "API Offline".

3. **Hardware Issues**:
   - Ensure all hardware components are properly connected and configured.
   - Check the I2C and SPI connections for the OLED display and sensors.

4. **Permission Errors**:
   - Ensure the script is run with appropriate permissions to access hardware interfaces and network resources.

---

### License
This project is licensed under the MIT License.