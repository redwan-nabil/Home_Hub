# 🚀 Release Notes

The following updates have been made to the `configuration.yaml` file for the Home Assistant setup:

### New Features
1. **Input Boolean for Dashboard Control**:
   - Added `input_boolean.show_pi_power_history` to toggle the display of Raspberry Pi power history on the dashboard.

2. **New Shell Commands**:
   - Added `cleanup_flight_log` and `cleanup_helicopter_log` commands to manage log files by keeping only the latest 1000 entries.
   - Updated `export_flight` shell command to sanitize single quotes in the log data.

3. **New Command Line Sensors**:
   - `RPi5 Live Power Draw`: Monitors real-time power consumption of the Raspberry Pi 5.
   - `RPi5 Fan Speed`: Reads fan speed from a local file.
   - `Main NVMe Health`: Monitors the health of the main NVMe drive.
   - `CCTV SSD Health`: Monitors the health of the CCTV SSD.
   
4. **Energy Tracking Engine**:
   - Added `sensor.rpi5_total_energy` to calculate total energy consumption in kWh.
   - Added `utility_meter` sensors for daily and monthly electricity usage tracking (`rpi5_daily_electricity` and `rpi5_monthly_electricity`).

5. **Enhanced MQTT Integration**:
   - Added new MQTT binary sensors for `CSI Room Occupancy` and `Kitchen Emergency Status`.
   - Added MQTT sensors for `Kitchen Temperature`, `Kitchen Humidity`, `Kitchen Barometric Pressure`, `Kitchen Gas Concentration`, and `Kitchen UPS Rail Voltage`.

6. **Recorder Enhancements**:
   - Excluded additional entities (`sensor.airspace_surveillance_log_10km`, `sensor.helicopter_surveillance_log_10km`) to optimize database size.

7. **Template Sensors**:
   - Added new template sensors for Islamic prayer times, including `Next Sahri Ends`, `Next Iftar`, `Active Waqt Details`, `Time Until Next Event Formatted`, and `Waqt Progress Percentage`.
   - Added `Tenda Uptime Formatted` sensor to display router uptime in a human-readable format.

8. **Zone and Geo-location**:
   - Added a new zone for a "10km Airspace Dome" with a radius of 10km.
   - Configured a USGS Earthquake feed for earthquakes with a magnitude of 4.5+ within a 1500km radius.

9. **Google Assistant Integration**:
   - Added Google Assistant integration with project ID `redwans-smart-home-hub` and exposed domains for `switch`, `light`, `script`, and `input_boolean`.

---

# Home Assistant Configuration

This repository contains the configuration for a Home Assistant setup. The configuration is designed to provide automation, monitoring, and control capabilities for a smart home environment. Below is a detailed explanation of the configuration.

---

## Table of Contents
1. [Default Config](#default-config)
2. [Frontend Themes](#frontend-themes)
3. [HTTP Configuration](#http-configuration)
4. [Dashboard Controls](#dashboard-controls)
5. [Shell Commands](#shell-commands)
6. [Command Line Sensors](#command-line-sensors)
7. [Energy Tracking Engine](#energy-tracking-engine)
8. [MQTT Integration](#mqtt-integration)
9. [Recorder Configuration](#recorder-configuration)
10. [Template Sensors](#template-sensors)
11. [Zones and Geo-location](#zones-and-geo-location)
12. [Google Assistant Integration](#google-assistant-integration)

---

## Default Config
The `default_config` integration is included to load the default set of Home Assistant integrations. Do not remove this section unless you intend to manually configure all integrations.

---

## Frontend Themes
The `frontend` integration is configured to load custom themes from the `themes` directory. Add your theme files to this folder to customize the appearance of your Home Assistant dashboard.

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

---

## HTTP Configuration
The HTTP integration is configured to use `x_forwarded_for` and includes a list of trusted proxies. This is useful for setups behind reverse proxies like NGINX.

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
An `input_boolean` entity has been added to control the visibility of the Raspberry Pi power history on the dashboard.

```yaml
input_boolean:
  show_pi_power_history:
    name: "Show Pi Power History"
    icon: mdi:chart-bar
```

---

## Shell Commands
Several shell commands are configured for remote operations and log management:

- `run_ha_backup`: Triggers a Home Assistant backup.
- `restart_nextcloud`: Restarts the Nextcloud service.
- `restart_cctv`: Restarts the CCTV service.
- `export_flight`: Exports flight data to a CSV file.
- `cleanup_flight_log`: Keeps only the latest 1000 lines in the flight log.
- `cleanup_helicopter_log`: Keeps only the latest 1000 lines in the helicopter log.

---

## Command Line Sensors
Command line sensors are configured to monitor system health and performance:

- **RPi5 Fan Speed**: Monitors the fan speed of the Raspberry Pi 5.
- **Main NVMe Health**: Displays the health of the main NVMe drive.
- **CCTV SSD Health**: Displays the health of the CCTV SSD.
- **RPi5 Live Power Draw**: Monitors the real-time power consumption of the Raspberry Pi 5.

---

## Energy Tracking Engine
The energy tracking engine calculates the total energy consumption of the Raspberry Pi 5 and tracks daily and monthly electricity usage.

- `sensor.rpi5_total_energy`: Tracks total energy consumption in kWh.
- `utility_meter.rpi5_daily_electricity`: Tracks daily electricity usage.
- `utility_meter.rpi5_monthly_electricity`: Tracks monthly electricity usage.

---

## MQTT Integration
MQTT sensors and binary sensors are configured for various smart home devices:

### Binary Sensors
- **CSI Room Occupancy**: Detects occupancy in the CSI room.
- **Kitchen Emergency Status**: Monitors the kitchen for smoke or fire.

### Sensors
- **Kitchen Temperature**: Reports the temperature in the kitchen.
- **Kitchen Humidity**: Reports the humidity in the kitchen.
- **Kitchen Barometric Pressure**: Reports the barometric pressure in the kitchen.
- **Kitchen Gas Concentration**: Reports gas concentration in the kitchen.
- **Kitchen UPS Rail Voltage**: Reports the voltage of the kitchen UPS rail.

---

## Recorder Configuration
The recorder integration is configured to retain data for 2 days and exclude certain domains and entities to optimize database size.

---

## Template Sensors
Custom template sensors are configured for advanced functionality:

- **Islamic Prayer Times**: Displays the next Sahri and Iftar times.
- **Dynamic Waqt Details**: Provides details about the current Islamic prayer time.
- **Time Until Next Event Formatted**: Displays a human-readable countdown to the next prayer or event.
- **Waqt Progress Percentage**: Displays the progress of the current prayer time as a percentage.
- **Tenda Uptime Formatted**: Displays the uptime of the Tenda router in a human-readable format.

---

## Zones and Geo-location
- **10km Airspace Dome**: A zone with a 10km radius for airspace monitoring.
- **USGS Earthquake Feed**: Monitors earthquakes with a magnitude of 4.5+ within a 1500km radius.

---

## Google Assistant Integration
Google Assistant integration is configured with the following settings:

- **Project ID**: `redwans-smart-home-hub`
- **Service Account**: Included via `SERVICE_ACCOUNT.json`.
- **Exposed Domains**: `switch`, `light`, `script`, and `input_boolean`.

---

This configuration enhances the Home Assistant setup with advanced automation, monitoring, and control capabilities. For further customization, refer to the [Home Assistant Documentation](https://www.home-assistant.io/docs/).