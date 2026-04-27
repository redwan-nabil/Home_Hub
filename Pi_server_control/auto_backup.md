# 🚀 Release Notes

### Version 5.0 Updates
- **NVMe Optimization**: Backup now targets `/dev/nvme0n1` instead of `/dev/mmcblk0` for faster OS backups.
- **Compression Tool Update**: Replaced `gzip` with `pigz` for multi-threaded compression.
- **Throttling Enhancements**: Increased `pv` speed limit from `8m` to `50m` for faster data transfer.
- **Docker-Aware Governor Improvements**:
  - Now pauses and resumes `pigz` instead of `gzip`.
  - Enhanced resource conflict detection and resolution.
- **Cloud Upload Configuration**: Centralized `rclone` configuration path to a variable for better maintainability.
- **Retention Policy**: Improved local USB retention logic to clean backups older than 3 days.
- **System Cleanup**: Added cleanup of temporary PDF files and reduced journal logs to 3 days.
- **Error Handling**: Improved error handling and notifications for OS and cloud backup failures.
- **Notifications**: Enhanced Telegram notifications for better clarity and status updates.

---

# Pi Server Control: `auto_backup.sh`

## Overview
The `auto_backup.sh` script is a unified backup pipeline designed for Raspberry Pi servers. It automates the backup of the operating system, Home Assistant, and Nextcloud configurations to both local USB storage and Google Drive. The script is optimized for systems using NVMe storage and includes a Docker-aware CPU governor to manage system resources during high-load conditions.

---

## Features
1. **Automated Backup Pipeline**:
   - Backs up Raspberry Pi OS, Home Assistant, and Nextcloud configurations.
   - Supports local USB storage and cloud synchronization with Google Drive.

2. **NVMe Optimization**:
   - Leverages `/dev/nvme0n1` for faster OS backups.
   - Uses `pigz` for multi-threaded compression.

3. **Docker-Aware CPU Governor**:
   - Monitors system load and Docker activity.
   - Pauses and resumes backup processes (`dd`, `pigz`, `tar`, `rclone`) to prioritize system tasks.

4. **Cloud Integration**:
   - Synchronizes backups to Google Drive using `rclone`.
   - Deletes cloud backups older than 48 hours to save storage.

5. **Retention Policy**:
   - Deletes local USB backups older than 3 days.

6. **System Cleanup**:
   - Removes temporary files and reduces journal logs to optimize disk space.

7. **Real-Time Notifications**:
   - Sends status updates and error notifications via Telegram.

---

## Prerequisites
1. **Hardware**:
   - Raspberry Pi with NVMe storage.
   - External USB storage for local backups.

2. **Software**:
   - `rclone` installed and configured with Google Drive.
   - `pigz`, `pv`, and `tar` installed.
   - Telegram bot token and chat ID for notifications.

3. **Permissions**:
   - Script must be run with `sudo` privileges.

---

## Configuration
### Variables
- **Directories**:
  - `BASE_USB_DIR`: Base directory for USB backups.
  - `OS_DIR`, `HA_DIR`, `NC_DIR`: Subdirectories for OS, Home Assistant, and Nextcloud backups.
- **Sources**:
  - `HA_SOURCE`: Path to Home Assistant configuration.
  - `NC_SOURCE`: Path to Nextcloud configuration.
- **Telegram**:
  - `TOKEN`: Telegram bot token.
  - `CHAT_ID`: Telegram chat ID.
- **Rclone**:
  - `RCLONE_CONF`: Path to `rclone` configuration file.

### Modify the Script
Update the following variables in the script to match your environment:
- `BASE_USB_DIR`
- `HA_SOURCE`
- `NC_SOURCE`
- `TOKEN`
- `CHAT_ID`
- `RCLONE_CONF`

---

## Usage
1. **Run the Script**:
   ```bash
   sudo ./auto_backup.sh
   ```

2. **Automate with Cron**:
   Add the script to your crontab for periodic execution. For example, to run daily at 2 AM:
   ```bash
   0 2 * * * /path/to/auto_backup.sh
   ```

---

## Pipeline Steps
1. **Preparation**:
   - Creates necessary directories.
   - Cleans up temporary files and reduces system logs.

2. **OS Backup**:
   - Creates a compressed image of the NVMe storage using `dd`, `pv`, and `pigz`.

3. **Home Assistant Backup**:
   - Archives the Home Assistant configuration directory.

4. **Nextcloud Backup**:
   - Archives the Nextcloud configuration directory, excluding `data` files.

5. **Cloud Upload**:
   - Deletes cloud backups older than 48 hours.
   - Uploads fresh backups to Google Drive.

6. **Retention**:
   - Deletes local USB backups older than 3 days.

---

## Error Handling
- **OS Backup Failure**:
  - Sends a Telegram notification and exits the script.
- **Cloud Upload Issues**:
  - Sends a warning notification if any upload fails.

---

## Logs
- Logs are stored in `/home/redwannabil/master_backup.log`.
- Includes timestamps and detailed output of each step.

---

## Known Issues
- Ensure sufficient storage space is available on both the USB drive and Google Drive.
- Verify `rclone` configuration and permissions for Google Drive.

---

## Future Improvements
- Add support for incremental backups.
- Include monitoring for additional system resources (e.g., memory usage).
- Extend cloud support to other providers (e.g., AWS S3, Dropbox).

---

## License
This script is provided under the MIT License. Use at your own risk.