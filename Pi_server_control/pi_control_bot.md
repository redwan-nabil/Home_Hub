# 🚀 Release Notes

### Updates in `pi_control_bot.py`:
1. **Removed Weather and Thunderstorm Radar Functionality**:
   - The weather API integration and thunderstorm radar functionality have been removed, including the background radar thread and associated configurations (e.g., `WEATHER_API_KEY`, `PHONE_IP`, `CITY`).

2. **Added Network Sync on Boot**:
   - Introduced a `wait_for_internet` function to ensure the Raspberry Pi waits for a stable internet connection before starting the bot.

3. **Enhanced Shutdown Command**:
   - The `/shutdown` command now includes additional steps for safely stopping Docker containers and syncing disks before powering off the Raspberry Pi.

4. **Improved `/clear cache` Command**:
   - Enhanced the `/clear cache` command to include additional cleanup tasks:
     - Removal of temporary PDF files.
     - Cleaning of system logs older than 1 day.
     - Clearing of APT cache.
     - Dropping unused RAM caches.

5. **Improved `/performance` Command**:
   - Added power consumption calculation using the Raspberry Pi's PMIC (Power Management Integrated Circuit) data.
   - Improved error handling for performance data collection.
   - Enhanced the performance report to include:
     - Total system power draw in watts.
     - Internet speed test results (download, upload, and ping).

6. **Removed Unused Code**:
   - Removed unused imports and configurations related to weather API and radar functionality (e.g., `requests`, `threading`, `WEATHER_API_KEY`, etc.).

7. **Startup Notification**:
   - Added a startup notification to inform the admin when the Raspberry Pi and bot are online.

---

# Pi Control Bot

`pi_control_bot.py` is a Python-based Telegram bot designed to provide remote control and monitoring capabilities for a Raspberry Pi. The bot includes features such as secure system commands with two-factor authentication (2FA), system performance monitoring, and safe shutdown procedures.

## Features

1. **Secure System Commands with 2FA**:
   - Execute critical system commands (`/reboot`, `/shutdown`, `/clear cache`) only after verifying a one-time password (OTP) sent to the admin's email.

2. **System Performance Monitoring**:
   - Monitor Raspberry Pi's performance metrics, including:
     - CPU usage
     - RAM usage
     - GPU memory usage
     - System temperature
     - Power consumption
     - Internet speed (download, upload, and ping)

3. **Safe Shutdown Procedures**:
   - The `/shutdown` command ensures a safe shutdown by stopping Docker containers and syncing disks before powering off.

4. **Deep Cache Cleaning**:
   - The `/clear cache` command performs a comprehensive cleanup of temporary files, logs, and unused RAM caches.

5. **Startup Notification**:
   - Sends a notification to the admin when the Raspberry Pi boots up and the bot is online.

---

## Prerequisites

1. **Hardware**:
   - A Raspberry Pi with an internet connection.

2. **Software**:
   - Python 3.x
   - Required Python libraries (see [Installation](#installation)).

3. **Telegram Bot**:
   - A Telegram bot token obtained from [BotFather](https://core.telegram.org/bots#botfather).
   - Your Telegram user ID (to set as the admin).

4. **Email Account**:
   - A Gmail account with an app-specific password for sending OTPs.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. **Install Dependencies**:
   Install the required Python libraries:
   ```bash
   pip install pyTelegramBotAPI psutil speedtest-cli
   ```

3. **Configure the Script**:
   - Open `pi_control_bot.py` and update the following variables:
     - `BOT_TOKEN`: Your Telegram bot token.
     - `ADMIN_ID`: Your Telegram user ID.
     - `SENDER_EMAIL`: Your Gmail address.
     - `EMAIL_APP_PASSWORD`: Your Gmail app-specific password.
     - `RECEIVER_EMAIL`: The email address where OTPs will be sent.

4. **Run the Bot**:
   ```bash
   python3 pi_control_bot.py
   ```

---

## Usage

### 1. **Secure Commands**
   - **Reboot**: `/reboot`
   - **Shutdown**: `/shutdown`
   - **Clear Cache**: `/clear cache`

   For each command:
   - The bot will send an OTP to the configured email.
   - Reply with the OTP to confirm the command.

### 2. **Performance Monitoring**
   - Use the `/performance` command to get a detailed report of the Raspberry Pi's performance metrics.

---

## Security

- **Two-Factor Authentication (2FA)**:
  - All critical commands require OTP verification.
  - OTPs are sent to the configured email address.

- **Admin Restriction**:
  - Only the admin (identified by `ADMIN_ID`) can interact with the bot.

---

## Known Issues

1. **Email Delivery**:
   - Ensure the Gmail account used for sending OTPs has app-specific passwords enabled.
   - Verify that the email credentials are correct.

2. **Performance Monitoring**:
   - Power consumption data may not be available on older Raspberry Pi models.

3. **Internet Connectivity**:
   - The bot waits for an active internet connection before starting. Ensure the Raspberry Pi is connected to a network.

---

## Future Improvements

1. **Add More Commands**:
   - Extend functionality to include additional system management commands.

2. **Multi-User Support**:
   - Allow multiple admins with different levels of access.

3. **Improved Error Handling**:
   - Enhance error reporting for email delivery and performance monitoring.

4. **Web-Based Dashboard**:
   - Develop a web interface for monitoring and controlling the Raspberry Pi.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

Developed by **Nabil Redwoan**. For any inquiries, please contact [nabilredwoan2005@gmail.com](mailto:nabilredwoan2005@gmail.com).