# Pi_server_control: autoclean.sh

## Overview

`autoclean.sh` is a maintenance script designed for Raspberry Pi servers to automate the cleanup of unnecessary files, logs, and Docker resources. This script is intended to run nightly, ensuring the system remains optimized, with minimal disk space usage and improved performance.

---

## Features

The script performs the following tasks:

1. **APT Package Cache Cleanup**:
   - Removes unused packages and dependencies.
   - Clears the APT cache to free up disk space.

2. **System Log Management**:
   - Retains only the last 3 days of system logs.
   - Deletes older logs to prevent excessive disk usage.

3. **Docker Cleanup**:
   - Removes unused Docker images, containers, volumes, and networks.
   - Ensures that only active Docker resources are retained.

4. **User Cache Cleanup**:
   - Deletes all files in the local user's cache directory (`~/.cache`).

5. **Completion Notification**:
   - Outputs a message with the current date and time upon successful execution.

---

## Prerequisites

Before using the script, ensure the following:

- The script is executed with **root privileges** (e.g., via `sudo`) to allow access to system-level operations.
- Docker is installed and configured on the Raspberry Pi if Docker cleanup is required.
- The user running the script has write permissions to the `/home/<username>/.cache` directory.

---

## Installation

1. Clone the `Pi_server_control` repository:
   ```bash
   git clone <repository_url>
   cd Pi_server_control
   ```

2. Make the script executable:
   ```bash
   chmod +x autoclean.sh
   ```

3. (Optional) Schedule the script to run nightly using `cron`:
   - Open the crontab editor:
     ```bash
     crontab -e
     ```
   - Add the following line to schedule the script to run at 2:00 AM daily:
     ```bash
     0 2 * * * /path/to/Pi_server_control/autoclean.sh >> /var/log/autoclean.log 2>&1
     ```

---

## Usage

To run the script manually, execute the following command:

```bash
sudo ./autoclean.sh
```

---

## Script Breakdown

### 1. APT Package Cache Cleanup
```bash
apt autoremove -y
apt clean
```
- `apt autoremove -y`: Removes unnecessary packages and dependencies.
- `apt clean`: Clears the local repository of retrieved package files.

### 2. System Log Management
```bash
journalctl --vacuum-time=3d
```
- Retains only the last 3 days of system logs.
- Deletes older logs to free up disk space.

### 3. Docker Cleanup
```bash
docker system prune -a -f
```
- Removes all unused Docker objects, including:
  - Stopped containers.
  - Unused images.
  - Unused networks.
  - Unused volumes.

### 4. User Cache Cleanup
```bash
rm -rf /home/redwannabil/.cache/*
```
- Deletes all files in the specified user's cache directory.
- Replace `redwannabil` with the appropriate username if needed.

### 5. Completion Notification
```bash
echo "Cleanup completed on $(date)"
```
- Outputs a message indicating the script has completed execution, along with the current date and time.

---

## Notes

- **Caution**: The script performs destructive operations (e.g., deleting files, purging Docker resources). Ensure you understand the implications before running it.
- **Custom User Cache Path**: If the script is used by a different user, update the cache directory path (`/home/redwannabil/.cache/*`) to match the target user's home directory.
- **Docker Dependency**: If Docker is not installed or used, the Docker cleanup section can be commented out or removed.

---

## Troubleshooting

- **Permission Denied**: Ensure the script is run with `sudo` or as the root user.
- **Docker Errors**: Verify that Docker is installed and running on the system.
- **Custom Log Retention**: Modify the `--vacuum-time=3d` parameter to adjust the number of days of logs to retain.

---

## License

This script is part of the `Pi_server_control` project and is licensed under the MIT License. See the repository's LICENSE file for more details.

---

## Author

Developed by the `Pi_server_control` team. For support or inquiries, please contact the repository maintainers.