# 🚀 Release Notes

### Changes in `nextcloud_watcher.sh`:
1. **No functional changes**: The new code is identical to the old code. No updates or modifications have been made to the script.

---

# Nextcloud File Watcher Script

This script, `nextcloud_watcher.sh`, is designed to monitor specific directories for file changes and synchronize them with a Nextcloud instance. It uses the `inotifywait` tool to detect file system events and triggers Nextcloud's `occ files:scan` command to update the file index.

## Features
- **Real-time File Monitoring**: Watches specified directories for changes such as file creation, modification, or movement.
- **Directory Exclusions**: Allows exclusion of specific files or directories from being monitored.
- **Nextcloud Integration**: Automatically updates the Nextcloud file index when changes are detected.
- **Multi-directory Support**: Monitors multiple directories simultaneously.

## Prerequisites
1. **Nextcloud Setup**: Ensure you have a running Nextcloud instance with the `occ` command available.
2. **Docker**: The script assumes that Nextcloud is running in a Docker container named `nextcloud-app-1`.
3. **inotify-tools**: The script relies on the `inotifywait` command, which is part of the `inotify-tools` package. Install it using your package manager:
   ```bash
   sudo apt-get install inotify-tools
   ```
4. **Permissions**: Ensure the script has execute permissions:
   ```bash
   chmod +x nextcloud_watcher.sh
   ```

## Usage
1. **Start the Script**:
   Run the script to start monitoring the specified directories:
   ```bash
   ./nextcloud_watcher.sh
   ```

2. **Monitored Directories**:
   - `/mnt/cctv_ssd/`: Watches for changes while excluding files or directories matching `(Camera1|cctv|lost+found)`.
   - `/mnt/usb_backup/`: Watches for all changes in this directory.

3. **File Events Monitored**:
   - `close_write`: Triggered when a file is closed after being written to.
   - `moved_to`: Triggered when a file is moved into the directory.
   - `create`: Triggered when a new file is created.

4. **Nextcloud Synchronization**:
   - For `/mnt/cctv_ssd/`, changes are synced to `redwansdrive/files/cctv_ssd` in Nextcloud.
   - For `/mnt/usb_backup/`, changes are synced to `redwansdrive/files/usb_backup` in Nextcloud.

## Script Details
### Watcher 1: CCTV SSD
- Monitors `/mnt/cctv_ssd/` for file changes.
- Excludes files or directories matching the regex `(Camera1|cctv|lost+found)`.
- On detecting a change, it triggers the following Nextcloud command:
  ```bash
  docker exec -e LANG=C.UTF-8 -u www-data nextcloud-app-1 php occ files:scan --path="redwansdrive/files/cctv_ssd"
  ```

### Watcher 2: USB Backup Pendrive
- Monitors `/mnt/usb_backup/` for file changes.
- On detecting a change, it triggers the following Nextcloud command:
  ```bash
  docker exec -e LANG=C.UTF-8 -u www-data nextcloud-app-1 php occ files:scan --path="redwansdrive/files/usb_backup"
  ```

### Script Lifecycle
- The script runs indefinitely, keeping the watchers active.
- The `wait` command at the end ensures the script does not terminate prematurely.

## Troubleshooting
- **`inotifywait: command not found`**: Ensure `inotify-tools` is installed.
- **Permission Denied**: Ensure the script has execute permissions and the user has access to the monitored directories.
- **Docker Errors**: Verify that the Docker container name (`nextcloud-app-1`) matches your Nextcloud container's name.
- **Nextcloud Errors**: Ensure the paths specified in the `occ files:scan` commands exist in your Nextcloud instance.

## Customization
- **Modify Monitored Directories**: Update the paths `/mnt/cctv_ssd/` and `/mnt/usb_backup/` to match your desired directories.
- **Adjust Exclusions**: Edit the `--exclude` regex in Watcher 1 to exclude additional files or directories.
- **Change Nextcloud Paths**: Update the `--path` argument in the `occ files:scan` commands to match your Nextcloud directory structure.

## Notes
- This script is designed to run continuously. Consider running it as a background process or using a process manager like `systemd` or `screen` for persistent monitoring.
- Ensure that the monitored directories are mounted and accessible before starting the script.

## License
This script is provided under the MIT License. Feel free to modify and distribute it as needed.