# 🚀 Release Notes

### Changes in `publish` Script
The following updates have been made to the `publish` script in the `Git_portfolio_automation` project:

1. **Absolute Path Handling**:
   - Added a mechanism to capture the absolute path of the file to be published using `realpath`. This ensures that the script can correctly locate the file regardless of the current working directory.

2. **File Existence Check**:
   - Updated the file existence check to use the absolute path (`FILE_ABS`) instead of the relative path. This prevents errors when the script changes directories during execution.

3. **Improved File Copying**:
   - Updated the `cp` command to use the absolute path (`FILE_ABS`) for copying the file to the staging directory. This ensures the correct file is copied even if the working directory changes.

---

# `publish` Script

The `publish` script is a Bash utility designed to automate the process of staging and sanitizing files for publication to a GitHub repository. It ensures that sensitive information is redacted from files before they are pushed to a public repository.

## Features

- **File Staging**: Copies the specified file to a structured staging directory.
- **Sensitive Data Scrubbing**: Automatically redacts sensitive information such as tokens, passwords, API keys, and chat IDs from the file.
- **GitHub Synchronization**: Ensures the local staging directory is in sync with the remote GitHub repository before staging new files.
- **Error Handling**: Provides clear error messages for missing files or invalid inputs.

---

## Prerequisites

1. **Git**: Ensure Git is installed and configured on the system.
2. **Staging Directory**: The script assumes the existence of a staging directory at `/home/redwannabil/portfolio_staging`.
3. **GitHub Pusher Script**: The script relies on an external script located at `/home/redwannabil/github_pusher.sh` to handle the final push to GitHub.

---

## Usage

```bash
./publish <file_to_publish>
```

### Parameters

- `<file_to_publish>`: The path to the file you want to publish. This can be a relative or absolute path.

### Example

```bash
./publish my_project/config.yaml
```

---

## Workflow

1. **Input Validation**:
   - The script checks if a file path is provided as an argument.
   - It verifies that the specified file exists using its absolute path.

2. **Project Folder Name**:
   - Prompts the user to enter a project folder name.
   - Replaces spaces in the folder name with underscores for compatibility.

3. **Git Synchronization**:
   - Navigates to the staging directory.
   - Fetches the latest state of the remote repository.
   - Resets the local repository to match the remote state.
   - Cleans up any untracked files or directories.

4. **File Staging**:
   - Creates a subdirectory in the staging directory based on the project folder name.
   - Copies the specified file to this subdirectory.

5. **Sensitive Data Scrubbing**:
   - Redacts sensitive information from the file using `sed` commands. The following patterns are sanitized:
     - `TOKEN = <value>` → `TOKEN = "REDACTED_BY_SYSADMIN"`
     - `PASSWORD = <value>` → `PASSWORD = "REDACTED_BY_SYSADMIN"`
     - `CHAT_ID = <value>` → `CHAT_ID = "REDACTED_BY_SYSADMIN"`
     - `API_KEY = <value>` → `API_KEY = "REDACTED_BY_SYSADMIN"`
     - `SMB_PASS = <value>` → `SMB_PASS = "REDACTED_BY_SYSADMIN"`

6. **GitHub Push**:
   - Hands off the process to the `github_pusher.sh` script for final publication.

---

## Error Handling

- If no file is provided as an argument, the script displays the usage instructions and exits.
- If the specified file does not exist, the script displays an error message and exits.
- If the script fails to navigate to the staging directory, it exits with an error.

---

## Improvements in This Version

- **Absolute Path Handling**: Ensures the script works correctly regardless of the current working directory.
- **Enhanced File Validation**: Uses the absolute path for file existence checks.
- **Improved File Copying**: Prevents issues caused by changing directories during script execution.

---

## Notes

- Ensure the `github_pusher.sh` script is executable and correctly configured to push changes to the desired GitHub repository.
- The script aggressively resets the local staging directory to match the remote repository. Any untracked files in the staging directory will be deleted during this process. Use with caution.