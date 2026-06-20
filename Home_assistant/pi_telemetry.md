# pi_telemetry.service

## Overview
The `pi_telemetry.service` is a systemd service designed to run a Raspberry Pi hardware telemetry agent. This service executes a script (`pi_telemetry.sh`) that collects and processes telemetry data from the Raspberry Pi hardware. The service ensures that the telemetry script runs continuously and restarts automatically in case of failure.

## Features
- **Automatic Startup**: The service starts automatically after the network becomes available.
- **Continuous Operation**: The service is configured to restart automatically if it stops or crashes.
- **User-Specific Execution**: Runs under the `redwannabil` user account for security and isolation.
- **Multi-User Target**: The service is enabled for the multi-user target, ensuring it runs in a non-graphical environment.

## Prerequisites
Before enabling and starting the service, ensure the following:
1. The `pi_telemetry.sh` script is located at `/home/redwannabil/pi_telemetry.sh`.
2. The script has executable permissions (`chmod +x /home/redwannabil/pi_telemetry.sh`).
3. The `redwannabil` user exists on the system and has the necessary permissions to execute the script.

## Installation

### Step 1: Create the Service File
1. Navigate to the systemd service directory:
   ```bash
   sudo nano /etc/systemd/system/pi_telemetry.service
   ```
2. Copy and paste the following content into the file:
   ```ini
   [Unit]
   Description=Raspberry Pi Hardware Telemetry Agent
   After=network.target

   [Service]
   ExecStart=/bin/bash /home/redwannabil/pi_telemetry.sh
   Restart=always
   User=redwannabil

   [Install]
   WantedBy=multi-user.target
   ```

3. Save and exit the file.

### Step 2: Reload Systemd
Reload the systemd manager configuration to recognize the new service:
```bash
sudo systemctl daemon-reload
```

### Step 3: Enable the Service
Enable the service to start automatically on boot:
```bash
sudo systemctl enable pi_telemetry.service
```

### Step 4: Start the Service
Start the service immediately:
```bash
sudo systemctl start pi_telemetry.service
```

## Usage

### Check Service Status
To verify the status of the service:
```bash
sudo systemctl status pi_telemetry.service
```

### Stop the Service
To stop the service:
```bash
sudo systemctl stop pi_telemetry.service
```

### Restart the Service
To restart the service:
```bash
sudo systemctl restart pi_telemetry.service
```

### Disable the Service
To disable the service from starting on boot:
```bash
sudo systemctl disable pi_telemetry.service
```

## Logs
The service logs can be viewed using the `journalctl` command:
```bash
sudo journalctl -u pi_telemetry.service
```

## Troubleshooting
- **Script Not Found**: Ensure the `pi_telemetry.sh` script exists at `/home/redwannabil/pi_telemetry.sh` and has executable permissions.
- **User Permissions**: Verify that the `redwannabil` user has the necessary permissions to execute the script.
- **Service Fails to Start**: Check the logs using `journalctl` for detailed error messages.

## Notes
- The service is dependent on the network being available (`After=network.target`). Ensure the network is properly configured on the Raspberry Pi.
- If modifications are made to the service file, always reload the systemd manager configuration using `sudo systemctl daemon-reload`.

## License
This service file is provided as-is and can be modified to suit your specific requirements. Ensure proper testing before deploying in production environments.