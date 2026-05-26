# Pi_server_Core Configuration

This repository contains the `configuration.yaml` file for the `Pi_server_Core` project. The configuration is designed to manage and automate various services and devices in a home automation environment. Below is a detailed breakdown of the configuration and its components.

---

## Table of Contents

1. [Overview](#overview)
2. [Configuration Details](#configuration-details)
   - [Default Config](#default-config)
   - [Frontend](#frontend)
   - [Automation, Scripts, and Scenes](#automation-scripts-and-scenes)
   - [HTTP Configuration](#http-configuration)
   - [Shell Commands](#shell-commands)
   - [Command Line Sensors](#command-line-sensors)
   - [MQTT Binary Sensors](#mqtt-binary-sensors)
   - [Recorder](#recorder)
3. [Setup Instructions](#setup-instructions)
4. [Security Considerations](#security-considerations)
5. [License](#license)

---

## Overview

The `configuration.yaml` file is the core configuration file for the `Pi_server_Core` project. It integrates various services, automations, and sensors to enable seamless home automation. This configuration includes support for HTTP proxies, MQTT sensors, command-line sensors, shell commands, and more.

---

## Configuration Details

### Default Config
```yaml
default_config:
```
This section loads the default set of integrations provided by Home Assistant. **Do not remove this section** as it ensures basic functionality.

---

### Frontend
```yaml
frontend:
  themes: !include_dir_merge_named themes
```
- Loads custom frontend themes from the `themes` directory.
- Allows for a personalized user interface.

---

### Automation, Scripts, and Scenes
```yaml
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```
- **Automation**: Includes automation rules from `automations.yaml`.
- **Scripts**: Includes reusable scripts from `scripts.yaml`.
- **Scenes**: Includes predefined scenes from `scenes.yaml`.

---

### HTTP Configuration
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
- **use_x_forwarded_for**: Enables support for reverse proxies.
- **trusted_proxies**: Specifies a list of trusted proxy IPs. Ensure these IPs are accurate to avoid security risks.

---

### Shell Commands
```yaml
shell_command:
  run_ha_backup: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa redwannabil@127.0.0.1 'nohup bash /home/redwannabil/ha_backup.sh > /dev/null 2>&1 &'"
  restart_nextcloud: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa redwannabil@127.0.0.1 'docker restart -t 5 nextcloud'"
  restart_cctv: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa redwannabil@127.0.0.1 'docker restart -t 5 motioneye'"
```
- **run_ha_backup**: Triggers a Home Assistant backup script via SSH.
- **restart_nextcloud**: Restarts the Nextcloud Docker container with a forced timeout of 5 seconds.
- **restart_cctv**: Restarts the CCTV Docker container with a forced timeout of 5 seconds.

---

### Command Line Sensors
```yaml
command_line:
  - sensor:
      name: "RPi5 Fan Speed"
      command: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa redwannabil@127.0.0.1 'cat /sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input 2>/dev/null || echo 0'"
      unit_of_measurement: "RPM"
      scan_interval: 15
  - sensor:
      name: "Main NVMe Health"
      command: "cat /config/nvme_health.txt"
      unit_of_measurement: "%"
      icon: mdi:harddisk
      scan_interval: 60
  - sensor:
      name: "CCTV SSD Health"
      command: "cat /config/sda_health.txt"
      unit_of_measurement: "%"
      icon: mdi:harddisk
      scan_interval: 60
```
- **RPi5 Fan Speed**: Monitors the fan speed of the Raspberry Pi 5 in RPM. Updates every 15 seconds.
- **Main NVMe Health**: Reads the health status of the main NVMe drive from a local file. Updates every 60 seconds.
- **CCTV SSD Health**: Reads the health status of the CCTV SSD from a local file. Updates every 60 seconds.

---

### MQTT Binary Sensors
```yaml
mqtt:
  binary_sensor:
    - name: "CSI Room Occupancy"
      state_topic: "home/room/occupancy"
      payload_on: "ON"
      payload_off: "OFF"
      device_class: occupancy
```
- **CSI Room Occupancy**: Monitors room occupancy via MQTT messages. 
  - `state_topic`: Topic to listen for occupancy updates.
  - `payload_on`: Message indicating the room is occupied.
  - `payload_off`: Message indicating the room is unoccupied.
  - `device_class`: Set to `occupancy` for semantic meaning.

---

### Recorder
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
```
- **purge_keep_days**: Retains only the last 2 days of history to save storage space.
- **commit_interval**: Groups database writes every 30 seconds to improve performance.
- **exclude**: Excludes specific domains and entities from being recorded to reduce database size.

---

## Setup Instructions

1. **Clone the Repository**: Clone the `Pi_server_Core` repository to your local machine or server.
2. **Place Configuration Files**:
   - Ensure `configuration.yaml` is in the root directory of your Home Assistant configuration folder.
   - Place additional files like `automations.yaml`, `scripts.yaml`, and `scenes.yaml` in the same directory.
3. **Create Required Directories**:
   - Create a `themes` folder and populate it with your custom themes.
   - Ensure the `ssh_keys` directory exists under `/config` and contains the necessary SSH private key (`id_rsa`).
4. **Set Permissions**:
   - Ensure the SSH private key has the correct permissions (`chmod 600`).
   - Verify that the Home Assistant user has access to the required files and directories.
5. **Restart Home Assistant**:
   - Restart Home Assistant to apply the new configuration.

---

## Security Considerations

1. **SSH Key Management**:
   - Ensure the SSH private key is stored securely in `/config/ssh_keys/id_rsa`.
   - Use strong passwords for the SSH key if applicable.
2. **Trusted Proxies**:
   - Verify the IP addresses listed under `trusted_proxies` to prevent unauthorized access.
3. **File Permissions**:
   - Restrict access to sensitive files such as `id_rsa` and health status files (`nvme_health.txt`, `sda_health.txt`).
4. **Network Security**:
   - Ensure your network is secured with a strong password and firewall rules.
   - Use VLANs or other network segmentation techniques to isolate IoT devices.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.