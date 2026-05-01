# rpi-eeprom-update.service

## Overview

The `rpi-eeprom-update.service` is a systemd service designed to automate the process of checking for and applying updates to the EEPROM firmware on Raspberry Pi devices. This service ensures that the Raspberry Pi's bootloader and critical firmware components are kept up-to-date, improving system stability, performance, and compatibility.

## Features

- **Automated EEPROM Updates**: The service runs the `rpi-eeprom-update` utility with flags to silently check for and apply available updates.
- **One-Time Execution**: The service is configured to execute only once per boot cycle, ensuring minimal resource usage.
- **Persistence**: The service remains in an "active" state after execution to indicate that it has completed its task.

## Service Configuration

### Unit Section

- **Description**: Provides a brief explanation of the service's purpose.
- **After**: Ensures that the service starts only after the `boot-firmware.mount` target is active. This guarantees that the necessary firmware files are available before attempting an update.

### Service Section

- **Type**: Configured as `oneshot`, meaning the service performs a single task and does not remain running.
- **RemainAfterExit**: Set to `true` to keep the service in an "active" state after it has completed execution. This allows system administrators to verify its status post-execution.
- **ExecStart**: Executes the `rpi-eeprom-update` command with the following flags:
  - `-s`: Silent mode, suppressing unnecessary output.
  - `-a`: Automatically applies any available updates.

### Install Section

- **WantedBy**: Links the service to the `multi-user.target`, ensuring it is started during the system's multi-user initialization phase.

## Installation

1. **Create the Service File**:
   Save the following content to `/etc/systemd/system/rpi-eeprom-update.service`:

   ```ini
   [Unit]
   Description=Check for Raspberry Pi EEPROM updates
   After=boot-firmware.mount

   [Service]
   Type=oneshot
   RemainAfterExit=true
   ExecStart=/usr/bin/rpi-eeprom-update -s -a

   [Install]
   WantedBy=multi-user.target
   ```

2. **Reload Systemd**:
   After creating or updating the service file, reload the systemd manager configuration:

   ```bash
   sudo systemctl daemon-reload
   ```

3. **Enable the Service**:
   Enable the service to run at boot:

   ```bash
   sudo systemctl enable rpi-eeprom-update.service
   ```

4. **Start the Service**:
   To manually start the service, use:

   ```bash
   sudo systemctl start rpi-eeprom-update.service
   ```

## Usage

- **Check Service Status**:
  To verify the status of the service, run:

  ```bash
  sudo systemctl status rpi-eeprom-update.service
  ```

- **Manually Trigger EEPROM Update**:
  If needed, you can manually trigger the EEPROM update by starting the service:

  ```bash
  sudo systemctl start rpi-eeprom-update.service
  ```

- **Disable the Service**:
  If you wish to disable the service from running at boot, use:

  ```bash
  sudo systemctl disable rpi-eeprom-update.service
  ```

## Notes

- The `rpi-eeprom-update` utility is specific to Raspberry Pi devices and is used to manage the bootloader and VL805 firmware.
- Ensure that the `rpi-eeprom-update` utility is installed and available at `/usr/bin/rpi-eeprom-update`. If not, install it using the Raspberry Pi OS package manager:

  ```bash
  sudo apt update
  sudo apt install rpi-eeprom
  ```

- The service assumes that the `boot-firmware` mount point is correctly configured and accessible. Verify your system's configuration if the service fails to start.

## Troubleshooting

- **Service Fails to Start**:
  - Check the logs for detailed error messages:
    ```bash
    journalctl -u rpi-eeprom-update.service
    ```
  - Ensure that the `boot-firmware` mount point is active and accessible.
  - Verify that the `rpi-eeprom-update` utility is installed and executable.

- **EEPROM Update Issues**:
  - Ensure your Raspberry Pi is connected to the internet to download the latest EEPROM updates.
  - Manually run the `rpi-eeprom-update` command to check for errors:
    ```bash
    sudo rpi-eeprom-update
    ```

## References

- [Raspberry Pi Documentation: Bootloader EEPROM](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#bootloader)
- [rpi-eeprom GitHub Repository](https://github.com/raspberrypi/rpi-eeprom)

## License

This service file is provided under the MIT License. See the LICENSE file for details.