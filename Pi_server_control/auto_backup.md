# Pi Server Control: `auto_backup.sh`

## Overview

The `auto_backup.sh` script is a comprehensive, automated backup solution for Raspberry Pi servers. It is designed to create backups of the Raspberry Pi OS, Home Assistant configurations, and Nextcloud administrative data. The script also includes features for resource management, cloud synchronization, and local retention policies. It is Docker-aware and ensures minimal disruption to system performance during backup operations.

---

## Features

1. **Unified Backup Pipeline**:
   - Creates backups for:
     - Raspberry Pi OS (`/dev/mmcblk0`)
     - Home Assistant configurations
     - Nextcloud administrative data (excluding user data)
   - Stores backups locally on a USB drive and uploads them to Google Drive.

2. **Resource-Aware CPU Governor**:
   - Monitors system load and Docker activity.
   - Pauses resource-intensive backup processes during high system load or active Docker operations.
   - Resumes backup processes when system resources are available.

3. **Telegram Notifications**:
   - Sends real-time updates about the backup process, including success, failure, and resource management events.

4. **Cloud Synchronization**:
   - Uploads Home Assistant and Nextcloud backups to Google Drive using `rclone`.
   - Deletes cloud backups older than 48 hours to save storage space.

5. **Local Retention Policy**:
   - Deletes local backups older than 3 days to manage disk space on the USB drive.

6. **System Cleanup**:
   - Removes unnecessary files and clears system caches to free up space before starting the backup process.

---

## Prerequisites

1. **Hardware**:
   - Raspberry Pi with a connected USB drive mounted at `/mnt/usb_backup`.

2. **Software**:
   - `rclone` installed and configured with access to Google Drive.
   - `pv` for monitoring progress during the `dd` operation.
   - `curl` for Telegram notifications.
   - `sudo` privileges for the user running the script.

3. **Configuration**:
   - Update the following variables in the script:
     - `TOKEN`: Your Telegram bot token.
     - `CHAT_ID`: Your Telegram chat ID.
     - `BASE_USB_DIR`: Path to the mounted USB drive.
     - `HA_SOURCE`: Path to the Home Assistant configuration directory.
     - `NC_SOURCE`: Path to the Nextcloud administrative data directory.
     - `rclone` configuration file path: Update the path to your `rclone.conf` file.

---

## Usage

1. **Setup**:
   - Place the `auto_backup.sh` script in a directory of your choice.
   - Make the script executable:
     ```bash
     chmod +x auto_backup.sh
     ```
   - Ensure the USB drive is mounted at the path specified in `BASE_USB_DIR`.

2. **Run the Script**:
   - Execute the script manually:
     ```bash
     ./auto_backup.sh
     ```
   - Or schedule it to run automatically using `cron`:
     ```bash
     crontab -e
     ```
     Add the following line to schedule the script (e.g., daily at 2:00 AM):
     ```bash
     0 2 * * * /path/to/auto_backup.sh
     ```

3. **Monitor Logs**:
   - Check the log file for detailed information about the backup process:
     ```bash
     tail -f /home/redwannabil/master_backup.log
     ```

---

## Backup Process Details

### 1. **Preparation**
- Creates necessary directories on the USB drive.
- Cleans up temporary files, old logs, and system caches.

### 2. **Throttled OS Backup**
- Creates a compressed image of the Raspberry Pi OS (`/dev/mmcblk0`) using `dd` and `gzip`.
- Limits the data transfer rate to 8 MB/s to reduce system impact.

### 3. **Home Assistant Backup**
- Archives the Home Assistant configuration directory into a `.tar.gz` file.

### 4. **Nextcloud Admin Backup**
- Archives the Nextcloud administrative data (excluding user data) into a `.tar.gz` file.

### 5. **Cloud Upload**
- Uploads Home Assistant and Nextcloud backups to Google Drive using `rclone`.
- Deletes cloud backups older than 48 hours.

### 6. **Local Retention**
- Deletes local backups older than 3 days to manage USB drive storage.

---

## Resource Management

The script includes a **CPU Governor** that monitors system load and Docker activity. If the system load exceeds `3.0` or if resource-intensive Docker commands are running, the script pauses backup processes (`dd`, `gzip`, `tar`, `rclone`). Once the load drops below `1.5` and Docker activity ceases, the backup processes resume.

---

## Notifications

The script uses Telegram to send real-time updates about the backup process. Notifications include:
- Pipeline start and completion.
- Success or failure of individual backup steps.
- Resource management events (e.g., pausing/resuming backups).

---

## Logs

All backup operations are logged in `/home/redwannabil/master_backup.log`. The log includes timestamps, step-by-step progress, and any errors encountered during the process.

---

## Error Handling

- If the OS backup fails, the script terminates immediately and sends a Telegram notification.
- If Home Assistant or Nextcloud backups fail, the script continues but logs a warning and sends a Telegram notification.

---

## Security Considerations

- Ensure the `TOKEN` and `CHAT_ID` variables are kept secure and not exposed in public repositories.
- Use appropriate permissions for the script and log files to prevent unauthorized access.

---

## Customization

- **Backup Frequency**: Adjust the `cron` schedule to change how often the script runs.
- **Retention Period**: Modify the `-mtime` value in the `find` commands to change the local retention period.
- **Cloud Storage**: Update the `rclone` configuration to use a different cloud provider if needed.

---

## Troubleshooting

1. **Script Fails to Run**:
   - Ensure the script is executable (`chmod +x auto_backup.sh`).
   - Verify the USB drive is mounted at the correct path.

2. **Telegram Notifications Not Received**:
   - Check the `TOKEN` and `CHAT_ID` values.
   - Test the Telegram bot manually using `curl`:
     ```bash
     curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" -d chat_id="<CHAT_ID>" -d text="Test message"
     ```

3. **Cloud Upload Fails**:
   - Verify the `rclone` configuration file path and credentials.
   - Test the `rclone` connection manually:
     ```bash
     rclone lsd gdrive:
     ```

4. **High System Load**:
   - The CPU Governor should automatically handle high system load. If issues persist, consider increasing the thresholds in the `governor_loop` function.

---

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk. Ensure you have proper backups and test the script in a safe environment before deploying it in production.