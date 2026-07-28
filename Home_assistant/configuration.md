# 🚀 Release Notes

### Changes in `configuration.yaml`:
1. **Recorder Configuration Update**:
   - `commit_interval` increased from `30` to `60` seconds for improved performance.
   
2. **New Features Added**:
   - **Energy Tracking Enhancements**:
     - Added new `utility_meter` entries for `Predator Daily Electricity Usage` and `Predator Monthly Electricity Usage`.
   - **Advanced Template Sensors**:
     - Added `Waqt Progress Percentage`, `Time Until Next Event Formatted`, and `Active Waqt Details` for dynamic Islamic prayer time tracking.
     - Introduced `Tenda Uptime Formatted` for router uptime in a human-readable format.
     - Added `Predator Live Power Draw` estimation logic.
   - **External Services**:
     - Enabled `google_assistant.report_state` for real-time state reporting.
     - Added granular `entity_config` for Google Assistant integration, exposing specific scripts, toggles, and environmental sensors.

---

# Home Assistant Configuration

This repository contains the configuration for a Home Assistant instance. Below is a detailed breakdown of the configuration and its components.

---

## Table of Contents

1. [Default Configuration](#default-configuration)
2. [Frontend Themes](#frontend-themes)
3. [HTTP Configuration](#http-configuration)
4. [Dashboard Controls](#dashboard-controls)
5. [Shell Commands](#shell-commands)
6. [Command Line Sensors](#command-line-sensors)
7. [Energy Tracking Engine](#energy-tracking-engine)
8. [Consolidated MQTT Engine](#consolidated-mqtt-engine)
9. [System Recorder & Database](#system-recorder--database)
10. [Advanced Template Sensors](#advanced-template-sensors)
11. [External Services](#external-services)

---

## Default Configuration

The `default_config` integration is included to load the default set of Home Assistant integrations. It is recommended not to remove this section.

---

## Frontend Themes

The `frontend` section loads custom themes from the `themes` directory using the `!include_dir_merge_named` directive.

---

## HTTP Configuration

The `http` section is configured to:
- Use `X-Forwarded-For` headers for reverse proxy setups.
- Define a list of trusted proxies, including local and private IP ranges.

---

## Dashboard Controls

### Input Booleans
- **`show_pi_power_history`**: Toggle to display Raspberry Pi power history.
- **`earthquake_alarm_armed`**: Toggle to arm/disarm the earthquake alarm system.

---

## Shell Commands

Custom shell commands for remote operations:
- **`run_ha_backup`**: Initiates a Home Assistant backup via SSH.
- **`restart_nextcloud`**: Restarts the Nextcloud server.
- **`restart_cctv`**: Restarts the CCTV system.
- **`export_flight`**: Appends flight log data to a CSV file.
- **`cleanup_flight_log`**: Trims the flight log to the last 1000 entries.
- **`cleanup_helicopter_log`**: Trims the helicopter log to the last 1000 entries.

---

## Command Line Sensors

### Sensors:
- **`RPi5 Fan Speed`**: Monitors the fan speed of the Raspberry Pi 5.
- **`Main NVMe Health`**: Reports the health of the main NVMe drive.
- **`CCTV SSD Health`**: Reports the health of the CCTV SSD.
- **`RPi5 Live Power Draw`**: Tracks the live power consumption of the Raspberry Pi 5.

---

## Energy Tracking Engine

### Sensors:
- **`RPi5 Total Energy`**: Tracks the total energy consumption of the Raspberry Pi 5.
- **`Predator Total Energy Accumulated`**: Tracks the total energy usage of the Predator system.
- **`Redwan's S23 Total Energy`**: Tracks energy usage for Redwan's S23 device.
- **`Redwan's S10 FE Total Energy`**: Tracks energy usage for Redwan's S10 FE device.
- **`Ahlia's Note 8 Total Energy`**: Tracks energy usage for Ahlia's Note 8 device.

### Utility Meters:
- **`RPi5 Daily/Monthly Electricity`**: Tracks daily and monthly electricity usage for the Raspberry Pi 5.
- **`Predator Daily/Monthly Electricity Usage`**: Tracks daily and monthly electricity usage for the Predator system.

---

## Consolidated MQTT Engine

### Binary Sensors:
- **`CSI Room Occupancy`**: Detects room occupancy.
- **`Kitchen Emergency Status`**: Monitors kitchen smoke alarm status.

### Sensors:
- **`Kitchen Temperature`**: Reports the temperature in the kitchen.
- **`Kitchen Humidity`**: Reports the humidity in the kitchen.
- **`Kitchen Barometric Pressure`**: Reports the barometric pressure in the kitchen.
- **`Kitchen Gas Concentration`**: Monitors gas concentration in the kitchen.
- **`Kitchen UPS Rail Voltage`**: Tracks the UPS rail voltage in the kitchen.

---

## System Recorder & Database

### Configuration:
- **`purge_keep_days`**: Retains data for 2 days.
- **`commit_interval`**: Commits data every 60 seconds.
- **Exclusions**:
  - Domains: `sun`, `weather`, `camera`, `update`.
  - Entities: `sensor.time`, `sensor.date`, and specific surveillance logs.

---

## Advanced Template Sensors

### Features:
- **Dynamic Islamic Prayer Times**:
  - `Next Sahri Ends`, `Next Iftar`, and `Active Waqt Details`.
  - Includes prohibited times for sunrise, zawal, and sunset.
- **Human-Readable Countdown**:
  - `Time Until Next Event Formatted` displays time until the next prayer/event.
- **Progress Gauge**:
  - `Waqt Progress Percentage` shows progress for the current prayer time.
- **Router Uptime**:
  - `Tenda Uptime Formatted` provides a human-readable router uptime.
- **Predator Power Estimation**:
  - `Predator Live Power Draw` estimates power consumption based on CPU and GPU load.

---

## External Services

### Zone:
- **`10km Airspace Dome`**: Defines a geofence with a 10km radius for airspace monitoring.

### Geo-location:
- **USGS Earthquake Feed**: Tracks earthquakes with a magnitude of 4.5+ within a 1500km radius.

### REST Commands:
- **`qbit_pause_all`**: Pauses all torrents in qBittorrent.
- **`qbit_resume_all`**: Resumes all torrents in qBittorrent.

### Google Assistant:
- **Project ID**: `redwans-smart-home-hub`.
- **State Reporting**: Enabled for real-time updates.
- **Exposed Entities**:
  - Scripts: `restart_nextcloud_server`, `arm_earthquake_system`.
  - Toggles: `show_pi_power_history`.
  - Sensors: `kitchen_temperature`, `kitchen_humidity`.

--- 

## Notes

- Ensure all external dependencies (e.g., `SERVICE_ACCOUNT.json`, SSH keys) are correctly configured.
- Validate the configuration using Home Assistant's built-in tools before deployment.