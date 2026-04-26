# 🚀 Release Notes

### Changes in `github_pusher.sh`:
1. **Removed `git pull` with rebase**:
   - The new script no longer includes the `git pull origin main --rebase` step before pushing changes. This simplifies the script but removes the safeguard against potential conflicts between local and remote branches.
   
2. **Updated logging messages**:
   - Improved clarity and conciseness of log messages.
   - Removed the "🔄 Syncing local Pi with Cloud AI changes..." message.
   - Updated the "⚠️ Git says there are no new changes to push" message to remove the reference to the "scrubber."

3. **General cleanup**:
   - Removed unnecessary comments and redundant logging.
   - Streamlined the script for better readability and maintainability.

---

# `github_pusher.sh`

## Overview
The `github_pusher.sh` script is a lightweight automation tool designed to streamline the process of staging, committing, and pushing changes from a local staging directory to a GitHub repository. It is particularly useful for automating updates to a portfolio or similar projects.

---

## Features
- Automatically stages all changes in the specified staging directory.
- Checks for new changes before committing to avoid unnecessary commits.
- Pushes committed changes to the `main` branch of the remote GitHub repository.
- Provides clear and concise logging for each step of the process.

---

## Requirements
- **Git**: Ensure Git is installed and properly configured on the system.
- **Access to the repository**: The script assumes that the user has the necessary permissions and SSH keys (or other authentication methods) configured for pushing to the remote repository.
- **Staging directory**: The script operates on a predefined staging directory where changes are made.

---

## Usage

1. **Set up the staging directory**:
   - Ensure that the `STAGING_DIR` variable in the script points to the correct directory where your files are located. By default, it is set to:
     ```
     /home/redwannabil/portfolio_staging
     ```

2. **Run the script**:
   - Execute the script using the following command:
     ```bash
     ./github_pusher.sh
     ```

3. **Script behavior**:
   - The script will:
     1. Navigate to the staging directory.
     2. Stage all changes using `git add --all`.
     3. Check if there are any changes to commit using `git diff --cached --quiet`.
     4. If changes are detected:
        - Commit the changes with a predefined message: `"Auto-Staged new raw scripts via publish command"`.
        - Push the changes to the `main` branch of the remote repository.
     5. If no changes are detected, it will log a message and exit without making any commits or pushes.

---

## Logging
The script provides the following log messages for clarity:
- `❌ Error: Could not change to $STAGING_DIR`: Indicates that the script could not navigate to the specified staging directory.
- `📦 Committing new script...`: Indicates that changes are being committed.
- `☁️ Push successful. The AI is now processing your file!`: Indicates that the push operation was successful.
- `⚠️ Git says there are no new changes to push.`: Indicates that no changes were detected, and no commit or push was performed.

---

## Customization
- **Commit message**:
  - To customize the commit message, modify the following line in the script:
    ```bash
    git commit -m "Auto-Staged new raw scripts via publish command"
    ```
- **Staging directory**:
  - Update the `STAGING_DIR` variable to point to your desired directory:
    ```bash
    STAGING_DIR="/path/to/your/staging_directory"
    ```

---

## Known Limitations
1. **No conflict resolution**:
   - The script does not handle merge conflicts or pull changes from the remote repository before pushing. Ensure that the local branch is up-to-date with the remote branch before running the script.
   
2. **No error handling for `git push`**:
   - If the push operation fails (e.g., due to authentication issues), the script will not retry or provide detailed error messages.

3. **Single branch support**:
   - The script is hardcoded to push changes to the `main` branch. If you need to push to a different branch, you must modify the script.

---

## Future Improvements
- Add support for pulling changes from the remote repository and handling merge conflicts.
- Implement error handling for the `git push` command.
- Allow dynamic configuration of the branch to push to.
- Add logging to a file for better traceability.

---

## License
This script is open-source and can be modified or redistributed under the terms of the MIT License.