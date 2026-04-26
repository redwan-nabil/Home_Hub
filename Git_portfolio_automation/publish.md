# 🚀 Release Notes

### Changes in `publish` Script
1. **Aggressive Sync with Cloud AI**:
   - Replaced `git pull origin main --rebase` with `git fetch origin`, `git reset --hard origin/main`, and `git clean -fd` for a more aggressive sync strategy. This ensures the local repository matches the remote repository exactly, removing any untracked files or changes.
   - Removed the `rm -rf "$STAGING_DIR/incoming/*"` command, as the aggressive sync now handles cleaning up untracked files.

2. **Improved Error Handling**:
   - Added `|| exit 1` to the `cd` command to prevent further execution if changing directories fails.

3. **No Functional Changes to Sanitization**:
   - The sanitization logic for sensitive data (e.g., tokens, passwords, API keys) remains unchanged.

---

# `publish` Script

The `publish` script is a utility for automating the process of staging and publishing files to a GitHub repository. It ensures that sensitive information is sanitized before uploading files to a public repository.

## Features
- **File Validation**: Ensures the specified file exists before proceeding.
- **Project Folder Input**: Prompts the user to specify a project folder name, which is sanitized to replace spaces with underscores.
- **Aggressive Git Sync**: Ensures the local staging directory matches the remote repository exactly by performing a hard reset and cleaning untracked files.
- **Sensitive Data Scrubbing**: Automatically redacts sensitive information (e.g., tokens, passwords, API keys) from the file before staging.
- **GitHub Integration**: Hands off the sanitized file to a separate script (`github_pusher.sh`) for publishing to GitHub.

## Prerequisites
- A valid GitHub repository configured as the remote for the staging directory.
- The `github_pusher.sh` script must be available and executable at `/home/redwannabil/github_pusher.sh`.
- The staging directory must exist at `/home/redwannabil/portfolio_staging`.

## Usage
```bash
publish <file_to_publish>
```

### Example
```bash
./publish my_script.sh
```

1. The script will prompt you to enter a project folder name. For example:
   ```
   📁 Enter the Project Folder name: My Project
   ```
   The folder name will be sanitized to `My_Project`.

2. The script will validate the existence of the specified file. If the file does not exist, it will terminate with an error:
   ```
   ❌ Error: File 'my_script.sh' does not exist.
   ```

3. The script will perform an aggressive sync with the remote GitHub repository:
   - Fetch the latest changes from the remote repository.
   - Reset the local repository to match the remote repository exactly.
   - Remove any untracked files or directories.

4. The script will create a staging folder for the project (e.g., `/home/redwannabil/portfolio_staging/incoming/My_Project`) and copy the specified file into it.

5. The script will sanitize the file by redacting sensitive information such as tokens, passwords, and API keys:
   - `TOKEN = ...` → `TOKEN = "REDACTED_BY_SYSADMIN"`
   - `PASSWORD = ...` → `PASSWORD = "REDACTED_BY_SYSADMIN"`
   - `CHAT_ID = ...` → `CHAT_ID = "REDACTED_BY_SYSADMIN"`
   - `API_KEY = ...` → `API_KEY = "REDACTED_BY_SYSADMIN"`
   - `SMB_PASS = ...` → `SMB_PASS = "REDACTED_BY_SYSADMIN"`

6. The script will confirm that the file has been sanitized and staged:
   ```
   ✅ Scrubbing complete. 'my_script.sh' safely staged.
   ```

7. Finally, the script will hand off the sanitized file to the `github_pusher.sh` script for publishing:
   ```
   🚀 Handing off to GitHub Pusher...
   ```

## Error Handling
- If no file is specified, the script will display usage instructions and exit:
  ```
  Usage: publish <file_to_publish>
  ```
- If the specified file does not exist, the script will terminate with an error:
  ```
  ❌ Error: File '<file_to_publish>' does not exist.
  ```
- If the script fails to change to the staging directory, it will terminate with an error:
  ```
  ❌ Error: Failed to change to staging directory.
  ```

## File Sanitization
The script uses `sed` with regular expressions to redact sensitive information from the file. The following patterns are targeted:
- `TOKEN`
- `PASSWORD`
- `CHAT_ID`
- `API_KEY`
- `SMB_PASS`

Each of these patterns is replaced with the string `"REDACTED_BY_SYSADMIN"`.

## Notes
- The aggressive sync strategy (`git reset --hard` and `git clean -fd`) ensures that the local repository is an exact match of the remote repository. Be cautious, as this will discard any uncommitted changes or untracked files in the local repository.
- Ensure that the `github_pusher.sh` script is properly configured to handle the final push to GitHub.

## License
This script is licensed under the MIT License.