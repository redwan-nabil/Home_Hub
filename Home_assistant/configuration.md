# 🚀 Release Notes

### Updates in `configuration.yaml`
1. **New Input Boolean Added**:
   - `earthquake_alarm_armed`: Allows toggling the earthquake alarm system with an icon `mdi:vibrate`.

2. **New Command Line Sensors**:
   - Added sensors for monitoring hardware and power usage:
     - `RPi5 Fan Speed`
     - `Main NVMe Health`
     - `CCTV SSD Health`
     - `RPi5 Live Power Draw`

3. **Energy Tracking Enhancements**:
   - Added new `utility_meter` sensors for daily and monthly electricity usage tracking:
     - `Predator Daily Electricity Usage`
     - `Predator Monthly Electricity Usage`

4. **New MQTT Sensors**:
   - Added binary sensors for:
     - `CSI Room Occupancy`
     - `Kitchen Emergency Status`
   - Added sensors for kitchen environment monitoring:
     - `Kitchen Temperature`
     - `Kitchen Humidity`
     - `Kitchen Barometric Pressure`
     - `Kitchen Gas Concentration`
     - `Kitchen UPS Rail Voltage`

5. **Advanced Template Sensors**:
   - Added sensors for:
     - Islamic prayer times and fasting schedules (`Next Sahri Ends`, `Next Iftar`, `Active Waqt Details`, etc.).
     - Dynamic Waqt progress percentage (`Waqt Progress Percentage`).
     - Router uptime formatter (`Tenda Uptime Formatted`).
     - Predator live power estimation (`Predator Live Power Draw`).

6. **External Services**:
   - Added a new `geo_location` platform for USGS earthquake feed with a 1500km radius and minimum magnitude of 4.5.

---

# Home Assistant Configuration

This repository contains the configuration files for a Home Assistant instance. The setup is designed to manage and monitor a smart home environment, including automation, energy tracking, MQTT sensors, and external integrations.

## Features

### Default Configuration
The `default_config` integration is included to load the default set of Home Assistant integrations.

### Frontend Themes
Custom themes are loaded from the `themes` directory using the `!include_dir_merge_named` directive.

### Automation, Scripts, and Scenes
- Automations: Configured in `automations.yaml`.
- Scripts: Configured in `scripts.yaml`.
- Scenes: Configured in `scenes.yaml`.

### HTTP Configuration
- `use_x_forwarded_for`: Enabled for reverse proxy support.
- `trusted_proxies`: Configured for specific IP ranges to allow trusted proxy connections.

### Input Booleans
Custom toggles for dashboard controls:
- `show_pi_power_history`: Toggle to display Raspberry Pi power history.
- `earthquake_alarm_armed`: Toggle to arm/disarm the earthquake alarm system.

### Shell Commands
Predefined shell commands for system management:
- `run_ha_backup`: Executes a Home Assistant backup via SSH.
- `restart_nextcloud`: Restarts the Nextcloud service.
- `restart_cctv`: Restarts the CCTV system.
- `export_flight`: Exports flight history to a CSV file.
- `cleanup_flight_log`: Trims flight history logs to the last 1000 entries.
- `cleanup_helicopter_log`: Trims helicopter logs to the last 1000 entries.

### Command Line Sensors
Sensors for monitoring hardware and system health:
- `RPi5 Fan Speed`: Monitors the fan speed of Raspberry Pi 5.
- `Main NVMe Health`: Tracks the health of the main NVMe drive.
- `CCTV SSD Health`: Tracks the health of the CCTV SSD.
- `RPi5 Live Power Draw`: Monitors the live power draw of Raspberry Pi 5.

### Energy Tracking
Energy usage is tracked using the `integration` platform:
- `RPi5 Total Energy`
- `Predator Total Energy Accumulated`
- `Redwan's S23 Total Energy`
- `Redwan's S10 FE Total Energy`
- `Ahlia's Note 8 Total Energy`

Utility meters are configured for daily and monthly electricity usage:
- `RPi5 Daily Electricity`
- `RPi5 Monthly Electricity`
- `Predator Daily Electricity Usage`
- `Predator Monthly Electricity Usage`

### MQTT Sensors
Integration with MQTT for real-time monitoring:
- Binary sensors:
  - `CSI Room Occupancy`
  - `Kitchen Emergency Status`
- Environmental sensors for the kitchen:
  - `Kitchen Temperature`
  - `Kitchen Humidity`
  - `Kitchen Barometric Pressure`
  - `Kitchen Gas Concentration`
  - `Kitchen UPS Rail Voltage`

### Recorder
- Data retention is limited to 2 days to optimize database performance.
- Excludes specific domains and entities from being recorded (e.g., `sun`, `weather`, `camera`, etc.).

### Advanced Template Sensors
Custom template sensors for advanced logic:
- Islamic prayer times and fasting schedules:
  - `Next Sahri Ends`
  - `Next Iftar`
  - `Active Waqt Details`
  - `Time Until Next Event Formatted`
  - `Waqt Progress Percentage`
- Router uptime formatter: `Tenda Uptime Formatted`.
- Predator live power estimation: `Predator Live Power Draw`.

### External Services
- **Zone**: Defined a 10km airspace dome for geofencing.
- **USGS Earthquake Feed**: Monitors earthquakes within a 1500km radius and a minimum magnitude of 4.5.
- **REST Commands**:
  - `qbit_pause_all`: Pauses all torrents in qBittorrent.
  - `qbit_resume_all`: Resumes all torrents in qBittorrent.
- **Google Assistant Integration**:
  - Configured for project `redwans-smart-home-hub`.
  - Exposed domains: `switch`, `light`, `script`, `input_boolean`.

---

## File Structure
```
configuration.yaml
automations.yaml
scripts.yaml
scenes.yaml
themes/
  └── <theme_files>
config/
  └── www/
      ├── flight_history.csv
      ├── helicopter_history.csv
      ├── fan_speed.txt
      ├── nvme_health.txt
      ├── sda_health.txt
      └── power_draw.txt
ssh_keys/
  └── id_rsa
SERVICE_ACCOUNT.json
```

---

## Installation
1. Clone this repository to your Home Assistant configuration directory.
2. Ensure all required files (e.g., `SERVICE_ACCOUNT.json`, `ssh_keys/id_rsa`) are correctly placed.
3. Restart Home Assistant to apply the changes.

---

## Notes
- Ensure the MQTT broker is properly configured and running.
- Update the IP addresses and credentials for external services (e.g., qBittorrent, SSH) as needed.
- Verify the paths for external files (e.g., `fan_speed.txt`, `nvme_health.txt`) are correct and accessible.

---

## Troubleshooting
- **Database Size**: If the database grows too large, adjust the `purge_keep_days` setting in the `recorder` section.
- **Sensor Errors**: Ensure all external files and MQTT topics are correctly configured and accessible.
- **Google Assistant Issues**: Verify the `SERVICE_ACCOUNT.json` file and project ID are correct.

For additional support, refer to the [Home Assistant Documentation](https://www.home-assistant.io/docs/).