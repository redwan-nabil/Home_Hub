# fan_logger.sh

## Overview
`fan_logger.sh` is a simple Bash script designed to monitor and log the speed of a cooling fan on a Raspberry Pi or similar device. The script continuously reads the fan speed from the system's hardware monitoring interface and writes the value to a specified file. This file can then be used by external systems, such as Home Assistant, for further processing or display.

## Features
- **Continuous Monitoring**: The script runs in an infinite loop, ensuring that fan speed data is consistently logged.
- **Home Assistant Integration**: The fan speed is written to a file (`fan_speed.txt`) located in the Home Assistant configuration directory, making it easy to integrate with Home Assistant dashboards or automations.
- **Error Handling**: If the fan speed cannot be read (e.g., due to missing hardware or permissions), the script logs a default value of `0` to ensure the output file is always updated.

## Prerequisites
1. **Hardware**: The script assumes the presence of a cooling fan connected to the system, with its speed accessible via the `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input` interface.
2. **Permissions**: The script must have read access to the fan speed file (`/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input`) and write access to the Home Assistant configuration directory (`/home/redwannabil/homeassistant/`).
3. **Home Assistant**: Ensure Home Assistant is installed and configured to read the `fan_speed.txt` file for integration.

## Installation
1. **Clone the Repository**: Clone the `Pi_server_control` repository to your Raspberry Pi or desired server.
2. **Place the Script**: Ensure `fan_logger.sh` is located in the appropriate directory within the repository.
3. **Set Permissions**: Make the script executable:
   ```bash
   chmod +x fan_logger.sh
   ```
4. **Run the Script**: Execute the script manually or set it up to run as a background service:
   ```bash
   ./fan_logger.sh
   ```

## Usage
The script continuously monitors the fan speed and writes the value to the `fan_speed.txt` file every 15 seconds. The file is located at:
```
/home/redwannabil/homeassistant/fan_speed.txt
```

### Example Output
The `fan_speed.txt` file will contain a single integer value representing the fan's speed in RPM (revolutions per minute). If the fan speed cannot be read, the file will contain `0`.

Example:
```
1200
```

## Integration with Home Assistant
To display the fan speed in Home Assistant:
1. Add a `file` sensor to your Home Assistant configuration:
   ```yaml
   sensor:
     - platform: file
       name: Fan Speed
       file_path: /home/redwannabil/homeassistant/fan_speed.txt
       unit_of_measurement: "RPM"
   ```
2. Restart Home Assistant to apply the changes.
3. The fan speed will now be available as a sensor in Home Assistant.

## Automation
To ensure the script runs continuously, you can set it up as a systemd service:

1. **Create a Service File**:
   ```bash
   sudo nano /etc/systemd/system/fan_logger.service
   ```
   Add the following content:
   ```ini
   [Unit]
   Description=Fan Logger Service
   After=network.target

   [Service]
   ExecStart=/path/to/fan_logger.sh
   Restart=always
   User=your-username

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and Start the Service**:
   ```bash
   sudo systemctl enable fan_logger.service
   sudo systemctl start fan_logger.service
   ```

3. **Check the Service Status**:
   ```bash
   sudo systemctl status fan_logger.service
   ```

## Troubleshooting
- **Fan Speed Not Updating**: Ensure the fan speed file exists at `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input`. If not, verify your hardware and drivers.
- **Permission Issues**: Run the script with sufficient privileges or adjust file permissions as needed.
- **File Not Found**: Ensure the Home Assistant configuration directory (`/home/redwannabil/homeassistant/`) exists and is writable by the script.

## Notes
- The script uses a default polling interval of 15 seconds. You can modify this interval by changing the `sleep 15` line in the script.
- The script assumes a specific file path for the fan speed. If your hardware uses a different path, update the script accordingly.

## License
This script is part of the `Pi_server_control` project and is licensed under the terms of the project's license.

## Disclaimer
This script is provided as-is without any guarantees. Use it at your own risk. Ensure you understand the script and its implications before running it on your system.