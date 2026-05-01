# 🚀 Release Notes

### Version: v4.5 (Updated)
The `auto_backup.sh` script in the `Pi_server_control` project has been updated with the following changes:

1. **Introduction of Docker-Aware CPU Governor**:
   - A new `governor_loop` function has been added to monitor system load and active Docker processes.
   - The governor dynamically pauses (`STOP`) or resumes (`CONT`) resource-intensive backup processes (`dd`, `gzip`, `tar`, `rclone`) based on system load and Docker activity.

2. **Enhanced Logging**:
   - Improved logging with timestamps for each step in the backup process.
   - Logs are appended to a centralized log file located at `/home/redwannabil/master_backup.log`.

3. **Telegram Notifications**:
   - Added Telegram notifications for key events such as backup start, success, failure, and completion.
   - Notifications for resource conflicts and resolutions are commented out but can be enabled.

4. **Backup Pipeline Improvements**:
   - **Step 0**: Pre-backup cleanup tasks (e.g., removing temporary files, clearing journal logs, and dropping caches).
   - **Step 1**: Throttled OS backup using `pv` to limit the data transfer rate.
   - **Step 2**: Home Assistant backup with error handling for partial success.
   - **Step 3**: Nextcloud Admin backup with exclusion of the `data` directory.
   - **Step 4**: Cloud upload to Google Drive using `rclone` with retention policies for backups older than 48 hours.
   - **Step 5**: Local USB retention policy to delete backups older than 3 days.

5. **Resource Optimization**:
   - Use of `nice` and `ionice` for low-priority cloud upload tasks.
   - Added system resource cleanup commands to free up memory and disk space.

---

# Pi Server Control - Auto Backup Script

## Overview
The `auto_backup.sh` script is a comprehensive backup solution for Raspberry Pi servers. It is designed to create and manage backups of the Raspberry Pi OS, Home Assistant, and Nextcloud Admin settings. The script is optimized for resource-constrained environments and includes a Docker-aware CPU governor to ensure system stability during backup operations.

## Features
- **Throttled OS Backup**: Creates compressed OS images with controlled data transfer rates.
- **Home Assistant Backup**: Archives Home Assistant configurations and data.
- **Nextcloud Admin Backup**: Archives Nextcloud Admin settings while excluding large data directories.
- **Cloud Sync**: Uploads backups to Google Drive using `rclone` with retention policies.
- **Local Retention Management**: Automatically deletes old backups from the local USB drive.
- **Resource-Aware Governor**: Monitors system load and Docker activity to pause/resume resource-intensive tasks dynamically.
- **System Cleanup**: Removes temporary files, clears journal logs, and drops caches before starting backups.
- **Telegram Notifications**: Sends real-time updates about the backup process to a specified Telegram chat.

## Prerequisites
1. **Hardware**:
   - Raspberry Pi 5 or compatible device.
   - External USB storage mounted at `/mnt/usb_backup/server_backup`.

2. **Software**:
   - `rclone` installed and configured for Google Drive.
   - `pv` installed for throttling data transfer during OS backup.
   - `curl` installed for Telegram notifications.

3. **Permissions**:
   - The script requires `sudo` privileges for certain operations (e.g., creating backups, cleaning system resources).

4. **Configuration**:
   - Update the `TOKEN` and `CHAT_ID` variables with your Telegram bot token and chat ID.
   - Ensure the `rclone` configuration file is located at `/home/redwannabil/.config/rclone/rclone.conf`.

## Installation
1. Clone the `Pi_server_control` repository:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. Make the script executable:
   ```bash
   chmod +x auto_backup.sh
   ```

3. Schedule the script to run automatically using `cron`:
   ```bash
   crontab -e
   ```
   Add the following line to schedule the script to run daily at 2 AM:
   ```bash
   0 2 * * * /path/to/Pi_server_control/auto_backup.sh
   ```

## Usage
Run the script manually:
```bash
sudo ./auto_backup.sh
```

## Script Workflow
1. **Initialization**:
   - Sets up logging and initializes variables for directories, sources, and Telegram settings.

2. **CPU Governor**:
   - Continuously monitors system load and Docker activity.
   - Pauses or resumes resource-intensive processes (`dd`, `gzip`, `tar`, `rclone`) based on system conditions.

3. **Backup Pipeline**:
   - **Step 0**: Prepares directories and cleans up system resources.
   - **Step 1**: Creates a throttled backup of the Raspberry Pi OS.
   - **Step 2**: Archives Home Assistant configurations and data.
   - **Step 3**: Archives Nextcloud Admin settings, excluding large data directories.
   - **Step 4**: Uploads Home Assistant and Nextcloud backups to Google Drive.
   - **Step 5**: Deletes old backups from the local USB drive.

4. **Notifications**:
   - Sends updates to a Telegram chat at key stages of the backup process.

5. **Cleanup**:
   - Ensures the CPU governor process is terminated when the script exits.

## Configuration
### Telegram Notifications
To enable Telegram notifications:
1. Create a Telegram bot using [BotFather](https://core.telegram.org/bots#botfather).
2. Obtain the bot token and your chat ID.
3. Replace the `TOKEN` and `CHAT_ID` placeholders in the script with your values.

### rclone Configuration
1. Install `rclone`:
   ```bash
   sudo apt update && sudo apt install rclone
   ```
2. Configure `rclone` for Google Drive:
   ```bash
   rclone config
   ```
3. Verify the configuration file is located at `/home/redwannabil/.config/rclone/rclone.conf`.

## Logging
- Logs are stored in `/home/redwannabil/master_backup.log`.
- Each step in the backup process is timestamped for easy debugging.

## Error Handling
- The script includes error handling for critical steps such as OS backup, Home Assistant backup, and cloud uploads.
- If an error occurs, a Telegram notification is sent, and the script exits with a non-zero status.

## Notes
- The CPU governor is designed to prioritize system stability over backup speed. If the system load exceeds a threshold or if Docker is actively running resource-intensive tasks, the backup processes will be paused.
- Ensure sufficient storage space is available on the USB drive and Google Drive to avoid backup failures.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Developed by [Your Name]. For support or inquiries, please contact [Your Email].