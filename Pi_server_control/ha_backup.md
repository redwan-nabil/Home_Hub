# HA Backup Script (`ha_backup.sh`) Documentation

## Overview
The `ha_backup.sh` script automates the backup process for Home Assistant (HA) configurations. It compresses the HA directory, stores the backup on a USB drive, uploads it to Google Drive, and performs cleanup operations for both local and cloud backups. Notifications are sent via Telegram to inform the user of the backup status.

---

## Features
1. **Automated Backup**:
   - Compresses the Home Assistant directory into a `.tar.gz` file.
   - Saves the backup to a USB drive.

2. **Cloud Integration**:
   - Uploads the backup to Google Drive using `rclone`.

3. **Cleanup Operations**:
   - Deletes local backups older than 7 days.
   - Deletes cloud backups older than 1 day.

4. **Notifications**:
   - Sends status updates (success or failure) via Telegram.

5. **Performance Optimization**:
   - Uses `nice` and `ionice` to minimize system resource impact during compression and upload.

---

## Prerequisites
### 1. **Hardware Requirements**:
   - USB drive mounted at `/mnt/usb_backup/ha_backups`.

### 2. **Software Requirements**:
   - **Rclone**: Configured for Google Drive integration.
   - **Curl**: Required for Telegram notifications.
   - **Tar**: For compression.

### 3. **Configuration Files**:
   - Rclone configuration file located at `/home/redwannabil/.config/rclone/rclone.conf`.

### 4. **Permissions**:
   - Script requires `sudo` privileges for compression.

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. **Set Execution Permissions**:
   ```bash
   chmod +x ha_backup.sh
   ```

3. **Configure Telegram Credentials**:
   - Replace `REDACTED_BY_SYSADMIN` placeholders in the script with your actual `TOKEN` and `CHAT_ID`.

4. **Verify USB Mount**:
   - Ensure the USB drive is mounted at `/mnt/usb_backup/ha_backups`.

5. **Test Rclone**:
   - Verify `rclone` is configured correctly for Google Drive:
     ```bash
     rclone listremotes
     ```

---

## Usage
Run the script manually or schedule it using `cron` for automated backups.

### Manual Execution:
```bash
sudo ./ha_backup.sh
```

### Automating with Cron:
1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add the following line to schedule daily backups at 2:00 AM:
   ```bash
   0 2 * * * /path/to/ha_backup.sh
   ```

---

## Script Workflow
1. **Initialization**:
   - Logs the start of the backup process.
   - Ensures the USB backup directory exists.

2. **Compression**:
   - Compresses the HA directory into a `.tar.gz` file.
   - Saves the compressed file to the USB drive.

3. **Local Cleanup**:
   - Deletes local backups older than 7 days.

4. **Cloud Cleanup**:
   - Deletes cloud backups older than 1 day using `rclone`.

5. **Cloud Upload**:
   - Uploads the latest backup to Google Drive.

6. **Notifications**:
   - Sends a Telegram message indicating success or failure.

7. **Completion**:
   - Logs the completion of the backup process.

---

## Logs
- Logs are stored in `/home/redwannabil/ha_backup.log`.
- Includes timestamps for each operation and error messages for troubleshooting.

---

## Error Handling
- If compression fails:
  - Logs the error.
  - Sends a Telegram notification.
  - Exits the script with a non-zero status.

- If cloud upload fails:
  - Logs the error.
  - Sends a Telegram alert.

---

## Customization
### Modify Backup Retention Periods:
- **Local Backups**: Change the `-mtime +7` value in the `find` command to adjust the retention period.
- **Cloud Backups**: Change the `--min-age 1d` value in the `rclone delete` command.

### Telegram Notifications:
- Replace `TOKEN` and `CHAT_ID` with your actual credentials.

---

## Troubleshooting
### Common Issues:
1. **USB Drive Not Mounted**:
   - Ensure the USB drive is mounted at `/mnt/usb_backup/ha_backups`.

2. **Rclone Configuration**:
   - Verify `rclone.conf` is correctly set up for Google Drive.

3. **Permission Errors**:
   - Run the script with `sudo` if encountering permission issues.

4. **Telegram Notifications Not Sent**:
   - Verify `TOKEN` and `CHAT_ID` are correct.
   - Check internet connectivity.

### Debugging:
- Review the log file at `/home/redwannabil/ha_backup.log` for detailed error messages.

---

## Security Considerations
- **Token and Chat ID**:
  - Store Telegram credentials securely. Avoid hardcoding sensitive information in the script.
  
- **Rclone Configuration**:
  - Ensure `rclone.conf` is protected with appropriate file permissions.

---

## License
This script is licensed under the MIT License. See the LICENSE file for details.

---

## Author
Developed by [Your Name/Team].

For questions or support, contact [Your Email].