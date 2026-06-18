# fan_logger.sh

## Overview
`fan_logger.sh` is a Bash script designed to continuously monitor and log the fan speed of a system. It reads the fan speed data from the system hardware and writes it to a file in the Home Assistant configuration folder. This script is intended to provide real-time fan speed data for integration with Home Assistant or other monitoring tools.

## Features
- Continuously monitors the fan speed of the system.
- Writes the fan speed data to a text file (`fan_speed.txt`) in the Home Assistant configuration directory.
- Handles cases where the fan speed data is unavailable by defaulting to `0`.
- Runs in an infinite loop with a 15-second interval between readings.

## Prerequisites
- The script assumes that the system exposes fan speed data via the `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input` file path.
- Ensure that the user running the script has the necessary permissions to read from the `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input` file and write to the Home Assistant configuration directory.

## Installation
1. Save the script as `fan_logger.sh` in a directory of your choice.
2. Make the script executable:
   ```bash
   chmod +x fan_logger.sh
   ```

## Usage
1. Run the script in the background to continuously log fan speed:
   ```bash
   ./fan_logger.sh &
   ```
2. The script will create or update the `fan_speed.txt` file in the Home Assistant configuration directory (`/home/redwannabil/homeassistant/`).

## File Output
- **File Path:** `/home/redwannabil/homeassistant/fan_speed.txt`
- **Content:** The current fan speed in RPM (revolutions per minute). If the fan speed cannot be read, the file will contain `0`.

## How It Works
1. The script runs an infinite loop (`while true`).
2. In each iteration:
   - It attempts to read the fan speed from the system file `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input`.
   - If the fan speed cannot be read (e.g., due to missing hardware or permissions), it defaults to writing `0`.
   - The output is redirected to the `fan_speed.txt` file in the Home Assistant configuration directory.
3. The script waits for 15 seconds before repeating the process.

## Customization
- **File Path for Home Assistant Configuration:**  
  If your Home Assistant configuration directory is different, update the file path in the script:
  ```bash
  /home/redwannabil/homeassistant/fan_speed.txt
  ```
  Replace `/home/redwannabil/homeassistant/` with your actual Home Assistant configuration directory.

- **Fan Speed Source Path:**  
  If your system exposes fan speed data at a different path, update the following line in the script:
  ```bash
  sh -c 'cat /sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input 2>/dev/null || echo 0'
  ```
  Replace `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input` with the correct path for your system.

- **Interval Between Readings:**  
  To change the interval between readings, modify the `sleep` duration:
  ```bash
  sleep 15
  ```
  Replace `15` with the desired number of seconds.

## Notes
- Ensure that the script is run with sufficient permissions to access the required system files and directories.
- Running the script as a background process (`&`) is recommended for continuous monitoring.
- If the script is terminated, fan speed logging will stop. Consider using a process manager (e.g., `systemd` or `cron`) to ensure the script runs continuously.

## Troubleshooting
- **Permission Denied Errors:**  
  Ensure the user running the script has read permissions for `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input` and write permissions for `/home/redwannabil/homeassistant/`.

- **File Not Found Errors:**  
  Verify that the fan speed data is available at `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input`. The exact path may vary depending on your hardware and system configuration.

- **High CPU Usage:**  
  If the script causes high CPU usage, consider increasing the sleep interval to reduce the frequency of readings.

## Disclaimer
This script is provided as-is without any warranty. Use it at your own risk. Ensure you understand the script and its implications before running it on your system.