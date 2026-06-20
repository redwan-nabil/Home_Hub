# Pi Telemetry Script (`pi_telemetry.sh`)

## Overview

The `pi_telemetry.sh` script is a telemetry monitoring tool designed for Raspberry Pi systems. It continuously collects and logs key hardware metrics, such as fan speed and power draw, at regular intervals. The script is intended to provide real-time data for monitoring and analysis, and it outputs the collected data to specific files for further use (e.g., integration with Home Assistant or other monitoring tools).

---

## Features

1. **Fan Speed Monitoring**:
   - Reads the current fan speed from the system's hardware monitoring interface (`/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input`).
   - If the fan speed cannot be read, it defaults to `0`.
   - Outputs the fan speed (in RPM) to the file:  
     `/home/redwannabil/homeassistant/fan_speed.txt`.

2. **Power Draw Calculation**:
   - Uses the `vcgencmd pmic_read_adc` command to retrieve power-related metrics (voltage and current) from the Raspberry Pi's PMIC (Power Management Integrated Circuit).
   - Performs calculations in Python to compute the total power draw in watts:
     - Multiplies corresponding voltage and current values for each channel.
     - Applies a correction factor (`1.1451`) and adds an offset (`0.5879`) for accuracy.
   - Outputs the calculated power draw (in watts) to the file:  
     `/home/redwannabil/homeassistant/power_draw.txt`.

3. **Continuous Monitoring**:
   - The script runs indefinitely in a `while` loop.
   - Data is collected and updated every 15 seconds.

---

## Requirements

### Hardware
- A Raspberry Pi with a compatible cooling fan and PMIC that supports telemetry via `vcgencmd`.

### Software
- **Bash**: The script is written in Bash and requires a Unix-like environment to run.
- **Python 3**: Used for power draw calculations.
- **vcgencmd**: A command-line utility for Raspberry Pi-specific hardware monitoring. Ensure it is installed and accessible.

---

## Installation

1. **Clone the Repository**:
   Clone the `Pi_server_control` repository to your Raspberry Pi.

   ```bash
   git clone <repository_url>
   cd Pi_server_control
   ```

2. **Set Permissions**:
   Ensure the script has executable permissions.

   ```bash
   chmod +x pi_telemetry.sh
   ```

3. **Verify Dependencies**:
   - Ensure Python 3 is installed:
     ```bash
     python3 --version
     ```
   - Ensure `vcgencmd` is installed and accessible:
     ```bash
     vcgencmd version
     ```

4. **Run the Script**:
   Execute the script to start monitoring.

   ```bash
   ./pi_telemetry.sh
   ```

---

## Output Files

The script generates and updates the following files every 15 seconds:

1. **Fan Speed**:
   - File: `/home/redwannabil/homeassistant/fan_speed.txt`
   - Content: Current fan speed in RPM. If the fan speed cannot be read, the value will be `0`.

2. **Power Draw**:
   - File: `/home/redwannabil/homeassistant/power_draw.txt`
   - Content: Current power draw in watts, calculated using voltage and current readings from the PMIC.

---

## Customization

1. **Output File Paths**:
   - Modify the paths for `fan_speed.txt` and `power_draw.txt` in the script to change where the output files are saved.

2. **Monitoring Interval**:
   - The default interval for data collection is 15 seconds. To change this, modify the `sleep 15` line in the script to your desired interval (in seconds).

---

## Troubleshooting

1. **Permission Denied**:
   - Ensure the script has executable permissions:
     ```bash
     chmod +x pi_telemetry.sh
     ```

2. **Missing `vcgencmd`**:
   - Install the `vcgencmd` utility by installing the `raspi-config` package:
     ```bash
     sudo apt update
     sudo apt install raspi-config
     ```

3. **Python Errors**:
   - Ensure Python 3 is installed and accessible via the `python3` command.

4. **Fan Speed Always `0`**:
   - Verify that your Raspberry Pi has a compatible cooling fan and that the fan's speed can be read from `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input`.

5. **Power Draw Not Calculated**:
   - Ensure the `vcgencmd` command is working correctly and returning PMIC data:
     ```bash
     vcgencmd pmic_read_adc
     ```

---

## Notes

- This script is designed to run indefinitely. To stop it, use `Ctrl+C` or terminate the process manually.
- Ensure that the output directory (`/home/redwannabil/homeassistant/`) exists and is writable by the user running the script.
- The power draw calculation includes a correction factor and offset, which may need adjustment based on your specific hardware setup.

---

## License

This script is part of the `Pi_server_control` project. Refer to the repository's license for usage and distribution terms.