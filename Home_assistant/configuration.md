# 🚀 Release Notes

### Changes in `configuration.yaml`
The following updates and additions have been made to the `configuration.yaml` file:

1. **Shell Commands**:
   - Updated the `export_flight` shell command to use a more secure and robust syntax for handling single quotes in `log_data`.

2. **Command Line Sensors**:
   - No changes were made to the existing command line sensors.

3. **Energy Tracking Engine**:
   - No changes were made to the energy tracking sensors or utility meters.

4. **MQTT Sensors**:
   - No changes were made to the MQTT configuration.

5. **Recorder**:
   - No changes were made to the recorder configuration.

6. **Template Sensors**:
   - Updated the `Tenda Uptime Formatted` template sensor to include a fallback mechanism for handling unavailable, unknown, or invalid uptime values. This ensures the sensor displays "Offline" when the uptime data is not available or invalid.

7. **External Services**:
   - No changes were made to the external services configuration.

---

# Home Assistant Configuration

This repository contains the configuration for a Home Assistant instance. The configuration is designed to provide a robust and feature-rich smart home experience, including automation, energy tracking, MQTT integration, advanced template sensors, and external service integrations.

## Features

### Default Configuration
The `default_config` integration is included to load the default set of integrations provided by Home Assistant.

### Frontend Themes
Custom themes are loaded from the `themes` directory using the `!include_dir_merge_named` directive.

### Automation, Scripts, and Scenes
Automations, scripts, and scenes are included from their respective YAML files:
- `automations.yaml`
- `scripts.yaml`
- `scenes.yaml`

### HTTP Configuration
- **`use_x_forwarded_for`**: Enabled to allow the use of the `X-Forwarded-For` header.
- **`trusted_proxies`**: Configured to include local and private IP ranges for trusted proxies.

### Home Assistant Configuration
- **`allowlist_external_dirs`**: Allows access to the `/config/www` directory for external files.

### Dashboard Controls
- **`input_boolean.show_pi_power_history`**: A toggle to show or hide Raspberry Pi power history on the dashboard.

### Shell Commands
- Various shell commands are defined for remote operations, including:
  - Running Home Assistant backups.
  - Restarting Nextcloud and CCTV services.
  - Exporting and cleaning flight and helicopter logs.

### Command Line Sensors
- Sensors to monitor hardware and system metrics:
  - Raspberry Pi 5 fan speed.
  - Main NVMe health.
  - CCTV SSD health.
  - Raspberry Pi 5 live power draw.

### Energy Tracking Engine
- **Integration Sensors**: Tracks total energy consumption for various devices.
- **Utility Meters**: Provides daily and monthly electricity usage for Raspberry Pi 5 and Predator devices.

### MQTT Integration
- **Binary Sensors**:
  - CSI room occupancy.
  - Kitchen emergency status.
- **Sensors**:
  - Kitchen temperature, humidity, barometric pressure, gas concentration, and UPS rail voltage.

### System Recorder & Database
- Configured to retain data for 2 days.
- Excludes specific domains and entities to optimize database size.

### Advanced Template Sensors
- **Fasting Times**:
  - `Next Sahri Ends` and `Next Iftar` sensors for Islamic prayer times.
- **Dynamic Waqt & Prohibited Time Logic**:
  - `Active Waqt Details` sensor to display the current Islamic prayer time or prohibited time.
- **Human-Readable Countdown**:
  - `Time Until Next Event Formatted` sensor for countdown to the next prayer or event.
- **Gauge Percentage**:
  - `Waqt Progress Percentage` sensor to display the progress of the current prayer time as a percentage.
- **Router Uptime Formatter**:
  - `Tenda Uptime Formatted` sensor with improved error handling for unavailable or invalid uptime data.
- **Predator Live Power Estimation**:
  - `Predator Live Power Draw` sensor to estimate power consumption based on CPU and GPU load.

### External Services
- **Zone**:
  - Defined a 10km airspace dome with specific latitude and longitude.
- **Geo-location**:
  - Configured to track earthquakes with a magnitude of 4.5 or higher within a 1500km radius.
- **REST Commands**:
  - Commands to pause and resume all torrents on a qBittorrent instance.
- **Google Assistant Integration**:
  - Configured for integration with Google Assistant, exposing specific domains.

---

## Installation

1. Clone this repository into your Home Assistant configuration directory.
2. Ensure all required directories (`themes`, `www`, etc.) exist and are populated as needed.
3. Update the `SERVICE_ACCOUNT.json` file for Google Assistant integration.
4. Restart your Home Assistant instance to apply the changes.

---

## Notes

- Ensure that the `ssh_keys` directory contains the necessary SSH keys for the shell commands to function.
- Verify that the IP addresses listed under `trusted_proxies` in the `http` section match your network configuration.
- Update the latitude and longitude values in the `zone` and `geo_location` sections to match your location.
- The `Tenda Uptime Formatted` sensor now includes fallback logic to handle unavailable or invalid uptime data, displaying "Offline" in such cases.

For further assistance, refer to the [Home Assistant documentation](https://www.home-assistant.io/docs/).