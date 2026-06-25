# 🚀 Release Notes

### Changes in `configuration.yaml`
The following updates have been made to the `configuration.yaml` file:

1. **New Sections Added:**
   - **Advanced Template Sensors:**
     - Added new template sensors for dynamic prayer times, human-readable countdowns, and Waqt progress percentage.
     - Added a new sensor for "Tenda Internal Stopwatch" to track router uptime more accurately.
     - Added a new sensor for "Predator Live Power Draw" to estimate power consumption based on CPU and GPU load.
   - **Energy Tracking Engine:**
     - Added new sensors for tracking energy consumption of additional devices (Predator, Redwan's S23, and S10 FE).
     - Added utility meters for daily and monthly electricity usage for the Predator device.
   - **Command Line Sensors:**
     - Added safety nets to value templates for existing command line sensors to handle unexpected or invalid values.
   - **System Recorder:**
     - Updated the `recorder` section to exclude additional entities and domains for better database performance.
   - **Shell Commands:**
     - Updated `export_flight` and `cleanup_flight_log` commands for better safety and functionality.
   - **External Services:**
     - No changes made to the `zone`, `geo_location`, `rest_command`, and `google_assistant` configurations.

2. **Removed Sections:**
   - Removed the `cleanup_helicopter_log` shell command.
   - Removed the "Helicopter Surveillance Log 10km" template sensor.

3. **General Improvements:**
   - Improved the formatting and readability of the YAML file by adding section headers and comments.
   - Enhanced the safety and robustness of command line sensors and shell commands.

---

# Home Assistant Configuration

This repository contains the `configuration.yaml` file for a Home Assistant instance. The configuration includes various integrations, sensors, automations, and external services to enhance the smart home experience.

## Features

### Default Configuration
- Loads the default set of integrations provided by Home Assistant.

### Frontend Themes
- Custom themes are loaded from the `themes` directory.

### Automations, Scripts, and Scenes
- Automations, scripts, and scenes are included from their respective YAML files.

### HTTP Configuration
- Supports `use_x_forwarded_for` for reverse proxy setups.
- Configures a list of trusted proxies to ensure secure communication.

### Dashboard Controls
- Adds an `input_boolean` entity to toggle the display of Raspberry Pi power history.

### Shell Commands
- Predefined shell commands for tasks such as:
  - Running Home Assistant backups.
  - Restarting Nextcloud and CCTV services.
  - Exporting and cleaning flight logs.

### Command Line Sensors
- Monitors system metrics using command-line scripts:
  - Raspberry Pi fan speed.
  - Main NVMe health.
  - CCTV SSD health.
  - Raspberry Pi live power draw.
- Safety nets added to handle unexpected or invalid values.

### Energy Tracking Engine
- Tracks energy consumption (kWh) for various devices using integration sensors:
  - Raspberry Pi 5.
  - Predator device.
  - Redwan's S23 and S10 FE devices.
- Utility meters for daily and monthly electricity usage.

### System Recorder
- Configured to retain data for 2 days and commit every 30 seconds.
- Excludes certain domains and entities to optimize database performance.

### Advanced Template Sensors
- Dynamic sensors for:
  - Tracking prayer times and prohibited times.
  - Displaying human-readable countdowns to the next event.
  - Calculating Waqt progress percentage.
  - Formatting router uptime.
  - Estimating Predator device's live power draw based on CPU and GPU load.

### External Services
- **Zone Configuration:**
  - Defines a 10km airspace dome for tracking.
- **Geo-location:**
  - Configures USGS Earthquake Feed to monitor earthquakes within a 1500km radius.
- **REST Commands:**
  - Commands for pausing and resuming torrents on a qBittorrent server.
- **Google Assistant Integration:**
  - Exposes specific domains to Google Assistant for voice control.

---

## File Structure

```plaintext
/configuration.yaml
/themes/                # Directory for custom themes
/automations.yaml       # File for automations
/scripts.yaml           # File for scripts
/scenes.yaml            # File for scenes
/config/www/            # Directory for external files (e.g., logs, backups)
/config/ssh_keys/       # Directory for SSH keys
/SERVICE_ACCOUNT.json   # Google Assistant service account credentials
```

---

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Install Home Assistant:**
   Follow the [official installation guide](https://www.home-assistant.io/installation/) to set up Home Assistant.

3. **Place Configuration Files:**
   Copy the `configuration.yaml` file and other necessary files to your Home Assistant configuration directory.

4. **Set Up SSH Keys:**
   - Place your SSH private key in the `/config/ssh_keys/` directory.
   - Ensure the key has the correct permissions:
     ```bash
     chmod 600 /config/ssh_keys/id_rsa
     ```

5. **Google Assistant Integration:**
   - Place the `SERVICE_ACCOUNT.json` file in the Home Assistant configuration directory.
   - Follow the [Google Assistant setup guide](https://www.home-assistant.io/integrations/google_assistant/) to configure the integration.

6. **Restart Home Assistant:**
   Restart Home Assistant to apply the new configuration:
   ```bash
   sudo systemctl restart home-assistant
   ```

---

## Notes

- Ensure all external scripts and files referenced in the configuration (e.g., `fan_speed.txt`, `nvme_health.txt`) are present in the specified directories.
- Update the IP addresses in the `trusted_proxies` and `rest_command` sections to match your network configuration.
- Regularly monitor the `recorder` database size and adjust the `purge_keep_days` setting as needed.

---

## Troubleshooting

- **Configuration Errors:**
  Run the following command to check for syntax errors in the configuration:
  ```bash
  ha core check
  ```

- **Database Size:**
  If the database grows too large, consider increasing the `purge_keep_days` or excluding additional domains/entities in the `recorder` section.

- **SSH Issues:**
  Ensure the SSH keys are correctly configured and the target devices allow SSH connections.

For further assistance, refer to the [Home Assistant documentation](https://www.home-assistant.io/docs/).