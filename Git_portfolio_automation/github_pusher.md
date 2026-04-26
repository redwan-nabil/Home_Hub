# GitHub Pusher Script (`github_pusher.sh`)

## Overview

The `github_pusher.sh` script is a utility designed to automate the process of staging, committing, and pushing changes from a local directory to a GitHub repository. It is specifically tailored for use in the `Git_portfolio_automation` project, ensuring that any updates made in the local staging directory are synchronized with the remote repository.

This script is particularly useful for automating workflows where frequent updates to a repository are required, such as managing a portfolio or deploying changes from a local environment to a remote GitHub repository.

---

## Features

- **Automated Staging**: Automatically stages all changes (new files, modifications, deletions) in the specified directory.
- **Change Detection**: Checks if there are any changes to commit before proceeding, avoiding unnecessary commits and pushes.
- **Commit Automation**: Commits changes with a predefined message for consistency.
- **Rebase and Pull**: Ensures the local branch is synchronized with the remote branch by pulling the latest changes with a rebase.
- **Push to GitHub**: Pushes committed changes to the `main` branch of the remote repository.
- **Error Handling**: Includes basic error handling to ensure smooth execution and provide meaningful feedback in case of issues.

---

## Prerequisites

Before using this script, ensure the following:

1. **Git Installed**: Git must be installed on the system. You can verify this by running `git --version`.
2. **Configured Git Repository**:
   - The `STAGING_DIR` directory must be a valid Git repository.
   - The repository should have a remote named `origin` pointing to the desired GitHub repository.
3. **Authentication**:
   - Ensure that the system is authenticated with GitHub. This can be done using SSH keys or a personal access token.
4. **Write Permissions**: The user running the script must have write permissions for the `STAGING_DIR` directory.

---

## Script Details

### 1. **Define Staging Directory**
The script begins by defining the absolute path to the staging directory:
```bash
STAGING_DIR="/home/redwannabil/portfolio_staging"
```
This directory is where the local Git repository resides. Update this path as needed to point to your specific staging directory.

### 2. **Navigate to Staging Directory**
The script attempts to change into the specified directory:
```bash
cd "$STAGING_DIR" || { echo "❌ Error: Could not change to $STAGING_DIR"; exit 1; }
```
If the directory does not exist or is inaccessible, the script exits with an error message.

### 3. **Stage All Changes**
The script stages all changes (new files, modifications, deletions) in the repository:
```bash
git add --all
```

### 4. **Check for Changes**
Before committing, the script checks if there are any changes to commit:
```bash
if ! git diff --cached --quiet; then
```
If no changes are detected, the script exits with a message:
```bash
echo "⚠️ Git says there are no new changes to push. Did the scrubber fail?"
```

### 5. **Commit Changes**
If changes are detected, the script commits them with a predefined message:
```bash
git commit -m "Auto-Staged new raw scripts via publish command"
```

### 6. **Rebase with Remote Changes**
To ensure the local branch is up-to-date with the remote branch, the script performs a `git pull` with the `--rebase` option:
```bash
git pull origin main --rebase
```

### 7. **Push Changes to GitHub**
Finally, the script pushes the committed changes to the `main` branch of the remote repository:
```bash
git push origin main
```
If the push is successful, a confirmation message is displayed:
```bash
echo "☁️ Push successful."
```

---

## Usage

1. Clone this repository (if not already cloned):
   ```bash
   git clone <repository-url>
   ```

2. Update the `STAGING_DIR` variable in the script to point to your local staging directory:
   ```bash
   STAGING_DIR="/path/to/your/staging/directory"
   ```

3. Make the script executable:
   ```bash
   chmod +x github_pusher.sh
   ```

4. Run the script:
   ```bash
   ./github_pusher.sh
   ```

---

## Error Handling

- **Directory Access Error**: If the script cannot access the `STAGING_DIR`, it will exit with the message:
  ```
  ❌ Error: Could not change to /path/to/staging/directory
  ```

- **No Changes to Commit**: If no changes are detected, the script will display:
  ```
  ⚠️ Git says there are no new changes to push. Did the scrubber fail?
  ```

- **Git Errors**: Any errors from Git commands (e.g., `git pull`, `git push`) will be displayed in the terminal.

---

## Customization

- **Commit Message**: Update the commit message in the following line to suit your needs:
  ```bash
  git commit -m "Auto-Staged new raw scripts via publish command"
  ```

- **Branch Name**: If you are using a branch other than `main`, update the branch name in the `git pull` and `git push` commands:
  ```bash
  git pull origin <your-branch-name> --rebase
  git push origin <your-branch-name>
  ```

---

## Notes

- This script assumes that the `main` branch is the default branch for the repository. If your repository uses a different default branch (e.g., `master`), update the branch name in the script.
- Ensure that the `STAGING_DIR` is a valid Git repository before running the script.
- The script does not handle merge conflicts. If a conflict occurs during the `git pull --rebase` step, manual intervention will be required to resolve it.

---

## Disclaimer

Use this script at your own risk. Ensure you have proper backups and understand the implications of automated Git operations, especially when using `--rebase` and `--force` options.