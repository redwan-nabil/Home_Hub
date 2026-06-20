# pi_telemetry.sh

## Overview

`pi_telemetry.sh` is a Bash script designed to continuously monitor and log telemetry data from a Raspberry Pi device. The script collects two key metrics:

1. **Fan Speed**: Reads the current speed of the cooling fan.
2. **Power Draw**: Calculates the power consumption of the Raspberry Pi using native Python math and the `vcgencmd` tool.

The script runs in an infinite loop, collecting data every 15 seconds and saving it to text files for further analysis or integration with other systems, such as Home Assistant.

---

## Features

- **Fan Speed Monitoring**: Reads the fan speed from the system hardware and logs it to a file.
- **Power Draw Calculation**: Uses Python to calculate the power draw based on current and voltage readings from the Raspberry Pi's PMIC (Power Management IC).
- **Continuous Monitoring**: Runs indefinitely, collecting data every 15 seconds.
- **Output to Files**: Saves the telemetry data to text files for easy access and integration.

---

## Prerequisites

### Hardware
- Raspberry Pi with a cooling fan connected.
- Raspberry Pi with PMIC support for power draw calculations.

### Software
- Bash shell (default on Raspberry Pi OS).
- Python 3 installed on the system.
- `vcgencmd` command-line tool (included with Raspberry Pi firmware).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Home_assistant
   ```

2. **Set Permissions**:
   Ensure the script has executable permissions:
   ```bash
   chmod +x pi_telemetry.sh
   ```

3. **Configure Output Directory**:
   By default, the script saves telemetry data to `/home/redwannabil/homeassistant/`. Ensure this directory exists or modify the script to use a different directory.

---

## Usage

To start the telemetry monitoring, run the script:

```bash
./pi_telemetry.sh
```

The script will begin collecting data and saving it to the following files:
- `fan_speed.txt`: Contains the current fan speed in RPM (or `0` if the fan is not detected).
- `power_draw.txt`: Contains the calculated power draw in watts.

---

## File Outputs

### `fan_speed.txt`
This file contains the current fan speed in RPM. If the fan is not detected, the value will be `0`.

Example:
```
1200
```

### `power_draw.txt`
This file contains the calculated power draw in watts, based on the current and voltage readings from the PMIC.

Example:
```
5.23
```

---

## Script Details

### Fan Speed Monitoring
The script reads the fan speed using the following command:
```bash
cat /sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input
```
If the fan is not detected, it defaults to `0`.

### Power Draw Calculation
The script uses Python to calculate the power draw. It reads current and voltage values from the PMIC using the `vcgencmd pmic_read_adc` command. The formula used for power calculation is:
```
Power (W) = Σ (Current * Voltage) * 1.1451 + 0.5879
```
This formula includes scaling and offset adjustments for accurate readings.

### Loop Interval
The script runs in an infinite loop, collecting data every 15 seconds using the `sleep 15` command.

---

## Troubleshooting

### Fan Speed Issues
- Ensure the cooling fan is properly connected to the Raspberry Pi.
- Verify the presence of the `/sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input` file.

### Power Draw Issues
- Ensure the `vcgencmd` tool is installed and accessible.
- Verify that your Raspberry Pi supports PMIC telemetry.

### Permission Errors
If you encounter permission errors, ensure the script has executable permissions:
```bash
chmod +x pi_telemetry.sh
```

---

## Customization

### Change Output Directory
To change the directory where telemetry data is saved, modify the paths in the script:
```bash
/home/redwannabil/homeassistant/fan_speed.txt
/home/redwannabil/homeassistant/power_draw.txt
```
Replace `/home/redwannabil/homeassistant/` with your desired directory.

### Adjust Loop Interval
To change the data collection interval, modify the `sleep` command:
```bash
sleep 15
```
Replace `15` with the desired number of seconds.

---

## Notes

- This script is designed to run indefinitely. To stop it, use `Ctrl+C` or terminate the process manually.
- Ensure your Raspberry Pi has sufficient permissions to access hardware telemetry files and execute the `vcgencmd` command.

---

## License

This script is provided under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute it as needed.

---

## Author

Developed by [Your Name]. For questions or support, please contact [Your Email].