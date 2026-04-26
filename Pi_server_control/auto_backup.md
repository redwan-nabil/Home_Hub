# 🚀 Release Notes

### Version: v4.5 (Updated)
The following changes have been made to the `auto_backup.sh` script in the `Pi_server_control` project:

1. **Telegram Notification Enhancements**:
   - Added notifications for resource conflict detection and resolution during the backup process.
   - Improved messaging for better clarity and user feedback.

2. **CPU Governor Enhancements**:
   - Enhanced the `governor_loop` function to dynamically pause and resume resource-intensive processes (`dd`, `gzip`, `tar`, `rclone`) based on CPU load and Docker activity.
   - Introduced logic to detect aggressive Docker commands (`docker compose`, `docker build`, `docker run`) and adjust backup operations accordingly.

3. **Improved Resource Management**:
   - Added `sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches` to clear system caches before starting the backup process.

4. **Cloud Upload Improvements**:
   - Added retention policy for Google Drive backups: Deletes backups older than 48 hours from the cloud storage.

5. **Code Refactoring**:
   - Improved readability and maintainability of the script with better comments and structure.

---

# Pi Server Control - `auto_backup.sh`

## Overview
The `auto_backup.sh` script is a unified backup solution for Raspberry Pi servers. It is designed to back up the Raspberry Pi OS, Home Assistant configurations, and Nextcloud admin settings to both a local USB drive and Google Drive. The script is optimized for resource management and includes a Docker-aware CPU governor to ensure system stability during the backup process.

---

## Features
1. **Automated Backup Pipeline**:
   - Creates backups for Raspberry Pi OS, Home Assistant, and Nextcloud admin settings.
   - Stores backups locally on a USB drive and uploads them to Google Drive.

2. **Docker-Aware CPU Governor**:
   - Monitors system load and Docker activity.
   - Pauses resource-intensive backup processes during high system load or active Docker operations.
   - Resumes backup processes when system resources are available.

3. **Telegram Notifications**:
   - Sends real-time notifications about the backup process, including:
     - Start and completion of the backup pipeline.
     - Resource conflicts and resolutions.
     - Success or failure of individual backup steps.
     - Cloud upload status.

4. **Retention Policies**:
   - Deletes local backups older than 3 days.
   - Deletes cloud backups older than 48 hours.

5. **System Maintenance**:
   - Performs system cleanup tasks, including:
     - Removing unused packages.
     - Cleaning temporary files.
     - Vacuuming system logs older than 3 days.
     - Clearing system caches.

---

## Prerequisites
1. **Hardware**:
   - Raspberry Pi 5 or compatible device.
   - External USB storage device mounted at `/mnt/usb_backup`.

2. **Software**:
   - `rclone` installed and configured for Google Drive.
   - `pv` package for monitoring data transfer rates.
   - `curl` for Telegram notifications.
   - `tar` and `gzip` for compression.

3. **Permissions**:
   - Script must be run with `sudo` privileges to perform system-level operations.

4. **Configuration**:
   - Update the following variables in the script:
     - `TOKEN`: Your Telegram bot token.
     - `CHAT_ID`: Your Telegram chat ID.
     - `BASE_USB_DIR`: Path to the mounted USB storage.
     - `HA_SOURCE`: Path to the Home Assistant configuration directory.
     - `NC_SOURCE`: Path to the Nextcloud admin directory.
     - `rclone` configuration file path.

---

## Usage
1. **Make the script executable**:
   ```bash
   chmod +x auto_backup.sh
   ```

2. **Run the script**:
   ```bash
   sudo ./auto_backup.sh
   ```

3. **Automate with Cron**:
   - Add the script to your crontab for periodic execution:
     ```bash
     sudo crontab -e
     ```
   - Add the following line to schedule the script (e.g., daily at 2 AM):
     ```bash
     0 2 * * * /path/to/auto_backup.sh
     ```

---

## Script Workflow
1. **Preparation**:
   - Creates necessary directories for backups.
   - Cleans up temporary files and performs system maintenance.

2. **CPU Governor**:
   - Monitors system load and Docker activity.
   - Pauses and resumes backup processes based on system resource availability.

3. **Backup Steps**:
   - **Step 1**: Creates a compressed image of the Raspberry Pi OS and saves it to the local USB drive.
   - **Step 2**: Archives the Home Assistant configuration directory and saves it to the local USB drive.
   - **Step 3**: Archives the Nextcloud admin directory (excluding `data` folder) and saves it to the local USB drive.

4. **Cloud Upload**:
   - Deletes cloud backups older than 48 hours.
   - Uploads Home Assistant and Nextcloud backups to Google Drive.

5. **Retention Policy**:
   - Deletes local backups older than 3 days.

6. **Completion**:
   - Sends a final notification indicating the successful completion of the backup pipeline.

---

## Logs
- All logs are saved to `/home/redwannabil/master_backup.log`.
- Logs include timestamps and detailed information about each step of the backup process.

---

## Troubleshooting
1. **Backup Failure**:
   - Check the log file for error messages: `/home/redwannabil/master_backup.log`.
   - Ensure the USB drive is mounted at the correct location (`/mnt/usb_backup`).
   - Verify that the `rclone` configuration file is correctly set up.

2. **Telegram Notifications Not Working**:
   - Verify the `TOKEN` and `CHAT_ID` values in the script.
   - Test the Telegram bot using the `curl` command:
     ```bash
     curl -s -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage" -d chat_id=<YOUR_CHAT_ID> -d text="Test message"
     ```

3. **High System Load**:
   - The CPU governor automatically pauses backup processes during high system load. Wait for the system to stabilize, and the backup will resume automatically.

---

## Notes
- The script is designed to be run on a Raspberry Pi 5 but may work on other Linux-based systems with minor modifications.
- Ensure sufficient storage space is available on the USB drive and Google Drive before running the script.
- The script is designed to handle common errors gracefully and provide detailed logs and notifications for troubleshooting.

---

## License
This script is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.