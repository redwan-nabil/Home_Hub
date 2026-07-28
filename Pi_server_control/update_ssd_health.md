# 🚀 Release Notes

### Changes in `update_ssd_health.sh`:
1. **Improved Robustness**:
   - Added explicit checks to ensure that the extracted health metrics (`NVME_USED` and `SDA_HEALTH`) are valid numbers before proceeding with calculations or file updates.
   
2. **Code Cleanup**:
   - Removed redundant or unnecessary comments for clarity.
   - Ensured consistent use of absolute paths for all system binaries (`nvme`, `findmnt`, `lsblk`, `smartctl`) to prevent potential path resolution issues.

3. **Error Handling**:
   - Added a fallback mechanism to write `0` to the `sda_health.txt` file if the external SSD is disconnected or unavailable.

---

# `update_ssd_health.sh`

## Overview
The `update_ssd_health.sh` script is designed to monitor and log the health of two SSDs on a Raspberry Pi server:
1. **Main NVMe Drive**: The operating system drive.
2. **External CCTV SSD**: A USB-connected SSD used for CCTV storage.

The script retrieves health metrics for both drives and writes the results to respective files in the Home Assistant directory for further monitoring or integration.

---

## Features
- **NVMe Health Monitoring**: Calculates the remaining health of the main NVMe drive by subtracting the percentage used from 100.
- **External SSD Health Monitoring**: Retrieves the health status of an external SSD using SMART attributes.
- **Error Handling**: Detects if the external SSD is disconnected and logs a health value of `0` to indicate failure.
- **Path Robustness**: Ensures all system binaries are accessed using absolute paths to avoid issues with missing or incorrect `$PATH` configurations.

---

## File Outputs
The script generates the following output files:
1. `/home/redwannabil/homeassistant/nvme_health.txt`: Contains the remaining health percentage of the main NVMe drive.
2. `/home/redwannabil/homeassistant/sda_health.txt`: Contains the health percentage of the external SSD or `0` if the drive is disconnected.

---

## Prerequisites
1. **Dependencies**:
   - `nvme-cli`: For retrieving NVMe drive health metrics.
   - `smartmontools`: For retrieving SMART attributes of the external SSD.
   - `findmnt` and `lsblk`: For identifying the mounted external SSD.

2. **Permissions**:
   - The script requires `sudo` privileges to execute `nvme` and `smartctl` commands.

3. **Home Assistant Directory**:
   - Ensure the directory `/home/redwannabil/homeassistant/` exists and is writable by the script.

---

## Usage
1. Save the script as `update_ssd_health.sh`.
2. Make the script executable:
   ```bash
   chmod +x update_ssd_health.sh
   ```
3. Run the script manually or schedule it via `cron` for periodic execution:
   ```bash
   ./update_ssd_health.sh
   ```

---

## Script Logic
### 1. Main NVMe Health Monitoring
- The script uses the `nvme smart-log` command to retrieve the `percentage_used` attribute of the NVMe drive (`/dev/nvme0n1`).
- It calculates the remaining health as `100 - percentage_used`.
- If the extracted value is a valid number, it writes the result to `/home/redwannabil/homeassistant/nvme_health.txt`.

### 2. External SSD Health Monitoring
- The script identifies the mounted external SSD partition using `findmnt`.
- If the partition is found, it determines the parent device using `lsblk`.
- It retrieves the health status using `smartctl` by checking specific SMART attributes (e.g., `Media_Wearout_Indicator`, `Wear_Leveling_Count`, etc.).
- If the health value is valid, it writes the result to `/home/redwannabil/homeassistant/sda_health.txt`.
- If the external SSD is disconnected, it writes `0` to indicate failure.

---

## Example Output
- **NVMe Health**:
  - File: `/home/redwannabil/homeassistant/nvme_health.txt`
  - Content: `95` (indicating 95% health remaining)
- **External SSD Health**:
  - File: `/home/redwannabil/homeassistant/sda_health.txt`
  - Content: `80` (indicating 80% health remaining) or `0` (if disconnected)

---

## Troubleshooting
1. **Permission Denied**:
   - Ensure the script is executable and run with appropriate permissions:
     ```bash
     chmod +x update_ssd_health.sh
     sudo ./update_ssd_health.sh
     ```

2. **Missing Dependencies**:
   - Install required tools:
     ```bash
     sudo apt update
     sudo apt install nvme-cli smartmontools
     ```

3. **Incorrect File Paths**:
   - Verify the paths to the Home Assistant directory and SSD devices.

---

## Future Improvements
- Add logging for debugging purposes.
- Implement email or notification alerts for critical health thresholds.
- Extend support for additional SSDs or storage devices.