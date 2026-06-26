# 🚀 Release Notes

### Changes in `configuration.yaml`:
1. **New Shell Commands Added**:
   - `cleanup_helicopter_log`: Added for managing helicopter log files.

2. **New Command Line Sensors**:
   - Added sensors for monitoring live power draw and health of various devices:
     - `RPi5 Live Power Draw`
     - `Main NVMe Health`
     - `CCTV SSD Health`

3. **Energy Tracking Enhancements**:
   - Added new sensors for tracking energy usage of additional devices:
     - `Redwan's S23 Total Energy`
     - `Redwan's S10 FE Total Energy`
     

4. **Utility Meter Updates**:
   - Added daily and monthly electricity tracking for `Predator`.

5. **MQTT Integration**:
   - Added binary sensors for room occupancy and kitchen emergency status.
   - Added sensors for kitchen environment monitoring:
     - Temperature, humidity, barometric pressure, gas concentration, and UPS rail voltage.

6. **Recorder Configuration**:
   - Excluded additional entities from being recorded:
     - `sensor.helicopter_surveillance_log_10km`

7. **Advanced Template Sensors**:
   - Added new template sensors:
     - `Helicopter Surveillance Log 10km`
     - `Tenda Uptime Formatted`
     - `Time Until Next Event Formatted`
     - `Waqt Progress Percentage`

8. **External Services**:
   - No changes in external services configuration.

---

# Home Assistant Configuration

This repository contains the `configuration.yaml` file for a Home Assistant setup. The configuration includes integrations, sensors, automations, and external services to enhance the functionality of your smart home system.

## Table of Contents
- [Default Configurations](#default-configurations)
- [Frontend Themes](#frontend-themes)
- [HTTP Configuration](#http-configuration)
- [Dashboard Controls](#dashboard-controls)
- [Shell Commands](#shell-commands)
- [Command Line Sensors](#command-line-sensors)
- [Energy Tracking](#energy-tracking)
- [MQTT Integration](#mqtt-integration)
- [Recorder Configuration](#recorder-configuration)
- [Advanced Template Sensors](#advanced-template-sensors)
- [External Services](#external-services)

---

## Default Configurations
The `default_config` integration is loaded to include the default set of Home Assistant integrations.

---

## Frontend Themes
Custom themes are loaded from the `themes` directory using:
```yaml
frontend:
  themes: !include_dir_merge_named themes
```

---

## HTTP Configuration
The HTTP component is configured to use `X-Forwarded-For` headers and includes a list of trusted proxies:
```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
    - "::1"
    - 172.17.0.2
    - 172.17.0.0/16
    - 192.168.0.0/16
    - 10.0.0.0/8
```

---

## Dashboard Controls
An `input_boolean` is defined to toggle the display of Raspberry Pi power history:
```yaml
input_boolean:
  show_pi_power_history:
    name: "Show Pi Power History"
    icon: mdi:chart-bar
```

---

## Shell Commands
Shell commands are defined for various tasks, including:
- Running backups
- Restarting services (e.g., Nextcloud, CCTV)
- Managing flight and helicopter logs
- Example:
  ```yaml
  shell_command:
    cleanup_helicopter_log: >
      tail -n 1000 /config/www/helicopter_history.csv > /config/www/tmp_heli.csv && mv /config/www/tmp_heli.csv /config/www/helicopter_history.csv
  ```

---

## Command Line Sensors
Command line sensors are used to monitor system health and performance:
- Raspberry Pi fan speed
- NVMe and SSD health
- Live power draw of Raspberry Pi
- Example:
  ```yaml
  - sensor:
      name: "RPi5 Fan Speed"
      command: "cat /config/fan_speed.txt"
      unit_of_measurement: "RPM"
      scan_interval: 15
      value_template: "{{ value | float(0) }}"
  ```

---

## Energy Tracking
Energy usage is tracked using integration sensors and utility meters:
- Devices tracked include Raspberry Pi, Predator, and mobile devices.
- Example:
  ```yaml
  sensor:
    - platform: integration
      source: sensor.rpi5_live_power_draw
      name: "RPi5 Total Energy"
      unique_id: rpi5_total_energy_tracker_unique
      unit_prefix: k
      round: 3
      method: left
  ```

---

## MQTT Integration
MQTT sensors and binary sensors are configured for real-time data monitoring:
- Room occupancy and kitchen emergency status.
- Kitchen environment metrics (temperature, humidity, gas concentration, etc.).
- Example:
  ```yaml
  mqtt:
    binary_sensor:
      - name: "CSI Room Occupancy"
        state_topic: "home/room/occupancy"
        payload_on: "ON"
        payload_off: "OFF"
        device_class: occupancy
    sensor:
      - name: "Kitchen Temperature"
        state_topic: "home/sensors/kitchen"
        value_template: "{{ value_json.temp | round(1) }}"
        unit_of_measurement: "°C"
        device_class: temperature
        state_class: measurement
  ```

---

## Recorder Configuration
The recorder is configured to purge data older than 2 days and exclude specific domains and entities:
```yaml
recorder:
  purge_keep_days: 2
  commit_interval: 30
  exclude:
    domains:
      - sun
      - weather
      - camera
      - update
    entities:
      - sensor.time
      - sensor.date
      - sensor.airspace_surveillance_log_10km
      - sensor.helicopter_surveillance_log_10km
```

---

## Advanced Template Sensors
Template sensors provide advanced functionality, including:
- Dynamic prayer times and prohibited time logic.
- Router uptime formatting.
- Power estimation for Predator device.
- Example:
  ```yaml
  template:
    - sensor:
        - name: "Waqt Progress Percentage"
          unit_of_measurement: "%"
          state: >
            {% set now = as_timestamp(now()) %}
            {% set times = [
              as_timestamp(states('sensor.islamic_prayer_times_fajr_prayer'), 0),
              as_timestamp(states('sensor.islamic_prayer_times_sunrise_time'), 0),
              as_timestamp(states('sensor.islamic_prayer_times_dhuhr_prayer'), 0),
              as_timestamp(states('sensor.islamic_prayer_times_asr_prayer'), 0),
              as_timestamp(states('sensor.islamic_prayer_times_maghrib_prayer'), 0),
              as_timestamp(states('sensor.islamic_prayer_times_isha_prayer'), 0)
            ] %}
            {% set past_times = times | select('<', now) | list %}
            {% set future_times = times | select('>', now) | list %}
            {% set start = past_times | last | default(now - 3600) %}
            {% set end = future_times | first | default(now + 3600) %}
            {% set total = end - start %}
            {% set elapsed = now - start %}
            {{ ((elapsed / total) * 100) | int }}
  ```

---

## External Services
External services include:
- Geolocation tracking (e.g., USGS Earthquake Feed).
- REST commands for managing torrents.
- Google Assistant integration for smart home control.
- Example:
  ```yaml
  rest_command:
    qbit_pause_all:
      url: "http://192.168.0.40:8082/api/v2/torrents/pause"
      method: POST
      payload: "hashes=all"
      content_type: "application/x-www-form-urlencoded"
  ```
