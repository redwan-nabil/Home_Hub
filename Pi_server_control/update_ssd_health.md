# `update_ssd_health.sh` - SSD Health Monitoring Script

## Overview

The `update_ssd_health.sh` script is designed to monitor and report the health of two SSDs on a Raspberry Pi server. It calculates the health of an NVMe SSD and a secondary SSD (used for CCTV storage) and writes the health metrics to files in a specified directory. These files can then be used by other applications, such as Home Assistant, for further processing or monitoring.

---

## Features

1. **NVMe SSD Health Calculation**:
   - Retrieves the `percentage_used` value from the NVMe SSD's SMART data.
   - Calculates the health as `100 - percentage_used`.
   - Outputs the health value to a file.

2. **CCTV SSD Health Calculation**:
   - Dynamically detects the base drive associated with the `/mnt/cctv_ssd` mount point.
   - Extracts the `Available_Reservd_Space` attribute from the SMART data of the detected drive.
   - Outputs the health value to a file.

3. **Integration with Home Assistant**:
   - Writes the health metrics to text files in the Home Assistant configuration directory for easy integration.

---

## Prerequisites

1. **Dependencies**:
   - `nvme-cli`: Required for retrieving SMART data from the NVMe SSD.
   - `smartmontools`: Required for retrieving SMART data from the secondary SSD.
   - `findmnt`: Used to determine the mount point of the CCTV SSD.
   - `lsblk`: Used to identify the base drive of the CCTV SSD.

2. **Permissions**:
   - The script requires `sudo` privileges to access SMART data for both SSDs.

3. **Directory Structure**:
   - The script assumes the following directory structure:
     - NVMe SSD: `/dev/nvme0n1`
     - CCTV SSD mount point: `/mnt/cctv_ssd`
     - Home Assistant configuration directory: `/home/redwannabil/homeassistant/`

---

## Installation

1. **Clone the Repository**:
   Clone the `Pi_server_control` repository to your Raspberry Pi server.

   ```bash
   git clone <repository_url>
   cd Pi_server_control
   ```

2. **Make the Script Executable**:
   Ensure the script has executable permissions.

   ```bash
   chmod +x update_ssd_health.sh
   ```

3. **Install Required Packages**:
   Install the necessary dependencies.

   ```bash
   sudo apt update
   sudo apt install nvme-cli smartmontools
   ```

---

## Usage

Run the script manually or schedule it to run periodically using a cron job.

### Manual Execution

```bash
sudo ./update_ssd_health.sh
```

### Automating with Cron

1. Edit the crontab file:

   ```bash
   crontab -e
   ```

2. Add an entry to run the script at a desired interval (e.g., every hour):

   ```bash
   0 * * * * /path/to/update_ssd_health.sh
   ```

---

## Output

The script generates two output files in the Home Assistant configuration directory:

1. **NVMe SSD Health**:
   - File: `/home/redwannabil/homeassistant/nvme_health.txt`
   - Content: A single integer representing the health percentage of the NVMe SSD.

2. **CCTV SSD Health**:
   - File: `/home/redwannabil/homeassistant/sda_health.txt`
   - Content: A single integer representing the health percentage of the CCTV SSD.

---

## Troubleshooting

1. **Permission Denied**:
   - Ensure the script is executed with `sudo` to access SMART data.

2. **Missing Dependencies**:
   - Verify that `nvme-cli` and `smartmontools` are installed.

   ```bash
   sudo apt install nvme-cli smartmontools
   ```

3. **Incorrect Mount Point**:
   - Ensure that the CCTV SSD is mounted at `/mnt/cctv_ssd`. Update the script if the mount point is different.

4. **SMART Data Not Available**:
   - Verify that SMART is enabled for the drives. Use the following commands to check:
     - For NVMe SSD: `sudo nvme smart-log /dev/nvme0n1`
     - For CCTV SSD: `sudo smartctl -A /dev/<device_name>`

---

## Notes

- The script assumes that the NVMe SSD is located at `/dev/nvme0n1`. If your NVMe SSD is located at a different path, update the script accordingly.
- The script dynamically detects the base drive for the CCTV SSD using the `/mnt/cctv_ssd` mount point. Ensure this mount point is correctly configured on your system.
- The `Available_Reservd_Space` attribute is used as a proxy for the health of the CCTV SSD. This may vary depending on the SSD model and manufacturer.

---

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk. Always back up your data before running scripts that interact with your storage devices.