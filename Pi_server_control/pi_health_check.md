# Pi Health Check Script (`pi_health_check.sh`)

## Overview
The `pi_health_check.sh` script is a health monitoring utility designed for Raspberry Pi devices. It performs critical system checks to ensure the device is operating within safe parameters and alerts the user if any issues are detected. The script is intended to be used as part of the `Pi_server_control` project.

## Features
The script performs the following health checks:
1. **CPU Temperature Monitoring**: Checks if the CPU temperature exceeds a safe threshold (60°C).
2. **SD Card Read-Only Status**: Verifies if the root filesystem has been switched to read-only mode, which may indicate SD card corruption or failure.
3. **Disk Space Usage**: Monitors the disk space usage of the root filesystem and alerts if usage exceeds 60%.

## Prerequisites
- The script assumes the presence of the `pi_alert` utility located at `/usr/local/bin/pi_alert`. This utility is used to send alerts when issues are detected.
- The script requires basic Linux utilities such as `cat`, `awk`, `grep`, `df`, and `sed`, which are typically available on most Linux distributions.

## Installation
1. Clone the `Pi_server_control` repository to your Raspberry Pi.
2. Place the `pi_health_check.sh` script in the desired directory (e.g., `/usr/local/bin/`).
3. Ensure the script has executable permissions:
   ```bash
   chmod +x /path/to/pi_health_check.sh
   ```
4. Verify that the `pi_alert` utility is installed and accessible at `/usr/local/bin/pi_alert`.

## Usage
Run the script manually or set it up as a cron job for periodic health checks.

### Running Manually
To execute the script manually, use the following command:
```bash
/path/to/pi_health_check.sh
```

### Setting Up a Cron Job
To automate the health checks, add the script to your crontab:
1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add an entry to run the script at your desired interval. For example, to run the script every 5 minutes:
   ```bash
   */5 * * * * /path/to/pi_health_check.sh
   ```

## Alerts
The script uses the `pi_alert` utility to send alerts when issues are detected. Below are the possible alerts:
1. **Overheating Alert**:
   - Message: `🔥 WARNING: Raspberry Pi is overheating! Current Temp: <TEMP>°C`
   - Trigger: CPU temperature is 60°C or higher.
2. **SD Card Read-Only Alert**:
   - Message: `🚨 CRITICAL: SD Card has switched to READ-ONLY mode! The drive is failing. Please replace hardware.`
   - Trigger: Root filesystem is mounted in read-only mode.
3. **Disk Space Alert**:
   - Message: `💾 STORAGE ALERT: Raspberry Pi SD card is <DISK_USAGE>% full!`
   - Trigger: Disk usage of the root filesystem is 60% or higher.

## Customization
You can customize the thresholds for the checks by modifying the script:
- **CPU Temperature Threshold**: Update the value `60` in the following line:
  ```bash
  if [ "$TEMP_C" -ge 60 ]; then
  ```
- **Disk Usage Threshold**: Update the value `60` in the following line:
  ```bash
  if [ "$DISK_USAGE" -ge 60 ]; then
  ```

## Troubleshooting
- **`pi_alert` Not Found**: Ensure the `pi_alert` utility is installed and located at `/usr/local/bin/pi_alert`. If it's located elsewhere, update the script to reflect the correct path.
- **Permissions Issues**: Ensure the script has executable permissions:
  ```bash
  chmod +x /path/to/pi_health_check.sh
  ```
- **Cron Job Not Running**: Verify the cron service is running and check the cron logs for errors:
  ```bash
  sudo service cron status
  grep CRON /var/log/syslog
  ```

## Limitations
- The script does not provide detailed diagnostics or remediation steps beyond sending alerts.
- The thresholds for CPU temperature and disk usage are hardcoded but can be manually adjusted in the script.

## License
This script is part of the `Pi_server_control` project and is licensed under the MIT License. See the project repository for more details.

## Author
This script was developed as part of the `Pi_server_control` project by the DevOps team. For questions or support, please contact the project maintainers.