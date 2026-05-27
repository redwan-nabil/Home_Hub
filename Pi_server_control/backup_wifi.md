# backup_wifi.service

## Overview
The `backup_wifi.service` is a systemd service designed to act as an emergency 4G failover watchdog for the `Pi_server_control` system. It ensures that a backup Wi-Fi connection is established and maintained in the event of a primary network failure. This service runs a script (`backup_wifi.sh`) that handles the failover process and continuously monitors the network status.

## Features
- Automatically starts the failover script (`backup_wifi.sh`) on boot.
- Monitors the failover process and ensures the script is always running.
- Restarts the script in case of failure or unexpected termination.
- Configured to retry every 10 seconds if the service fails.

## Service Configuration

### `[Unit]` Section
- **Description**: Provides a brief description of the service: "Emergency 4G Failover Watchdog".
- **After**: Specifies that the service should start only after the `network.target` is active. This ensures that the primary network stack is initialized before the failover script is executed.

### `[Service]` Section
- **ExecStart**: Specifies the command to execute when the service starts. In this case, it runs the script located at `/usr/local/bin/backup_wifi.sh`.
- **Restart**: Configured to always restart the service if it stops or crashes.
- **RestartSec**: Sets a delay of 10 seconds before attempting to restart the service.
- **User**: Runs the service as the `root` user to ensure it has the necessary permissions to manage network configurations.

### `[Install]` Section
- **WantedBy**: Ensures the service is started as part of the `multi-user.target`, which is the standard system runlevel for non-graphical multi-user systems.

## Installation

1. **Place the Service File**:
   Save the `backup_wifi.service` file to the systemd service directory:
   ```
   /etc/systemd/system/backup_wifi.service
   ```

2. **Reload Systemd Daemon**:
   After placing the service file, reload the systemd manager configuration to recognize the new service:
   ```
   sudo systemctl daemon-reload
   ```

3. **Enable the Service**:
   Enable the service to start automatically at boot:
   ```
   sudo systemctl enable backup_wifi.service
   ```

4. **Start the Service**:
   Start the service immediately:
   ```
   sudo systemctl start backup_wifi.service
   ```

5. **Check Service Status**:
   Verify that the service is running correctly:
   ```
   sudo systemctl status backup_wifi.service
   ```

## Usage

The `backup_wifi.service` is designed to run in the background and requires no manual intervention during normal operation. It will automatically monitor and manage the failover process using the `backup_wifi.sh` script.

### Logs
To view logs for the service, use the `journalctl` command:
```
sudo journalctl -u backup_wifi.service
```

This will display logs related to the execution of the `backup_wifi.sh` script and any issues encountered by the service.

## Customization

- **Script Path**: If the `backup_wifi.sh` script is located in a different directory, update the `ExecStart` line in the service file to reflect the correct path.
- **Restart Delay**: Modify the `RestartSec` value to change the delay between restart attempts.
- **User**: If the script does not require root privileges, you can change the `User` field to a less privileged user.

## Troubleshooting

- **Service Fails to Start**:
  - Check the syntax of the service file:
    ```
    sudo systemd-analyze verify /etc/systemd/system/backup_wifi.service
    ```
  - Review the logs for detailed error messages:
    ```
    sudo journalctl -u backup_wifi.service
    ```

- **Script Issues**:
  - Ensure the `backup_wifi.sh` script is executable:
    ```
    sudo chmod +x /usr/local/bin/backup_wifi.sh
    ```
  - Test the script manually to verify its functionality:
    ```
    /usr/local/bin/backup_wifi.sh
    ```

## Uninstallation

To remove the `backup_wifi.service`, follow these steps:

1. Stop the service:
   ```
   sudo systemctl stop backup_wifi.service
   ```

2. Disable the service:
   ```
   sudo systemctl disable backup_wifi.service
   ```

3. Remove the service file:
   ```
   sudo rm /etc/systemd/system/backup_wifi.service
   ```

4. Reload the systemd daemon:
   ```
   sudo systemctl daemon-reload
   ```

5. Optionally, remove the `backup_wifi.sh` script if it is no longer needed:
   ```
   sudo rm /usr/local/bin/backup_wifi.sh
   ```

## Notes
- Ensure that the `backup_wifi.sh` script is properly configured and tested to handle the failover process.
- This service requires root privileges to manage network configurations. Use caution when modifying the service or script.

## License
This service is part of the `Pi_server_control` project and is subject to the project's licensing terms.