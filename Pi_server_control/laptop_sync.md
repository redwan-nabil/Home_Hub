# Laptop Sync Script (`laptop_sync.sh`) - v4.5

## Overview

The `laptop_sync.sh` script is a robust, asynchronous backup synchronization tool designed to transfer backup files from a Raspberry Pi server to a designated laptop. It incorporates advanced features such as mutex locking, CPU load-aware synchronization, and Telegram notifications to ensure reliable and efficient operation.

---

## Features

1. **Mutex Locking**: Prevents duplicate script executions by using a lock file mechanism.
2. **Telegram Notifications**: Sends real-time updates about the sync process to a configured Telegram chat.
3. **CPU Governor**: Dynamically pauses and resumes the `rsync` process based on system load and Docker activity to ensure system stability.
4. **Backup Tracking**: Ensures that only new or updated backups are synchronized, avoiding redundant transfers.
5. **Laptop Connectivity Check**: Verifies the availability of the target laptop before initiating the sync process.
6. **Error Handling**: Handles specific `rsync` exit codes (e.g., code 24 for vanished files) to ensure smooth operation.
7. **Automated Cleanup**: Deletes old backup files on the laptop to free up space.
8. **Bandwidth Limiting**: Limits the bandwidth usage of `rsync` to avoid network congestion.

---

## Prerequisites

1. **Dependencies**:
   - `rsync`
   - `curl`
   - `nc` (Netcat)
   - `flock`
   - `mount.cifs` (for CIFS/SMB mounting)

2. **Configuration**:
   - Ensure the target laptop has an SMB share configured and accessible.
   - Update the script with the correct SMB credentials and share name.
   - Configure Telegram Bot API token and chat ID for notifications.

3. **Permissions**:
   - The script requires `sudo` privileges for certain operations (e.g., mounting, file deletion).

---

## Script Workflow

### 1. **Mutex Lock**
- Prevents multiple instances of the script from running simultaneously by creating a lock file (`/tmp/laptop_sync.lock`).

### 2. **Identify the Latest Backup**
- Searches the USB backup directory (`/mnt/usb_backup/server_backup`) for the most recent backup file (`*.img.gz` or `*.tar.gz`).

### 3. **Check Backup Sync Status**
- Compares the timestamp of the latest backup file with a tracking file (`.last_sync_time`) to determine if synchronization is required.

### 4. **Laptop Connectivity Check**
- Iterates through a list of predefined laptop IPs (`LAPTOP_IPS`) to find an online laptop with an active SMB share.

### 5. **Telegram Notification**
- Sends a notification to the configured Telegram chat when the sync process starts.

### 6. **CPU Governor**
- Monitors system load and Docker activity:
  - Pauses `rsync` if the load exceeds 3.0 or if Docker is actively running resource-intensive commands.
  - Resumes `rsync` when the load drops below 1.5 and Docker activity subsides.

### 7. **Mount SMB Share**
- Mounts the laptop's SMB share to a local mount point (`/mnt/laptop_sync`).

### 8. **Synchronize Backups**
- Uses `rsync` to transfer files from the USB backup directory to the laptop's SMB share.
- Limits bandwidth usage to 3 MB/s (`--bwlimit=3000`).
- Logs the sync process to `/home/redwannabil/laptop_sync.log`.

### 9. **Post-Sync Cleanup**
- Deletes backup files older than 3 days from specific directories on the laptop:
  - `RPI_OS_backup`
  - `HA_Backup`
  - `Nextcloud_Admin_backup`

### 10. **Unmount SMB Share**
- Unmounts the SMB share after the sync process is complete.

### 11. **Telegram Notification**
- Sends a success or error notification to the configured Telegram chat based on the sync status.

---

## Configuration

### 1. **Script Variables**
- `LOGFILE`: Path to the log file.
- `BASE_USB_DIR`: Directory containing backup files on the Raspberry Pi.
- `MOUNT_PT`: Mount point for the laptop's SMB share.
- `TRACKING_FILE`: File used to track the last synced backup.

### 2. **Telegram Settings**
- `TOKEN`: Telegram Bot API token (replace `REDACTED_BY_SYSADMIN` with your token).
- `CHAT_ID`: Telegram chat ID (replace `REDACTED_BY_SYSADMIN` with your chat ID).

### 3. **Laptop Settings**
- `LAPTOP_IPS`: List of potential laptop IP addresses.
- `SMB_USER`: SMB username for authentication.
- `SMB_PASS`: SMB password for authentication (replace `REDACTED_BY_SYSADMIN` with your password).
- `SHARE_NAME`: Name of the SMB share on the laptop.

---

## Usage

1. Place the script in a directory with execute permissions.
2. Update the configuration variables as needed.
3. Run the script manually or schedule it using `cron` for automated execution.

Example `cron` entry to run the script every hour:
```
0 * * * * /path/to/laptop_sync.sh
```

---

## Logging

- All sync operations and errors are logged to `/home/redwannabil/laptop_sync.log`.

---

## Error Handling

- **Exit Code 24**: Handled as a non-critical error (vanished files during sync).
- **Other Errors**: Sends a Telegram notification with the error code and logs the issue.

---

## Security Considerations

1. **Sensitive Information**:
   - Ensure that sensitive information (e.g., SMB credentials, Telegram token) is properly secured and not exposed in public repositories.
   - Use environment variables or a secure secrets management solution if possible.

2. **Permissions**:
   - Restrict access to the script and log files to authorized users only.

---

## Future Improvements

1. Add support for encrypted backups.
2. Implement retry logic for failed sync attempts.
3. Enhance logging with more detailed error messages.

---

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk. Ensure proper testing in a controlled environment before deploying in production.