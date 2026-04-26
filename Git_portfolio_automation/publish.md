# Git Portfolio Automation - `publish` Script

The `publish` script is a Bash utility designed to automate the process of publishing files to a GitHub repository while ensuring sensitive information is sanitized. This script is part of the `Git_portfolio_automation` project and is intended to streamline the workflow of staging and pushing files to a public GitHub repository.

---

## Features

- **File Validation**: Ensures the file to be published exists before proceeding.
- **Dynamic Project Folder Creation**: Prompts the user to specify a project folder name, which is sanitized to replace spaces with underscores.
- **Git Syncing**: Automatically pulls the latest changes from the `main` branch of the repository to ensure the staging directory is up-to-date.
- **Sensitive Data Scrubbing**: Automatically redacts sensitive information such as tokens, passwords, chat IDs, API keys, and SMB passwords from the file before publishing.
- **File Staging**: Copies the sanitized file to a designated staging directory for further processing.
- **GitHub Integration**: Hands off the staged file to a separate script (`github_pusher.sh`) for committing and pushing to the GitHub repository.

---

## Prerequisites

Before using the `publish` script, ensure the following:

1. **Git Configuration**:
   - The staging directory (`/home/redwannabil/portfolio_staging`) must be a valid Git repository.
   - The repository should have a `main` branch configured for pulling updates.

2. **Dependencies**:
   - The script relies on a secondary script located at `/home/redwannabil/github_pusher.sh` to handle the GitHub push process. Ensure this script is present and executable.

3. **Permissions**:
   - The user must have write permissions for the staging directory (`/home/redwannabil/portfolio_staging`) and its subdirectories.
   - The `publish` script itself must have executable permissions.

4. **Environment**:
   - The script is designed to run on a Unix-like environment with Bash installed.

---

## Installation

1. Clone the `Git_portfolio_automation` repository to your local machine.
2. Place the `publish` script in a directory included in your system's `PATH` or execute it directly from its location.
3. Ensure the script has executable permissions:
   ```bash
   chmod +x publish
   ```

---

## Usage

To use the `publish` script, follow these steps:

1. Open a terminal.
2. Run the script with the file you want to publish as an argument:
   ```bash
   publish <file_to_publish>
   ```
   Replace `<file_to_publish>` with the path to the file you want to publish.

3. The script will prompt you to enter the project folder name. This name will be used to organize the file in the staging directory. Spaces in the folder name will be replaced with underscores.

4. The script will:
   - Validate the existence of the file.
   - Sync the staging directory with the latest changes from the `main` branch of the GitHub repository.
   - Sanitize the file by redacting sensitive information.
   - Copy the sanitized file to the appropriate location in the staging directory.
   - Trigger the `github_pusher.sh` script to commit and push the changes to GitHub.

---

## Example

```bash
$ publish my_script.py
📁 Enter the Project Folder name: My Awesome Project
🔄 Syncing with Cloud AI...
Already up to date.
🛡️ Sanitizing 'my_script.py' for public GitHub...
✅ Scrubbing complete. 'my_script.py' safely staged.
🚀 Handing off to GitHub Pusher...
```

---

## Script Workflow

1. **Input Validation**:
   - Checks if a file path is provided as an argument.
   - Verifies that the specified file exists.

2. **Project Folder Setup**:
   - Prompts the user for a project folder name.
   - Replaces spaces in the folder name with underscores.

3. **Git Sync**:
   - Navigates to the staging directory.
   - Pulls the latest changes from the `main` branch using `git pull --rebase`.
   - Removes any residual files in the `incoming` directory.

4. **File Staging**:
   - Creates a new directory under `incoming` with the specified project folder name.
   - Copies the file to the newly created directory.

5. **Sensitive Data Scrubbing**:
   - Uses `sed` to redact sensitive information in the file, including:
     - Tokens (`TOKEN`)
     - Passwords (`PASSWORD`)
     - Chat IDs (`CHAT_ID`)
     - API Keys (`API_KEY`)
     - SMB Passwords (`SMB_PASS`)

6. **GitHub Push**:
   - Calls the `github_pusher.sh` script to handle the GitHub commit and push process.

---

## Error Handling

- If no file is provided as an argument, the script displays usage instructions and exits.
- If the specified file does not exist, the script displays an error message and exits.
- Any issues during the Git sync or file staging process will result in appropriate error messages.

---

## Notes

- The script assumes that the `github_pusher.sh` script is correctly configured to handle GitHub operations.
- The sanitization process uses regular expressions to redact sensitive information. Ensure that the patterns match the format of sensitive data in your files.

---

## License

This script is part of the `Git_portfolio_automation` project and is licensed under the MIT License. See the LICENSE file in the repository for more details.

---

## Author

Developed by **redwannabil**. For questions or support, please contact [redwannabil@example.com](mailto:redwannabil@example.com).