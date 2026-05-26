# Nextcloud Watcher Script (`nextcloud_watcher.sh`)

## Overview

The `nextcloud_watcher.sh` script is a file monitoring and synchronization utility designed for Nextcloud deployments. It leverages `inotifywait` to monitor specific directories for file changes and automatically triggers Nextcloud's file scanning process to ensure that the Nextcloud file index remains up-to-date. This script is optimized for UTF-8 encoding and is designed to work seamlessly with Dockerized Nextcloud instances.

## Features

- **Real-Time File Monitoring**: Watches specified directories for file changes, including file creation, modifications, and moves.
- **Automatic Nextcloud Sync**: Automatically triggers Nextcloud's `files:scan` command to update the file index whenever changes are detected.
- **Multi-Watcher Support**: Supports multiple directory watchers with independent configurations.
- **Safety Exclusions**: Allows exclusion of specific files or directories from monitoring to prevent unnecessary processing.
- **UTF-8 Optimization**: Ensures compatibility with UTF-8 encoded file paths.

## Prerequisites

Before using this script, ensure the following prerequisites are met:

1. **Nextcloud Instance**: A running Nextcloud instance, preferably in a Docker container.
2. **Docker**: Docker must be installed and running on the host system.
3. **inotify-tools**: The `inotifywait` command must be available. Install it using your package manager:
   ```bash
   sudo apt-get install inotify-tools
   ```
4. **Permissions**: Ensure the script has execute permissions:
   ```bash
   chmod +x nextcloud_watcher.sh
   ```

## Script Details

### Watcher 1: CCTV SSD

- **Monitored Directory**: `/mnt/cctv_ssd/`
- **Excluded Patterns**: Files or directories matching `Camera1`, `cctv`, or `lost+found`.
- **Nextcloud Path**: `redwansdrive/files/cctv_ssd`
- **Trigger Events**: 
  - File creation
  - File move
  - File close after write

### Watcher 2: USB Backup Pendrive

- **Monitored Directory**: `/mnt/usb_backup/`
- **Nextcloud Path**: `redwansdrive/files/usb_backup`
- **Trigger Events**: 
  - File creation
  - File move
  - File close after write

### Master Script Behavior

The script runs both watchers in the background and uses the `wait` command to keep the master process alive indefinitely.

## Usage

1. **Edit the Script**: Update the paths and Nextcloud configurations as needed:
   - Replace `/mnt/cctv_ssd/` and `/mnt/usb_backup/` with the directories you want to monitor.
   - Replace `redwansdrive/files/cctv_ssd` and `redwansdrive/files/usb_backup` with the corresponding Nextcloud paths.

2. **Run the Script**:
   ```bash
   ./nextcloud_watcher.sh
   ```

3. **Stop the Script**:
   Use `Ctrl+C` to terminate the script.

## Example Output

When a file change is detected, the script outputs messages similar to the following:

```
Starting Nexus Hub Unified File Watcher (UTF-8 Optimized)...
[CCTV SSD] Change detected: example_file.mp4. Syncing...
[USB BACKUP] Change detected: backup_file.zip. Syncing...
```

## Customization

- **Exclusions**: Modify the `--exclude` parameter in Watcher 1 to add or remove patterns for files/directories you want to ignore.
- **Additional Watchers**: Add more `inotifywait` watchers by copying and modifying the existing watcher blocks.
- **Docker Container Name**: Update `nextcloud-app-1` with the name of your Nextcloud Docker container.

## Troubleshooting

- **`inotifywait` Not Found**: Ensure `inotify-tools` is installed.
- **Permission Denied**: Run the script with appropriate permissions or as a user with access to the monitored directories.
- **Docker Command Fails**: Verify the Docker container name and ensure the container is running.

## Notes

- This script is designed for environments where Nextcloud is running in a Docker container. For non-Dockerized setups, modify the `docker exec` commands accordingly.
- The script runs indefinitely. Consider using a process manager like `systemd` or `supervisord` to manage its lifecycle in production environments.

## License

This script is provided under the MIT License. Feel free to modify and distribute it as needed.