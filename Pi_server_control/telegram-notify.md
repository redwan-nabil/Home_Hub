# Telegram Notify Service (`telegram-notify.service`)

This service is designed to notify a Telegram bot when a Raspberry Pi system boots up or shuts down. Additionally, it runs a Python-based Telegram bot (`pi_control_bot.py`) that allows for administrative control of the Raspberry Pi via Telegram.

## Features

- **Boot Notification**: Sends a Telegram message when the Raspberry Pi boots up.
- **Shutdown Notification**: Sends a Telegram message when the Raspberry Pi is shutting down.
- **Admin Control Bot**: Runs a Python-based Telegram bot that allows for administrative control of the Raspberry Pi, such as shutting it down remotely.
- **Automatic Restart**: The service is configured to automatically restart in case of failure.

---

## Prerequisites

1. **Python 3**: Ensure Python 3 is installed on the Raspberry Pi.
2. **`pi_alert` Script**: A custom script located at `/usr/local/bin/pi_alert` is required to send Telegram notifications. This script should handle sending messages to a Telegram bot.
3. **`pi_control_bot.py` Script**: The main Python script for the Telegram bot, located at `/home/redwannabil/pi_control_bot.py`.
4. **Network Connectivity**: The service depends on the network being online to send notifications and run the bot.

---

## Installation

1. **Place the Service File**:
   Save the `telegram-notify.service` file in the systemd directory:
   ```
   /etc/systemd/system/telegram-notify.service
   ```

2. **Ensure Scripts Are in Place**:
   - The `pi_alert` script must be executable and located at `/usr/local/bin/pi_alert`.
   - The `pi_control_bot.py` script must be located at `/home/redwannabil/pi_control_bot.py`.

3. **Set Permissions**:
   Ensure the necessary scripts have the correct permissions:
   ```bash
   sudo chmod +x /usr/local/bin/pi_alert
   sudo chmod +x /home/redwannabil/pi_control_bot.py
   ```

4. **Enable the Service**:
   Enable the service to start on boot:
   ```bash
   sudo systemctl enable telegram-notify.service
   ```

5. **Start the Service**:
   Start the service immediately:
   ```bash
   sudo systemctl start telegram-notify.service
   ```

---

## Service Configuration

### `[Unit]` Section
- **Description**: Describes the service as a Telegram Boot Notifier and Admin Control Bot.
- **Dependencies**:
  - `After=network-online.target`: Ensures the service starts only after the network is online.
  - `Wants=network-online.target`: Indicates the service requires the network to be online.

### `[Service]` Section
- **WorkingDirectory**: Specifies the working directory for the service (`/home/redwannabil`).
- **Type**: Set to `simple`, meaning the service starts the main process directly.
- **ExecStartPre**: Executes the `pi_alert` script to send a boot notification before starting the main bot. The `-` prefix ensures that errors (e.g., due to slow Wi-Fi connection) are ignored.
- **ExecStart**: Runs the `pi_control_bot.py` script using Python 3.
- **ExecStop**: Executes the `pi_alert` script to send a shutdown notification when the service stops.
- **Restart**: Ensures the service restarts automatically if it fails.
- **RestartSec**: Specifies a 10-second delay before restarting the service.

### `[Install]` Section
- **WantedBy**: Ensures the service is started in the `multi-user.target` (standard multi-user mode).

---

## Usage

### Starting the Service
To manually start the service:
```bash
sudo systemctl start telegram-notify.service
```

### Stopping the Service
To stop the service:
```bash
sudo systemctl stop telegram-notify.service
```

### Checking Service Status
To check the status of the service:
```bash
sudo systemctl status telegram-notify.service
```

### Enabling the Service at Boot
To enable the service to start automatically on boot:
```bash
sudo systemctl enable telegram-notify.service
```

### Disabling the Service at Boot
To disable the service from starting automatically:
```bash
sudo systemctl disable telegram-notify.service
```

---

## Troubleshooting

1. **Service Fails to Start**:
   - Check the logs for errors:
     ```bash
     sudo journalctl -u telegram-notify.service
     ```
   - Ensure the `pi_alert` and `pi_control_bot.py` scripts are in their expected locations and executable.

2. **Notifications Not Sent**:
   - Verify the `pi_alert` script is working correctly by running it manually:
     ```bash
     /usr/local/bin/pi_alert "Test Message"
     ```
   - Check the network connection.

3. **Bot Not Responding**:
   - Ensure the `pi_control_bot.py` script is functioning correctly by running it manually:
     ```bash
     python3 /home/redwannabil/pi_control_bot.py
     ```

---

## Notes

- The `pi_alert` script is critical for sending Telegram notifications. Ensure it is properly configured with your Telegram bot token and chat ID.
- The `pi_control_bot.py` script should be implemented to handle administrative commands securely. Avoid exposing sensitive operations without proper authentication.
- The service is configured to restart automatically in case of failure, with a 10-second delay between restart attempts.

---

## Uninstallation

To remove the service:

1. Stop the service:
   ```bash
   sudo systemctl stop telegram-notify.service
   ```

2. Disable the service:
   ```bash
   sudo systemctl disable telegram-notify.service
   ```

3. Remove the service file:
   ```bash
   sudo rm /etc/systemd/system/telegram-notify.service
   ```

4. Reload systemd to apply changes:
   ```bash
   sudo systemctl daemon-reload
   ```

---

## License

This service and its associated scripts are provided as-is. Ensure proper security measures are in place when using Telegram bots for administrative control. Use at your own risk.