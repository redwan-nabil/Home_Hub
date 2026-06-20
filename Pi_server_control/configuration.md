# Pi Server Control - Configuration

This repository contains the `configuration.yaml` file for the `Pi_server_control` project. The configuration is designed to manage and monitor a Raspberry Pi server environment, integrating various functionalities such as automation, shell commands, MQTT sensors, and system monitoring.

## Features

1. **Default Integrations**:
   - The `default_config` integration is included to load the default set of Home Assistant integrations.

2. **Frontend Themes**:
   - Custom themes are loaded from the `themes` directory using the `!include_dir_merge_named` directive.

3. **Automation, Scripts, and Scenes**:
   - Automations, scripts, and scenes are modularized and included from their respective YAML files:
     - `automations.yaml`
     - `scripts.yaml`
     - `scenes.yaml`

4. **HTTP Configuration**:
   - Configured to use `X-Forwarded-For` headers for reverse proxy setups.
   - Trusted proxies include:
     - `127.0.0.1` (localhost)
     - `::1` (IPv6 localhost)
     - `172.17.0.2` and `172.17.0.0/16` (Docker network)
     - `192.168.0.0/16` (Local network)
     - `10.0.0.0/8` (Private network)

5. **Shell Commands**:
   - **Backup Trigger**: Initiates a Home Assistant backup in the background to prevent timeouts.
   - **Restart Nextcloud Container**: Restarts the Nextcloud Docker container with a forced kill after 5 seconds.
   - **Restart CCTV Container**: Restarts the MotionEye Docker container with a forced kill after 5 seconds.

6. **Command Line Sensors**:
   - **RPi5 Fan Speed**:
     - Monitors the fan speed of the Raspberry Pi 5.
     - Unit: RPM (Revolutions Per Minute)
     - Updates every 15 seconds.
   - **Main NVMe Health**:
     - Reads the health status of the main NVMe drive from a pre-generated file (`nvme_health.txt`).
     - Unit: Percentage (%)
     - Updates every 60 seconds.
   - **CCTV SSD Health**:
     - Reads the health status of the CCTV SSD from a pre-generated file (`sda_health.txt`).
     - Unit: Percentage (%)
     - Updates every 60 seconds.

7. **MQTT Binary Sensor**:
   - **CSI Room Occupancy**:
     - Monitors the occupancy status of the CSI room.
     - Listens to the MQTT topic `home/room/occupancy`.
     - Payloads:
       - `ON`: Room is occupied.
       - `OFF`: Room is unoccupied.
     - Device class: `occupancy`.

8. **Recorder Configuration**:
   - Limits the history retention to 2 days (default is 10 days).
   - Groups database writes every 30 seconds to improve performance.
   - Excludes specific domains and entities from being recorded:
     - **Domains**: `sun`, `weather`, `camera`, `update`
     - **Entities**: `sensor.time`, `sensor.date`

## File Structure

The configuration is modularized for better organization and maintainability. Below is the file structure:

```
Pi_server_control/
├── configuration.yaml  # Main configuration file
├── automations.yaml    # Automation rules
├── scripts.yaml        # Custom scripts
├── scenes.yaml         # Scene configurations
├── themes/             # Directory for frontend themes
│   ├── theme1.yaml
│   ├── theme2.yaml
│   └── ...
├── ssh_keys/           # Directory for SSH keys
│   └── id_rsa          # Private SSH key for remote commands
├── nvme_health.txt     # File containing NVMe health status
└── sda_health.txt      # File containing SSD health status
```

## Prerequisites

1. **Home Assistant**:
   - Ensure Home Assistant is installed and running on your Raspberry Pi server.

2. **SSH Configuration**:
   - Set up SSH access to the Raspberry Pi server.
   - Place the private SSH key (`id_rsa`) in the `ssh_keys` directory under the Home Assistant configuration folder.
   - Ensure the SSH key has the correct permissions (`chmod 600`).

3. **Docker**:
   - Ensure Docker is installed and configured on the Raspberry Pi server.
   - The `nextcloud` and `motioneye` containers should be running and accessible.

4. **MQTT Broker**:
   - Configure an MQTT broker and ensure the `home/room/occupancy` topic is published with the appropriate payloads (`ON`/`OFF`).

5. **System Monitoring**:
   - Ensure the Raspberry Pi server is configured to generate the `nvme_health.txt` and `sda_health.txt` files with the appropriate health data.

## Usage

1. **Backup**:
   - Trigger a Home Assistant backup by calling the `shell_command.run_ha_backup` service.

2. **Restart Containers**:
   - Restart the Nextcloud container by calling the `shell_command.restart_nextcloud` service.
   - Restart the MotionEye container by calling the `shell_command.restart_cctv` service.

3. **Monitor Sensors**:
   - View the following sensors in the Home Assistant dashboard:
     - `RPi5 Fan Speed`: Displays the current fan speed in RPM.
     - `Main NVMe Health`: Displays the health status of the main NVMe drive.
     - `CCTV SSD Health`: Displays the health status of the CCTV SSD.

4. **Room Occupancy**:
   - Monitor the occupancy status of the CSI room via the `CSI Room Occupancy` binary sensor.

5. **History Management**:
   - The recorder is configured to retain only 2 days of history and exclude unnecessary domains and entities to optimize database performance.

## Security Considerations

- Ensure the private SSH key (`id_rsa`) is stored securely and has the correct permissions (`chmod 600`).
- Limit access to the Raspberry Pi server and Home Assistant instance to trusted users.
- Regularly update your Home Assistant instance and Docker containers to patch security vulnerabilities.

## Customization

- Modify the `themes` directory to include your custom frontend themes.
- Update the `trusted_proxies` list under the `http` section to match your network configuration.
- Adjust the `purge_keep_days` and `commit_interval` values in the `recorder` section based on your storage and performance requirements.
- Add or modify shell commands and sensors as needed to suit your specific use case.

## Troubleshooting

- **SSH Issues**:
  - Ensure the SSH key is correctly configured and accessible by Home Assistant.
  - Verify the SSH connection to the Raspberry Pi server using the same key.

- **Sensor Data Not Updating**:
  - Check the paths to the `nvme_health.txt` and `sda_health.txt` files.
  - Ensure the files are being updated with the correct data.

- **MQTT Sensor Not Working**:
  - Verify the MQTT broker configuration and ensure the `home/room/occupancy` topic is being published with the correct payloads.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Support

If you encounter any issues or have questions, please open an issue in the repository.