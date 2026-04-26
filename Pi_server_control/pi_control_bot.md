# 🚀 Release Notes

### Updates in `pi_control_bot.py`:
1. **Enhanced System Performance Monitoring**:
   - Added detailed power draw calculations using Raspberry Pi PMIC data.
   - Improved error handling for performance data retrieval.
   - Enhanced performance metrics with GPU memory and system power draw.

2. **Improved Thunderstorm Radar**:
   - Added checks for admin activity (`is_admin_working`) and presence at home (`is_admin_home`) to decide on emergency shutdown actions.
   - Enhanced alert messages for thunderstorms with detailed instructions for the admin.

3. **Bug Fixes**:
   - Fixed missing parentheses in `bot.edit_message_text` calls in the `/performance` command.
   - Improved error handling for email sending and radar scanning.

4. **Code Refactoring**:
   - Organized code into sections for better readability and maintainability.
   - Improved comments and documentation for better understanding of the code.

---

# Pi Control Bot with 2FA & Weather Radar

`pi_control_bot.py` is a Python-based Telegram bot designed to provide secure remote control and monitoring of a Raspberry Pi. The bot includes two-factor authentication (2FA) for critical commands, system performance monitoring, and an emergency thunderstorm radar.

## Features

1. **Two-Factor Authentication (2FA)**:
   - Secure execution of critical commands (`/reboot`, `/shutdown`, `/clear cache`) using email-based OTP verification.

2. **System Performance Monitoring**:
   - Monitor CPU usage, RAM usage, GPU memory, temperature, and power draw.
   - Perform internet speed tests (download, upload, and ping).

3. **Thunderstorm Radar**:
   - Monitors weather conditions using OpenWeatherMap API.
   - Automatically shuts down the Raspberry Pi during thunderstorms to protect hardware.
   - Checks if the admin is actively working or at home before initiating shutdown.

4. **Background Radar Thread**:
   - Continuously monitors weather conditions every 15 minutes.

5. **Admin Authentication**:
   - Only the admin (specified by `ADMIN_ID`) can interact with the bot.

---

## Installation

### Prerequisites
- Python 3.6 or higher
- A Telegram bot token (create one using [BotFather](https://core.telegram.org/bots#botfather))
- OpenWeatherMap API key (sign up at [OpenWeatherMap](https://openweathermap.org/))
- A Gmail account with an app password for sending OTP emails
- Raspberry Pi with `vcgencmd` and `psutil` installed

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. Install required Python libraries:
   ```bash
   pip install pyTelegramBotAPI psutil speedtest-cli requests
   ```

3. Configure the bot:
   - Open `pi_control_bot.py` and replace the following placeholders with your credentials:
     - `BOT_TOKEN`: Your Telegram bot token.
     - `ADMIN_ID`: Your Telegram user ID.
     - `SENDER_EMAIL`: Your Gmail address.
     - `EMAIL_APP_PASSWORD`: Your Gmail app password.
     - `RECEIVER_EMAIL`: Your email address to receive OTPs.
     - `WEATHER_API_KEY`: Your OpenWeatherMap API key.
     - `PHONE_IP`: Your phone's local IP address.
     - `CITY`: Your city and country code (e.g., `Dhaka,BD`).

4. Run the bot:
   ```bash
   python3 pi_control_bot.py
   ```

---

## Usage

### Commands
1. **Secure Commands**:
   - `/reboot`: Reboot the Raspberry Pi.
   - `/shutdown`: Shut down the Raspberry Pi.
   - `/clear cache`: Perform a deep clean of temporary files and caches.

   **Note**: These commands require OTP verification sent to your email.

2. **Performance Monitoring**:
   - `/performance`: Display system performance metrics, including CPU usage, RAM usage, GPU memory, temperature, power draw, and internet speed.

3. **Thunderstorm Radar**:
   - The radar runs in the background and monitors weather conditions every 15 minutes.
   - If a thunderstorm is detected:
     - If the admin is working on the Pi, a warning is sent to save work and unplug manually.
     - If the admin is at home but not working, an emergency shutdown is initiated with a warning to unplug the adapter.
     - If the admin is not home, the Pi shuts down to protect hardware.

---

## Security

- **Two-Factor Authentication**: Critical commands require a 6-digit OTP sent to the admin's email.
- **Admin-Only Access**: Only the admin (specified by `ADMIN_ID`) can interact with the bot.
- **Email Alerts**: Alerts are sent to the admin's email for secure command execution.

---

## Troubleshooting

1. **Email Sending Issues**:
   - Ensure the Gmail app password is correctly configured.
   - Verify that "Allow less secure apps" is enabled in your Gmail account settings.

2. **Weather API Issues**:
   - Ensure the OpenWeatherMap API key is valid and correctly configured.
   - Check your internet connection.

3. **Performance Metrics Errors**:
   - Ensure `vcgencmd` is installed and accessible on your Raspberry Pi.
   - Verify that `psutil` and `speedtest-cli` are installed.

4. **Bot Not Responding**:
   - Check if the bot token is correctly configured.
   - Ensure the bot is running and connected to the internet.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.