# backup_wifi.sh - Emergency Backup Wi-Fi Script for Pi Server Control

## Overview
`backup_wifi.sh` is a robust Bash script designed to ensure uninterrupted internet connectivity for Raspberry Pi servers in environments where power efficiency and reliability are critical. The script monitors the primary fiber internet connection and automatically switches to a backup cellular modem and Wi-Fi hotspot when the fiber connection fails. It also restores the primary connection when it becomes available, optimizing power usage by controlling USB power to the modem.

---

## Features
- **Automatic Internet Failover**: Monitors the primary fiber connection and switches to backup cellular internet when the fiber is down.
- **Power Efficiency**: Dynamically controls USB power to the cellular modem to conserve energy, ideal for solar-powered setups.
- **Adaptive Monitoring**: Adjusts the frequency of internet checks based on the current network status.
- **Wi-Fi Hotspot Management**: Activates and deactivates the RaspAP Wi-Fi hotspot as needed.
- **Real-Time Logging**: Provides timestamped logs for all major events, including connection status changes and system actions.

---

## Requirements
### Hardware
- Raspberry Pi with Raspbian OS.
- USB cellular modem (e.g., ZTE modem).
- USB hub with power control support (compatible with `uhubctl`).
- TP-Link router or similar device for primary fiber internet.

### Software
- `uhubctl`: For USB power control.
- `hostapd`: For managing the Wi-Fi hotspot.
- `ping`: For network connectivity checks.
- `systemctl`: For managing services.

---

## Configuration
The script uses the following configurable variables:

| Variable       | Description                                      | Default Value       |
|----------------|--------------------------------------------------|---------------------|
| `MAIN_IF`      | Network interface for primary fiber connection. | `eth0`              |
| `ROUTER_IP`    | IP address of the primary router.               | `192.168.0.1`       |
| `TEST_IP`      | IP address used for internet connectivity tests.| `8.8.8.8` (Google DNS) |
| `USB_HUB`      | Target USB hub number for the modem.            | `2`                 |
| `USB_PORT`     | Target USB port number for the modem.           | `1`                 |
| `SLEEP_TIME`   | Interval (in seconds) between connectivity checks.| `30` (adjusts dynamically) |

---

## Installation
1. **Install Required Packages**:
   Ensure the following packages are installed:
   ```bash
   sudo apt update
   sudo apt install uhubctl hostapd
   ```

2. **Place the Script**:
   Save the script as `backup_wifi.sh` in your desired directory (e.g., `/usr/local/bin/`).

3. **Make the Script Executable**:
   ```bash
   chmod +x /usr/local/bin/backup_wifi.sh
   ```

4. **Configure USB Hub and Port**:
   Verify the USB hub and port numbers for your modem using `uhubctl`:
   ```bash
   uhubctl
   ```
   Update the `USB_HUB` and `USB_PORT` variables in the script accordingly.

5. **Enable Hostapd**:
   Configure `hostapd` to manage the Wi-Fi hotspot. Refer to the [hostapd documentation](https://w1.fi/hostapd/) for setup instructions.

---

## Usage
Run the script manually or set it up as a systemd service for automatic execution on boot.

### Manual Execution
```bash
sudo /usr/local/bin/backup_wifi.sh
```

### Systemd Service
1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/backup_wifi.service
   ```
   Add the following content:
   ```ini
   [Unit]
   Description=Backup Wi-Fi Failover Script
   After=network.target

   [Service]
   ExecStart=/usr/local/bin/backup_wifi.sh
   Restart=always
   User=root

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable backup_wifi.service
   sudo systemctl start backup_wifi.service
   ```

---

## How It Works
1. **Startup**:
   - The script starts by ensuring the backup Wi-Fi hotspot is disabled and the USB modem is powered off to conserve energy.

2. **Monitoring**:
   - The script continuously pings `TEST_IP` (Google DNS) via the primary fiber connection (`MAIN_IF`) every 30 seconds.
   - If the ping fails, the script performs a secondary check after 3 seconds to confirm the fiber connection is down.

3. **Failover**:
   - If the fiber connection is confirmed down:
     - Powers on the USB modem.
     - Waits 45 seconds for the modem to boot and register on the cellular network.
     - Starts the `hostapd` service to enable the Wi-Fi hotspot.
     - Removes the default route via the fiber connection to route traffic through the cellular modem.

4. **Recovery**:
   - If the fiber connection is restored:
     - Stops the `hostapd` service to disable the Wi-Fi hotspot.
     - Restores the default route via the fiber connection.
     - Powers off the USB modem to conserve energy.

5. **Adaptive Sleep**:
   - The script adjusts the sleep interval based on the network status:
     - 30 seconds during normal operation.
     - 15 seconds during backup mode for faster recovery.

---

## Logging
The script logs key events with timestamps, including:
- Fiber connection status changes.
- Activation and deactivation of the backup system.
- Power state changes for the USB modem.

Logs are displayed in the terminal during execution.

---

## Troubleshooting
- **USB Power Control Issues**:
  Ensure your USB hub supports power control and is compatible with `uhubctl`. Test using:
  ```bash
  uhubctl -l <hub> -p <port> -a on
  ```

- **Hostapd Service Fails to Start**:
  Verify your `hostapd` configuration and ensure it is correctly set up for your Wi-Fi hotspot.

- **Incorrect Routing**:
  Check the default route using:
  ```bash
  ip route
  ```
  Ensure the route points to the correct gateway (`ROUTER_IP` for fiber, or cellular modem during backup).

---

## Notes
- This script is optimized for power-sensitive environments, such as solar-powered Raspberry Pi setups.
- Ensure proper configuration of the `hostapd` service and USB hub/port settings before running the script.
- Modify the `TEST_IP` variable if you prefer to use a different server for connectivity checks.

---

## License
This script is provided under the MIT License. Feel free to use, modify, and distribute it as needed.

---

## Author
Developed by the Pi Server Control team. For questions or support, please contact [support@example.com].