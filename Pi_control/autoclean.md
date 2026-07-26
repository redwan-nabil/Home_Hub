# autoclean.sh - Raspberry Pi Auto-Clean Script

## Overview
`autoclean.sh` is a maintenance script designed to optimize the performance and storage usage of a Raspberry Pi by performing routine cleanup tasks. The script is intended to run nightly and automates the removal of unnecessary files, logs, and unused Docker resources.

## Features
The script performs the following tasks:
1. **APT Package Cache Cleanup**:
   - Removes unnecessary packages and clears the APT cache to free up disk space.
2. **System Logs Management**:
   - Retains only the last 3 days of system logs and deletes older logs to reduce clutter.
3. **Docker Cleanup**:
   - Purges all unused Docker images, containers, and networks to reclaim storage.
4. **User Cache Cleanup**:
   - Clears the local cache for the user `redwannabil`.

## Prerequisites
- The script requires `sudo` privileges to execute certain commands (e.g., APT cleanup, log management).
- Docker must be installed if the Docker cleanup step is to be executed.
- The script assumes the username `redwannabil` for clearing the user cache. Update the script if a different username is used.

## Usage
1. **Manual Execution**:
   - Run the script manually using the following command:
     ```bash
     sudo ./autoclean.sh
     ```
   - Ensure the script has executable permissions:
     ```bash
     chmod +x autoclean.sh
     ```

2. **Automated Execution**:
   - Schedule the script to run nightly using `cron`:
     ```bash
     sudo crontab -e
     ```
   - Add the following line to schedule the script to run at 2:00 AM daily:
     ```bash
     0 2 * * * /path/to/autoclean.sh
     ```

## Script Breakdown
### 1. APT Package Cache Cleanup
```bash
apt autoremove -y
apt clean
```
- `apt autoremove -y`: Removes unnecessary packages that were automatically installed and are no longer required.
- `apt clean`: Clears the local repository of retrieved package files.

### 2. System Logs Management
```bash
journalctl --vacuum-time=3d
```
- Retains only the last 3 days of system logs and deletes older logs to free up disk space.

### 3. Docker Cleanup
```bash
docker system prune -a -f
```
- Removes all unused Docker images, containers, volumes, and networks.
- `-a`: Removes all unused images, not just dangling ones.
- `-f`: Forces the cleanup without prompting for confirmation.

### 4. User Cache Cleanup
```bash
rm -rf /home/redwannabil/.cache/*
```
- Deletes all files in the `.cache` directory of the user `redwannabil`.

### 5. Completion Message
```bash
echo "Cleanup completed on $(date)"
```
- Prints a timestamped message indicating the cleanup process has finished.

## Notes
- **User-Specific Cache**: If the script is used for a different user, update the path `/home/redwannabil/.cache/*` to the appropriate user's home directory.
- **Docker Dependency**: If Docker is not installed, the Docker cleanup step will fail. You can safely comment out or remove this section if Docker is not used on the system.
- **System Logs**: Adjust the `--vacuum-time` parameter if you want to retain logs for a different duration.

## Troubleshooting
- **Permission Denied**: Ensure the script is executed with `sudo` privileges.
- **Docker Errors**: Verify that Docker is installed and running if the Docker cleanup step fails.
- **User Cache Path**: Double-check the username and path for the user cache cleanup step.

## Disclaimer
Use this script with caution, as it performs irreversible cleanup operations. Test the script in a controlled environment before deploying it on a production system.