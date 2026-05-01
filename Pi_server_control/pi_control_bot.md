# 🚀 Release Notes

### Updates in `pi_control_bot.py`:
1. **Enhanced Performance Monitoring**:
   - Added calculation for total system power draw using Raspberry Pi 5 PMIC data with linear correction.
   - Improved error handling for performance data retrieval.

2. **Thunderstorm Radar Enhancements**:
   - Added checks for admin activity (`is_admin_working`) and presence at home (`is_admin_home`) to determine appropriate actions during thunderstorms.
   - Implemented emergency shutdown procedures during severe weather conditions.

3. **Bug Fixes**:
   - Fixed missing `chat_id` parameter in `bot.edit_message_text` calls within the `check_performance` function.
   - Improved error handling for radar scanning and weather API requests.

4. **General Improvements**:
   - Refined email OTP generation and validation logic for secure commands.
   - Added additional cleanup commands in `/clear cache` functionality.

---

# Pi Admin Control Bot with 2FA & Weather Radar

## Overview
`pi_control_bot.py` is a Python-based Telegram bot designed to manage and monitor a Raspberry Pi server securely. It includes features such as two-factor authentication (2FA), system performance monitoring, and an emergency thunderstorm radar. The bot ensures secure access to critical commands and automates safety measures during severe weather conditions.

---

## Features

### 1. **Secure Commands with 2FA**
- Commands like `/reboot`, `/shutdown`, and `/clear cache` require OTP verification sent via email.
- Admin can cancel actions or verify OTP to execute commands securely.

### 2. **System Performance Monitoring**
- Provides detailed system metrics:
  - CPU usage
  - RAM usage
  - GPU memory
  - Temperature
  - Internet speed (download, upload, ping)
  - Total system power draw (Raspberry Pi 5 PMIC data with linear correction)

### 3. **Thunderstorm Radar**
- Monitors weather conditions in the configured city using OpenWeatherMap API.
- Automatically shuts down the Raspberry Pi during thunderstorms if the admin is not actively working or at home.
- Sends alerts to the admin before executing emergency actions.

### 4. **Background Radar Thread**
- Continuously scans for thunderstorms every 15 minutes.
- Executes emergency shutdown procedures to protect hardware during severe weather.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Raspberry Pi OS or compatible Linux distribution
- Telegram account and bot token
- OpenWeatherMap API key
- Gmail account for email notifications

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. Install dependencies:
   ```bash
   pip install telebot psutil speedtest-cli requests
   ```

3. Configure credentials:
   - Open `pi_control_bot.py` and replace placeholders (`REDACTED_BY_SYSADMIN`) with actual values:
     - `BOT_TOKEN`: Telegram bot token
     - `ADMIN_ID`: Telegram user ID of the admin
     - `SENDER_EMAIL`: Gmail address for sending OTPs
     - `EMAIL_APP_PASSWORD`: App password for the Gmail account
     - `RECEIVER_EMAIL`: Email address to receive OTPs
     - `WEATHER_API_KEY`: OpenWeatherMap API key
     - `PHONE_IP`: Local IP address of the admin's phone
     - `CITY`: City name and country code (e.g., `Dhaka,BD`)

4. Run the bot:
   ```bash
   python pi_control_bot.py
   ```

---

## Usage

### Telegram Commands
- `/reboot`: Reboot the Raspberry Pi (requires OTP verification).
- `/shutdown`: Shut down the Raspberry Pi (requires OTP verification).
- `/clear cache`: Perform a deep clean of temporary files and cached data (requires OTP verification).
- `/performance`: Display detailed system performance metrics.

### Emergency Thunderstorm Radar
- Automatically scans for thunderstorms every 15 minutes.
- Sends alerts and executes emergency shutdown if severe weather is detected.

---

## Configuration

### Email Notifications
- Ensure the Gmail account used for `SENDER_EMAIL` has "Allow less secure apps" enabled or use an app password.

### Weather API
- Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api) and configure `WEATHER_API_KEY`.

### Admin Presence
- Update `PHONE_IP` with the local IP address of the admin's phone for presence detection.

---

## Troubleshooting

### Common Issues
1. **Email Sending Failure**:
   - Verify `EMAIL_APP_PASSWORD` and ensure the Gmail account allows app passwords.
   - Check internet connectivity.

2. **Weather API Errors**:
   - Ensure `WEATHER_API_KEY` is valid and has sufficient quota.
   - Verify the city name and country code format.

3. **Performance Metrics Unavailable**:
   - Ensure `vcgencmd` is installed and accessible on the Raspberry Pi.
   - Check hardware compatibility for PMIC data retrieval.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For support or inquiries, contact the repository owner at `nabilredwoan2005@gmail.com`.