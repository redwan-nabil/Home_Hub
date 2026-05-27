# backup_wifi.sh

## 🚀 Release Notes

### Changes in the Updated Script:
1. **Enhanced Logging**:
   - Added timestamps to log messages for better debugging and monitoring.
   - Improved clarity of log messages to indicate the system's state transitions (e.g., "Fiber down!", "Fiber restored!").

2. **Adaptive Sleep Mechanism**:
   - Introduced a dynamic sleep interval (`SLEEP_TIME`) that adjusts based on the system's state:
     - **Fiber Active**: Relaxed 30-second interval for health checks.
     - **Fiber Down**: Faster 15-second interval to quickly detect fiber restoration.

3. **Code Cleanup**:
   - Improved readability and maintainability with better comments and structure.
   - Removed redundant or unnecessary operations.

---

## Overview

`backup_wifi.sh` is a power-efficient watchdog script designed for Raspberry Pi servers running on solar power. It monitors the primary fiber internet connection and automatically switches to a backup 4G modem with a Wi-Fi hotspot when the fiber connection fails. The script ensures minimal power consumption by dynamically managing the power state of the USB modem and Wi-Fi hotspot.

---

## Features

- **Primary Internet Monitoring**: Continuously pings a test IP (Google DNS: `8.8.8.8`) to verify the availability of the primary fiber connection.
- **Automatic Failover**: Activates a backup 4G modem and Wi-Fi hotspot when the primary connection is down.
- **Power Management**:
  - Turns off the USB modem and Wi-Fi hotspot when the primary connection is restored.
  - Uses `uhubctl` to physically cut power to the USB modem, conserving energy.
- **Adaptive Health Checks**: Adjusts the frequency of health checks based on the system's state to optimize performance and power usage.
- **Logging**: Provides clear and timestamped logs for debugging and monitoring.

---

## Prerequisites

1. **Hardware**:
   - Raspberry Pi with a USB-connected 4G modem.
   - TP-Link router or any router with a static IP configuration.
   - USB hub with power control support (compatible with `uhubctl`).

2. **Software**:
   - `uhubctl`: For managing USB power states.
   - `hostapd`: For managing the Wi-Fi hotspot.
   - `iproute2`: For managing network routes.

3. **Configuration**:
   - Ensure the main fiber connection is configured on interface `eth0`.
   - Set the correct USB hub and port numbers for the 4G modem in the script.

---

## Configuration

Modify the following variables in the script to match your setup:

```bash
MAIN_IF="eth0"               # Main Fiber Ethernet connection
ROUTER_IP="192.168.0.1"      # Main TP-Link Router IP
TEST_IP="8.8.8.8"            # Google DNS to test real internet
USB_HUB="2"                  # Your modem's target USB Hub
USB_PORT="1"                 # Your modem's target USB Port
```

---

## How It Works

1. **Startup**:
   - The script starts by disabling the Wi-Fi hotspot (`hostapd`) and cutting power to the USB modem to save energy.

2. **Health Check**:
   - The script pings the test IP (`8.8.8.8`) every 30 seconds to check the status of the primary fiber connection.

3. **Failover to Backup**:
   - If the primary connection is down:
     - The script performs a quick recheck to confirm the failure.
     - Powers on the USB modem using `uhubctl`.
     - Waits 45 seconds for the modem to boot and register on the cellular network.
     - Starts the Wi-Fi hotspot (`hostapd`) to provide internet access via the 4G modem.
     - Removes the default route through the fiber connection to ensure traffic is routed through the 4G modem.
     - Reduces the health check interval to 15 seconds to quickly detect when the fiber connection is restored.

4. **Restoration to Primary**:
   - If the primary connection is restored:
     - The script stops the Wi-Fi hotspot to save power.
     - Restores the default route through the fiber connection.
     - Cuts power to the USB modem using `uhubctl`.
     - Resets the health check interval to 30 seconds.

5. **Loop**:
   - The script runs indefinitely, continuously monitoring the primary connection and managing the backup system as needed.

---

## Usage

1. **Make the Script Executable**:
   ```bash
   chmod +x backup_wifi.sh
   ```

2. **Run the Script**:
   ```bash
   ./backup_wifi.sh
   ```

3. **Run on Boot**:
   - Add the script to your crontab or systemd service to ensure it starts automatically on boot.

---

## Logs

The script outputs logs to the console, including timestamps for key events:

- Fiber connection status (up or down).
- Actions taken (e.g., powering on/off the modem, starting/stopping the Wi-Fi hotspot).
- Sleep interval adjustments.

Example log output:
```
🚀 Ultimate Power-Saving Watchdog Started...
Mon Oct 30 10:00:00 UTC 2023: Fiber down! Dropping to fast check...
Mon Oct 30 10:00:03 UTC 2023: Fiber confirmed dead. Restoring 5V power to USB modem...
Waiting 45s for cellular network registration...
⚡ Emergency Network is fully ONLINE.
Mon Oct 30 10:01:00 UTC 2023: Fiber restored! Cleaning up emergency system...
🔒 Modem powered completely OFF. System running on Fiber.
```

---

## Troubleshooting

- **`uhubctl` Not Found**:
  - Install `uhubctl` using your package manager or from the [official repository](https://github.com/mvp/uhubctl).
  - Ensure your USB hub supports power control.

- **Wi-Fi Hotspot Issues**:
  - Verify that `hostapd` is installed and configured correctly.
  - Check the status of `hostapd` using:
    ```bash
    sudo systemctl status hostapd
    ```

- **Network Route Issues**:
  - Ensure the correct IP and interface are configured for the primary router (`ROUTER_IP` and `MAIN_IF`).

---

## License

This script is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

---

## Author

Developed by a Senior DevOps Engineer. For questions or support, feel free to reach out.