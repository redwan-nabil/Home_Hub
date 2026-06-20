# update_ssd_health.sh

## Overview
`update_ssd_health.sh` is a Bash script designed to monitor and report the health of two types of storage devices: an NVMe SSD and a secondary SSD used for CCTV storage. The script calculates the health metrics for these devices and writes the results to plain text files in the Home Assistant configuration folder. This allows Home Assistant to monitor and display the health status of the storage devices.

---

## Features
1. **NVMe SSD Health Calculation**:
   - Retrieves the `percentage_used` value from the NVMe device using `nvme smart-log`.
   - Calculates the health as `100 - percentage_used`.

2. **CCTV SSD Health Calculation**:
   - Dynamically detects the base drive associated with the `/mnt/cctv_ssd` mount point.
   - Uses `smartctl` to retrieve the `Available_Reservd_Space` attribute, which indicates the health of the SSD.

3. **Integration with Home Assistant**:
   - Outputs the health metrics as plain numbers into text files (`nvme_health.txt` and `sda_health.txt`) located in the Home Assistant configuration folder.

---

## Prerequisites
Before running the script, ensure the following dependencies are installed and configured:

1. **Tools**:
   - `nvme-cli`: Required for retrieving NVMe SSD health information.
   - `smartmontools`: Required for retrieving health information of non-NVMe SSDs.

2. **Permissions**:
   - The script requires `sudo` privileges to execute `nvme smart-log` and `smartctl` commands.
   - Ensure the user running the script has write access to the Home Assistant configuration folder.

3. **Mount Point**:
   - The secondary SSD must be mounted at `/mnt/cctv_ssd`.

---

## Installation
1. Place the script in a directory of your choice, e.g., `/usr/local/bin/update_ssd_health.sh`.
2. Make the script executable:
   ```bash
   chmod +x /usr/local/bin/update_ssd_health.sh
   ```

---

## Usage
Run the script manually or set it up as a cron job for periodic execution.

### Manual Execution
```bash
sudo /usr/local/bin/update_ssd_health.sh
```

### Automating with Cron
1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add an entry to execute the script periodically (e.g., every hour):
   ```bash
   0 * * * * sudo /usr/local/bin/update_ssd_health.sh
   ```

---

## Output
The script generates two output files in the Home Assistant configuration folder:
1. `nvme_health.txt`: Contains the health percentage of the NVMe SSD.
2. `sda_health.txt`: Contains the health percentage of the CCTV SSD.

Example:
- `/home/redwannabil/homeassistant/nvme_health.txt`:
  ```
  95
  ```
- `/home/redwannabil/homeassistant/sda_health.txt`:
  ```
  98
  ```

---

## Script Details

### 1. NVMe SSD Health Calculation
- Command: `sudo nvme smart-log /dev/nvme0n1`
- Extracts the `percentage_used` value, removes the `%` symbol, and calculates the health as `100 - percentage_used`.

### 2. CCTV SSD Health Calculation
- Dynamically identifies the base drive associated with `/mnt/cctv_ssd` using:
  - `findmnt -n -o SOURCE /mnt/cctv_ssd`
  - `lsblk -no pkname`
- Runs `smartctl` on the base drive to extract the `Available_Reservd_Space` attribute.

### 3. Writing Output
- Writes the calculated health values to:
  - `/home/redwannabil/homeassistant/nvme_health.txt`
  - `/home/redwannabil/homeassistant/sda_health.txt`

---

## Troubleshooting

### Common Issues
1. **Permission Denied**:
   - Ensure the script is executed with `sudo` or by a user with sufficient privileges.
   - Verify write permissions for the Home Assistant configuration folder.

2. **Missing Dependencies**:
   - Install `nvme-cli` and `smartmontools` using your package manager:
     ```bash
     sudo apt install nvme-cli smartmontools
     ```

3. **Incorrect Mount Point**:
   - Verify that the secondary SSD is mounted at `/mnt/cctv_ssd`:
     ```bash
     findmnt /mnt/cctv_ssd
     ```

4. **Dynamic Drive Detection Fails**:
   - Ensure the mount point `/mnt/cctv_ssd` exists and is properly configured.

---

## Notes
- The script assumes the NVMe device is located at `/dev/nvme0n1`. Update the script if your NVMe device uses a different path.
- The script dynamically detects the base drive for the CCTV SSD, ensuring compatibility with various system configurations.

---

## License
This script is provided "as-is" without any warranty. Use at your own risk.