# 🚀 Release Notes

### Changes in `update_ssd_health.sh`:
1. **Improved Path Handling**:
   - Absolute paths are now used for critical binaries (`nvme`, `findmnt`, `lsblk`, `smartctl`) to ensure compatibility across environments and avoid dependency on `$PATH`.

2. **Enhanced Error Handling**:
   - Added checks to ensure that extracted values (`NVME_USED`, `SDA_HEALTH`) are valid numbers before proceeding with calculations or file writes.
   - Handles cases where the external CCTV SSD is disconnected by writing `0` to the health file.

3. **Refined NVMe Health Calculation**:
   - Extracts `percentage_used` directly using `cut` and `tr` for more robust parsing.

4. **Dynamic SSD Health Detection**:
   - Improved logic for detecting and handling the external CCTV SSD health using multiple potential SMART attributes (`Media_Wearout_Indicator`, `Wear_Leveling_Count`, `Percent_Lifetime_Remain`, `SSD_Life_Left`).

5. **Code Structure**:
   - Added clear section headers for better readability and maintainability.

---

# `update_ssd_health.sh`

## Overview
The `update_ssd_health.sh` script monitors the health of two SSDs:
1. **Main NVMe SSD (OS Drive)**: Tracks the health of the primary NVMe drive by calculating the remaining health percentage based on the `percentage_used` attribute.
2. **External CCTV SSD**: Monitors the health of an external SSD used for CCTV storage by dynamically detecting the drive and extracting relevant SMART attributes.

The script writes the health metrics to text files in the Home Assistant configuration directory for further monitoring and integration.

---

## Prerequisites
1. **Dependencies**:
   - `nvme-cli`: Required for querying NVMe drive health.
   - `smartmontools`: Required for querying SMART attributes of the external SSD.
   - `findmnt` and `lsblk`: For dynamic detection of the external SSD.

   Install dependencies using:
   ```bash
   sudo apt update
   sudo apt install nvme-cli smartmontools util-linux
   ```

2. **Permissions**:
   - The script uses `sudo` to access `nvme` and `smartctl`. Ensure the user running the script has appropriate `sudo` permissions.

3. **Mount Point**:
   - The external SSD must be mounted at `/mnt/cctv_ssd`.

---

## Installation
1. Place the script in the desired directory, e.g., `/usr/local/bin/update_ssd_health.sh`.
2. Make the script executable:
   ```bash
   chmod +x /usr/local/bin/update_ssd_health.sh
   ```
3. Schedule the script to run periodically using `cron` or a similar scheduler:
   ```bash
   crontab -e
   ```
   Add the following line to run the script every hour:
   ```bash
   0 * * * * /usr/local/bin/update_ssd_health.sh
   ```

---

## Script Details

### 1. Main NVMe Health (OS Drive)
- **Purpose**: Calculates the remaining health of the primary NVMe drive.
- **Logic**:
  - Extracts the `percentage_used` attribute using `nvme smart-log`.
  - Calculates the remaining health as `100 - percentage_used`.
  - Writes the result to `/home/redwannabil/homeassistant/nvme_health.txt`.

- **Error Handling**:
  - Ensures `percentage_used` is a valid number before performing calculations.

### 2. External CCTV SSD Health
- **Purpose**: Monitors the health of an external SSD used for CCTV storage.
- **Logic**:
  - Dynamically detects the base drive of the mounted SSD using `findmnt` and `lsblk`.
  - Extracts relevant SMART attributes (`Media_Wearout_Indicator`, `Wear_Leveling_Count`, `Percent_Lifetime_Remain`, or `SSD_Life_Left`) using `smartctl`.
  - Writes the health value to `/home/redwannabil/homeassistant/sda_health.txt`.

- **Error Handling**:
  - If the SSD is disconnected, writes `0` to indicate failure.

---

## Output
The script generates two files in the Home Assistant configuration directory:
1. `nvme_health.txt`: Contains the remaining health percentage of the NVMe drive.
2. `sda_health.txt`: Contains the health value of the external CCTV SSD or `0` if the drive is disconnected.

---

## Troubleshooting
1. **Permission Denied**:
   - Ensure the script is executable and the user has `sudo` permissions for `nvme` and `smartctl`.

2. **Incorrect Health Values**:
   - Verify that the dependencies (`nvme-cli`, `smartmontools`) are installed and functional.
   - Check the mount point `/mnt/cctv_ssd` and ensure the external SSD is properly connected.

3. **Script Fails to Run in Cron**:
   - Ensure the full path to the script is specified in the `crontab` entry.
   - Add the following line at the top of the script to load system paths:
     ```bash
     export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
     ```

---

## Future Improvements
- Add logging to capture script execution details and errors.
- Extend support for additional SSD health attributes.
- Implement email or notification alerts for critical health thresholds.