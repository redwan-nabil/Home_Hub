# Pi Control Bot - Raspberry Pi Server Control with Telegram Bot

## Overview
The `pi_control_bot.py` script is a powerful tool designed to manage and monitor a Raspberry Pi server remotely via Telegram. It includes secure command execution with Two-Factor Authentication (2FA), system performance monitoring, and an emergency thunderstorm radar for automated shutdown during severe weather conditions. The bot is designed to ensure security, reliability, and ease of use for administrators.

---

## Features

### 1. **Secure Command Execution with 2FA**
- Commands such as `reboot`, `shutdown`, and `clear cache` require administrator authentication via a one-time password (OTP) sent to a pre-configured email address.
- Unauthorized users attempting to execute commands are denied access.

### 2. **System Performance Monitoring**
- Provides detailed system performance metrics including:
  - CPU usage
  - RAM usage
  - GPU memory
  - Temperature
  - Internet speed (download, upload, ping)
  - Total system power draw (if supported by Raspberry Pi model)

### 3. **Emergency Thunderstorm Radar**
- Monitors weather conditions using OpenWeatherMap API.
- Automatically shuts down the Raspberry Pi during thunderstorms to protect hardware.
- Differentiates between scenarios where the administrator is actively working or at home.

### 4. **Background Radar Thread**
- Continuously scans for weather updates every 15 minutes.
- Executes emergency shutdown procedures if a thunderstorm is detected.

---

## Prerequisites

### Hardware
- Raspberry Pi (recommended: Raspberry Pi 4 or newer)
- Internet connection
- Email account for 2FA

### Software
- Python 3.x
- Required Python libraries:
  - `telebot`
  - `psutil`
  - `speedtest`
  - `subprocess`
  - `smtplib`
  - `requests`
  - `email`

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. **Install Dependencies**
   Install the required Python libraries:
   ```bash
   pip install pyTelegramBotAPI psutil speedtest-cli requests
   ```

3. **Configure Credentials**
   - Open the `pi_control_bot.py` file and update the following variables:
     - `BOT_TOKEN`: Your Telegram bot token.
     - `ADMIN_ID`: Your Telegram user ID.
     - `SENDER_EMAIL`: Email address used to send OTPs.
     - `EMAIL_APP_PASSWORD`: App password for the sender email.
     - `RECEIVER_EMAIL`: Email address to receive OTPs.
     - `WEATHER_API_KEY`: API key for OpenWeatherMap.
     - `PHONE_IP`: Local IP address of your phone (used for radar checks).
     - `CITY`: City name and country code for weather monitoring (e.g., `Dhaka,BD`).

4. **Run the Script**
   ```bash
   python3 pi_control_bot.py
   ```

---

## Usage

### Telegram Commands
1. **Secure Commands**
   - `/reboot`: Reboots the Raspberry Pi (requires OTP verification).
   - `/shutdown`: Shuts down the Raspberry Pi (requires OTP verification).
   - `/clear cache`: Clears system cache and temporary files (requires OTP verification).

2. **Performance Monitoring**
   - `/performance`: Displays detailed system performance metrics.

---

## Security Features

### Two-Factor Authentication (2FA)
- OTPs are sent to the administrator's email for secure command execution.
- OTPs expire after one use or if canceled by the administrator.

### Restricted Access
- Only the administrator (defined by `ADMIN_ID`) can execute commands or access system data.

---

## Emergency Thunderstorm Radar

### Functionality
- Monitors weather conditions using OpenWeatherMap API.
- Detects thunderstorms (weather codes 200-232).
- Executes emergency shutdown procedures to protect the Raspberry Pi during severe weather.

### Scenarios
1. **Administrator Working on Pi**
   - Sends a warning message but does not shut down the system.
2. **Administrator at Home**
   - Sends a warning message and shuts down the system after a delay.
3. **Administrator Away**
   - Sends a warning message and shuts down the system immediately.

---

## Background Processes

### Radar Thread
- Runs continuously in the background to monitor weather conditions.
- Checks for updates every 15 minutes.

### Telegram Bot
- Runs in the foreground to handle user commands and interactions.

---

## Error Handling

- Email errors during OTP generation are logged and reported to the administrator.
- Performance monitoring errors are handled gracefully with error messages sent via Telegram.
- Radar errors are logged for debugging purposes.

---

## Notes

- Ensure the Raspberry Pi has proper email and internet configurations for the bot to function correctly.
- The script uses system-level commands (e.g., `sudo reboot`, `sudo shutdown`). Ensure the bot is run with appropriate permissions.
- The radar functionality requires an active OpenWeatherMap API key.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Disclaimer

Use this script at your own risk. The developers are not responsible for any damage caused to your Raspberry Pi or data loss due to improper use of the bot. Always test the script in a controlled environment before deploying it in production.