# `backup_wifi.sh` Script Documentation

## Overview
The `backup_wifi.sh` script is designed to provide a robust failover mechanism for a Raspberry Pi server setup. It ensures uninterrupted internet connectivity by monitoring the primary fiber connection and activating a backup cellular modem with a Wi-Fi hotspot when the primary connection fails. The script is optimized for power-saving, making it ideal for solar-powered setups or environments where energy efficiency is critical.

---

## Features
- **Primary Internet Monitoring**: Continuously monitors the primary fiber connection via Ethernet (`eth0`).
- **Automatic Failover**: Activates a backup cellular modem and Wi-Fi hotspot when the primary connection is unavailable.
- **Power Management**: Automatically powers off the USB modem when the primary connection is restored to conserve energy.
- **Adaptive Monitoring**: Adjusts the monitoring frequency based on the current network status (normal or backup mode).
- **Safety Startup**: Ensures the backup system is powered off during script initialization to save energy.

---

## Prerequisites
Before using the script, ensure the following:
1. **Hardware Requirements**:
   - Raspberry Pi with a USB hub supporting power control (e.g., uhubctl-compatible hub).
   - USB cellular modem (e.g., ZTE modem) connected to the specified USB hub and port.
   - TP-Link router or similar device for primary fiber connection.
   - Solar power setup (optional).

2. **Software Requirements**:
   - `uhubctl`: For USB power control.
   - `hostapd`: For managing the Wi-Fi hotspot.
   - Proper configuration of the Raspberry Pi's network interfaces and routing.

3. **Configuration**:
   - Update the script variables to match your setup:
     - `MAIN_IF`: Name of the primary Ethernet interface (e.g., `eth0`).
     - `ROUTER_IP`: IP address of the primary router (e.g., `192.168.0.1`).
     - `TEST_IP`: IP address to ping for internet connectivity checks (e.g., `8.8.8.8`).
     - `USB_HUB`: USB hub number where the modem is connected.
     - `USB_PORT`: USB port number where the modem is connected.

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. **Place the Script**:
   Ensure `backup_wifi.sh` is located in the appropriate directory within the repository.

3. **Set Permissions**:
   Make the script executable:
   ```bash
   chmod +x backup_wifi.sh
   ```

4. **Install Dependencies**:
   Install required packages:
   ```bash
   sudo apt update
   sudo apt install uhubctl hostapd -y
   ```

5. **Configure Network**:
   - Ensure the primary Ethernet interface (`eth0`) is properly configured.
   - Set up `hostapd` for Wi-Fi hotspot functionality.

---

## Usage
Run the script using the following command:
```bash
sudo ./backup_wifi.sh
```

The script will:
1. Start by ensuring the backup Wi-Fi and USB modem are powered off.
2. Continuously monitor the primary fiber connection.
3. Activate the backup system if the primary connection fails.
4. Restore the primary connection and deactivate the backup system when the fiber connection is restored.

---

## Configuration Details
### Script Variables
- `MAIN_IF`: The name of the primary Ethernet interface (default: `eth0`).
- `ROUTER_IP`: IP address of the primary router (default: `192.168.0.1`).
- `TEST_IP`: IP address used for internet connectivity checks (default: `8.8.8.8`).
- `USB_HUB`: USB hub number where the modem is connected (default: `2`).
- `USB_PORT`: USB port number where the modem is connected (default: `1`).

### Power Management
- The script uses `uhubctl` to control USB power for the modem, ensuring energy efficiency.
- The modem is powered off when the primary connection is active and powered on only when the backup system is needed.

---

## Logs and Output
The script provides real-time logs for key events:
- Fiber connection status.
- Activation and deactivation of the backup system.
- USB power control actions.
- Adaptive sleep intervals.

Example log output:
```
🚀 Ultimate Power-Saving Watchdog Started...
Wed Oct 11 12:00:00 UTC 2023: Fiber down! Dropping to fast check...
Wed Oct 11 12:00:03 UTC 2023: Fiber confirmed dead. Restoring 5V power to USB modem...
Waiting 45s for cellular network registration...
⚡ Emergency Network is fully ONLINE.
Wed Oct 11 12:15:00 UTC 2023: Fiber restored! Cleaning up emergency system...
🔒 Modem powered completely OFF. System running on Fiber.
```

---

## Troubleshooting
### Common Issues
1. **`uhubctl` Not Found**:
   Ensure `uhubctl` is installed and compatible with your USB hub.
   ```bash
   sudo apt install uhubctl
   ```

2. **Wi-Fi Hotspot Not Starting**:
   Verify `hostapd` is installed and properly configured:
   ```bash
   sudo systemctl status hostapd
   ```

3. **Incorrect USB Hub/Port Configuration**:
   Use `uhubctl` to list available hubs and ports:
   ```bash
   sudo uhubctl
   ```

4. **Routing Issues**:
   Ensure the default route is correctly configured for both primary and backup connections.

---

## Notes
- The script is designed for continuous operation and should ideally be run as a background service.
- Consider adding the script to your system's startup sequence for automatic failover management.

---

## License
This script is licensed under the MIT License. See the LICENSE file for details.

---

## Author
Developed by [Your Name/Team]. For questions or support, contact [Your Email/Support Channel].