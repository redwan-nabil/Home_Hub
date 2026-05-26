# README for `Pi_server_Core` - Hostname Configuration Script

## Overview

This script is designed to add or update the `hostname` configuration in the `Pi_server_Core` system. The hostname is a critical component in network identification and communication. This script ensures that the hostname is correctly set or updated as needed.

## Features

- **Add New Hostname**: If no hostname is currently configured, the script allows you to set a new hostname for the system.
- **Update Existing Hostname**: If a hostname already exists, the script updates it to the desired value.
- **Validation**: Ensures that the provided hostname adheres to standard naming conventions.
- **Automation**: Simplifies the process of managing the hostname configuration for `Pi_server_Core`.

## Prerequisites

Before running this script, ensure the following:

1. You have administrative privileges on the system.
2. The `Pi_server_Core` environment is properly set up and running.
3. Python (or the required scripting language) is installed on the system.
4. The script file is executable. If not, you can make it executable using:
   ```bash
   chmod +x <script_name>
   ```

## Installation

1. Clone the repository or download the script file to your local machine:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the directory containing the script:
   ```bash
   cd Pi_server_Core
   ```

## Usage

### Running the Script

1. Execute the script using the following command:
   ```bash
   ./<script_name>
   ```
   Replace `<script_name>` with the actual name of the script file.

2. Follow the on-screen prompts to either add a new hostname or update the existing one.

### Example

- To set a new hostname:
  ```bash
  ./<script_name>
  ```
  Enter the desired hostname when prompted.

- To update an existing hostname:
  ```bash
  ./<script_name>
  ```
  Enter the new hostname when prompted.

### Script Behavior

- The script will first check if a hostname is already configured.
- If a hostname exists, it will prompt the user to confirm whether they want to update it.
- If no hostname exists, the script will prompt the user to enter a new hostname.
- The script will validate the entered hostname to ensure it meets the following criteria:
  - Contains only alphanumeric characters and hyphens (`-`).
  - Does not start or end with a hyphen.
  - Is not longer than 63 characters.

## Error Handling

- If an invalid hostname is entered, the script will display an error message and prompt the user to enter a valid hostname.
- If the script encounters any issues while updating the hostname, it will provide a detailed error message and log the issue for troubleshooting.

## Logs

The script generates a log file (`hostname_update.log`) in the same directory. This log file contains details of all hostname changes, including timestamps and any errors encountered.

## Troubleshooting

- **Permission Denied**: Ensure you have the necessary permissions to execute the script. Use `chmod +x <script_name>` to make the script executable.
- **Invalid Hostname**: Ensure the hostname you enter meets the validation criteria.
- **Script Errors**: Check the `hostname_update.log` file for detailed error messages.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please submit a pull request or open an issue in the repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or support, please contact the maintainer at [your_email@example.com].