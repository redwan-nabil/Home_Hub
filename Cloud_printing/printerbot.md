# README for `printerbot.service`

## Overview

The `printerbot.service` is a systemd service unit designed to manage the Telegram Printer and Scanner Bot. This bot, implemented in Python, facilitates printing and scanning tasks via Telegram. The service ensures that the bot runs continuously and restarts automatically in case of failure.

---

## Service Details

### Unit Section
- **Description**: Provides a brief description of the service: "Telegram Printer and Scanner Bot".
- **After**: Specifies that the service should start only after the `network.target` is active, ensuring network connectivity is available.

### Service Section
- **User**: The service runs under the `redwannabil` user account.
- **WorkingDirectory**: The working directory for the service is `/home/redwannabil`.
- **ExecStart**: Specifies the command to start the bot:
  ```
  /usr/bin/python3 /home/redwannabil/businessbot.py
  ```
  This runs the `businessbot.py` script using Python 3.
- **Restart**: Configured to always restart the service if it stops unexpectedly.
- **RestartSec**: Sets a 10-second delay before attempting to restart the service.

### Install Section
- **WantedBy**: Ensures the service is started as part of the `multi-user.target`, which is a standard systemd target for non-graphical multi-user systems.

---

## Installation and Usage

### Prerequisites
1. Ensure Python 3 is installed on the system.
2. Verify that the `businessbot.py` script is located in `/home/redwannabil` and is executable.
3. Ensure the `redwannabil` user exists and has the necessary permissions to execute the script.

### Steps to Install the Service
1. Copy the `printerbot.service` file to the systemd directory:
   ```
   sudo cp printerbot.service /etc/systemd/system/
   ```
2. Reload the systemd daemon to recognize the new service:
   ```
   sudo systemctl daemon-reload
   ```
3. Enable the service to start on boot:
   ```
   sudo systemctl enable printerbot.service
   ```
4. Start the service:
   ```
   sudo systemctl start printerbot.service
   ```

### Verifying the Service
- Check the status of the service:
  ```
  sudo systemctl status printerbot.service
  ```
- View logs for debugging:
  ```
  journalctl -u printerbot.service
  ```

---

## Troubleshooting

1. **Service Fails to Start**:
   - Verify the `businessbot.py` script exists in `/home/redwannabil`.
   - Ensure the script is executable:
     ```
     chmod +x /home/redwannabil/businessbot.py
     ```
   - Check for Python 3 installation:
     ```
     python3 --version
     ```

2. **Permission Issues**:
   - Ensure the `redwannabil` user has the necessary permissions for the working directory and script.

3. **Network Issues**:
   - Since the service depends on network connectivity, ensure the system's network is properly configured and active.

---

## Customization

- **Change User**: To run the service under a different user, modify the `User` directive in the `[Service]` section.
- **Change Working Directory**: Update the `WorkingDirectory` directive to point to the desired directory.
- **Modify Restart Behavior**: Adjust the `Restart` and `RestartSec` directives to change the restart policy and delay.

---

## Uninstallation

To remove the service:
1. Stop the service:
   ```
   sudo systemctl stop printerbot.service
   ```
2. Disable the service:
   ```
   sudo systemctl disable printerbot.service
   ```
3. Remove the service file:
   ```
   sudo rm /etc/systemd/system/printerbot.service
   ```
4. Reload the systemd daemon:
   ```
   sudo systemctl daemon-reload
   ```

---

## Notes

- Ensure the `businessbot.py` script is properly configured to handle Telegram bot interactions and printing/scanning tasks.
- Regularly monitor the service logs for any errors or issues.

--- 

## License

This service configuration is provided as-is. Ensure compliance with your organization's policies and guidelines when deploying this service.