# 🚀 Release Notes

### Changes in `auto_backup.sh` for `Pi_server_control`
1. **Migration from Bash to Python**:
   - The script has been completely rewritten in Python, replacing the original Bash implementation.
   - The new implementation leverages the `telebot` library for Telegram bot integration and Python libraries for system monitoring and email notifications.

2. **Enhanced Security**:
   - Added a Two-Factor Authentication (2FA) mechanism for critical commands (`reboot`, `shutdown`, `clear cache`) using OTP sent via email.
   - Only the admin user (identified by `ADMIN_ID`) can execute these commands.

3. **New Features**:
   - **Network Sync on Boot**: The script waits for an active internet connection before proceeding.
   - **System Performance Monitoring**: Added a `/performance` command to monitor system metrics such as temperature, CPU usage, RAM usage, GPU memory, power draw, and internet speed.
   - **Enhanced Shutdown Process**: The shutdown command now includes stopping Docker containers and syncing disks before powering off.
   - **Deep Cache Cleaning**: The `/clear cache` command now performs a deep clean of temporary files, system logs, and RAM caches.

4. **Improved Logging and Notifications**:
   - Notifications are sent to the admin via Telegram for critical events such as system boot, command execution, and errors.
   - Detailed error handling and user feedback for failed operations.

5. **Removed Legacy Features**:
   - The old Bash-based backup pipeline and resource governor have been removed in favor of the new Python-based implementation.

---

# Pi Server Control Bot - `auto_backup.sh`

## Overview

The `auto_backup.sh` script has been updated to a Python-based implementation, providing a robust and secure way to manage and monitor your Raspberry Pi server. The script integrates with Telegram for remote control and notifications, and includes features such as two-factor authentication (2FA), system performance monitoring, and enhanced system management commands.

---

## Features

### 1. **Two-Factor Authentication (2FA) for Secure Commands**
   - Critical commands (`/reboot`, `/shutdown`, `/clear cache`) require a one-time password (OTP) sent to the admin's email.
   - Only the admin user (identified by `ADMIN_ID`) can execute these commands.
   - OTPs are valid for a single use and are automatically invalidated after a failed attempt or cancellation.

### 2. **Network Sync on Boot**
   - The script ensures that the Raspberry Pi is connected to the internet before starting the bot.

### 3. **System Performance Monitoring**
   - The `/performance` command provides detailed system metrics, including:
     - CPU usage
     - RAM usage
     - GPU memory usage
     - System temperature
     - Power draw (if supported by the hardware)
     - Internet speed (download/upload) and ping

### 4. **Enhanced Shutdown Process**
   - The `/shutdown` command stops all Docker containers, syncs disks, and safely powers off the Raspberry Pi.

### 5. **Deep Cache Cleaning**
   - The `/clear cache` command removes temporary files, cleans system logs, and frees up RAM by dropping caches.

### 6. **Telegram Notifications**
   - The bot sends notifications to the admin for:
     - System boot
     - Command execution
     - Errors or issues during execution

---

## Installation

### Prerequisites
1. **Python 3.6+**: Ensure Python is installed on your Raspberry Pi.
2. **Install Required Python Libraries**:
   ```bash
   pip install pyTelegramBotAPI psutil speedtest-cli
   ```
3. **Email Configuration**:
   - Use a Gmail account for sending OTPs.
   - Enable "Allow less secure apps" in your Gmail account settings or create an App Password if 2FA is enabled.

### Setup
1. Clone the `Pi_server_control` repository:
   ```bash
   git clone https://github.com/your-repo/Pi_server_control.git
   cd Pi_server_control
   ```
2. Update the following credentials in the script:
   - `BOT_TOKEN`: Your Telegram bot token.
   - `ADMIN_ID`: Your Telegram user ID.
   - `SENDER_EMAIL`: The email address used to send OTPs.
   - `EMAIL_APP_PASSWORD`: The app password for the sender email.
   - `RECEIVER_EMAIL`: The email address to receive OTPs.

3. Make the script executable:
   ```bash
   chmod +x auto_backup.sh
   ```

4. Run the script:
   ```bash
   python3 auto_backup.sh
   ```

---

## Usage

### Telegram Commands
1. **/reboot**: Reboots the Raspberry Pi after OTP verification.
2. **/shutdown**: Shuts down the Raspberry Pi after stopping Docker containers and syncing disks (requires OTP verification).
3. **/clear cache**: Performs a deep clean of temporary files, system logs, and RAM caches (requires OTP verification).
4. **/performance**: Displays system performance metrics.

### OTP Verification
- After sending a secure command, the bot will generate a 6-digit OTP and send it to the admin's email.
- Reply to the bot with the OTP to confirm the command.
- To cancel the command, reply with `cancel`.

---

## Error Handling
- The bot provides detailed error messages for failed operations.
- If the email fails to send, the bot will notify the admin and the command will not proceed.

---

## Security
- The bot is designed to be used by a single admin user, identified by `ADMIN_ID`.
- All critical commands are protected by a 2FA mechanism using OTPs sent via email.
- Ensure that your email credentials and bot token are kept secure and not shared.

---

## Known Issues
1. **Performance Monitoring**:
   - Power draw calculation may not be available on all Raspberry Pi models.
   - Internet speed test may take up to 20 seconds to complete.

2. **Email Delivery**:
   - Ensure that the sender email account is properly configured to allow sending emails via SMTP.

3. **Error Handling**:
   - Some error messages may not provide detailed information. Future updates will improve error reporting.

---

## Future Improvements
1. Add support for multiple admin users.
2. Implement logging to a file for better debugging and audit trails.
3. Enhance the `/performance` command to include additional metrics.
4. Add support for more email providers beyond Gmail.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

---

## Contact
For questions or support, please contact [Nabil Redwoan](mailto:nabilredwoan2005@gmail.com).