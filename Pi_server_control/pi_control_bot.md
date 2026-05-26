# 🚀 Release Notes

### Updates in `pi_control_bot.py`:
1. **New Feature: Enhanced System Performance Monitoring**
   - Added detailed system performance monitoring under the `/performance` command.
   - Reports CPU usage, RAM usage, GPU memory, system temperature, power draw (with PMIC linear correction for Raspberry Pi 5), and internet speed (download, upload, and ping).

2. **Improved Security for Secure Commands**
   - Enhanced the `/clear` command to validate the exact syntax `/clear cache` to prevent accidental execution.
   - Added detailed error messages for invalid `/clear` command usage.

3. **Bug Fixes**
   - Fixed missing `chat_id` parameter in `bot.edit_message_text` within the `/performance` command handler.
   - Improved error handling for email sending and performance data retrieval.

4. **Code Refactoring**
   - Improved code readability and modularity by adding comments and organizing sections.
   - Enhanced logging for better debugging and monitoring.

---

# Pi Server Control Bot

`pi_control_bot.py` is a Python-based Telegram bot designed to provide secure remote control and monitoring of a Raspberry Pi server. It includes features like two-factor authentication (2FA) for critical commands, system performance monitoring, and automated email notifications for security.

## Features

1. **Secure Commands with 2FA**
   - Commands like `/reboot`, `/shutdown`, and `/clear cache` are protected with a one-time password (OTP) sent to the admin's email.
   - Only the authorized admin can execute these commands after verifying the OTP.

2. **System Performance Monitoring**
   - Use the `/performance` command to get detailed system performance metrics, including:
     - CPU usage
     - RAM usage
     - GPU memory usage
     - System temperature
     - Total power draw (with PMIC correction for Raspberry Pi 5)
     - Internet speed (download, upload, and ping)

3. **Startup Notification**
   - Sends a notification to the admin's Telegram account when the Raspberry Pi boots up and the bot is ready.

4. **Network Connectivity Check**
   - Ensures the Raspberry Pi is connected to the internet before starting the bot.

5. **Error Handling**
   - Provides detailed error messages for email sending, command execution, and performance monitoring.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```

2. **Install Dependencies**
   Ensure you have Python 3 installed, then install the required Python packages:
   ```bash
   pip install pyTelegramBotAPI psutil speedtest-cli
   ```

3. **Configure Credentials**
   - Open `pi_control_bot.py` and replace the following placeholders with your credentials:
     - `BOT_TOKEN`: Your Telegram bot token.
     - `ADMIN_ID`: Your Telegram user ID.
     - `SENDER_EMAIL`: The email address used to send OTPs.
     - `EMAIL_APP_PASSWORD`: The app password for the sender email.
     - `RECEIVER_EMAIL`: The email address where OTPs will be sent.

4. **Set Up Email**
   - Ensure the sender email account is configured to allow app passwords (e.g., for Gmail, enable "Allow less secure apps" or use an app password).

5. **Run the Bot**
   Start the bot using the following command:
   ```bash
   python3 pi_control_bot.py
   ```

---

## Usage

### 1. **Secure Commands**
   - `/reboot`: Reboots the Raspberry Pi after OTP verification.
   - `/shutdown`: Safely shuts down the Raspberry Pi after OTP verification.
   - `/clear cache`: Clears temporary files, system logs, and frees up RAM after OTP verification.

   **Example Workflow:**
   - Send `/reboot` to the bot.
   - The bot will send an OTP to the configured email.
   - Reply to the bot with the OTP to execute the command.

### 2. **System Performance**
   - `/performance`: Displays detailed system performance metrics, including:
     - CPU usage
     - RAM usage
     - GPU memory usage
     - System temperature
     - Total power draw (for Raspberry Pi 5)
     - Internet speed (download, upload, and ping)

   **Example Output:**
   ```
   📊 Raspberry Pi Performance:

   🌡️ Temperature: 45.2°C
   ⚡ Power Draw: 5.67 W (Total System)
   🧠 CPU Usage: 23%
   💾 RAM Usage: 45%
   🎮 GPU Memory: 76M

   🌐 Internet Speed:
   ⬇️ Download: 50.23 Mbps
   ⬆️ Upload: 10.45 Mbps
   🏓 Ping: 25.3 ms
   ```

### 3. **Startup Notification**
   - Upon boot, the bot sends a message to the admin's Telegram account:
     ```
     🚀 *System Online:* Raspberry Pi has successfully booted and the Control Bot is ready.
     ```

---

## Security

- **Two-Factor Authentication (2FA):** Critical commands require a one-time password (OTP) sent to the admin's email for execution.
- **Admin Restriction:** Only the admin (identified by `ADMIN_ID`) can interact with the bot.
- **Email Alerts:** The bot sends email notifications for every secure command request.

---

## Troubleshooting

1. **Bot Not Responding**
   - Ensure the Raspberry Pi is connected to the internet.
   - Verify that the `BOT_TOKEN` and `ADMIN_ID` are correctly configured.

2. **Email Not Sent**
   - Check the `SENDER_EMAIL` and `EMAIL_APP_PASSWORD` credentials.
   - Ensure the sender email account allows app passwords or less secure apps.

3. **Performance Metrics Not Displayed**
   - Ensure the `vcgencmd` command is available on your Raspberry Pi.
   - Install the `speedtest-cli` Python package if internet speed is not displayed.

4. **Permission Issues**
   - Ensure the bot script is run with sufficient permissions to execute system commands (e.g., `sudo`).

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.