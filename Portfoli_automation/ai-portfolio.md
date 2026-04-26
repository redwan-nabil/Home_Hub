# AI Portfolio Architect Automation

## Overview

The `ai-portfolio.yml` workflow is designed to automate the process of building and updating an AI-powered portfolio using GitHub Actions. This workflow leverages Python and OpenAI's API to dynamically generate portfolio content based on incoming changes. The automation ensures seamless integration, efficient updates, and version control for portfolio-related files.

---

## Features

- **Automated Portfolio Updates**: Automatically builds and updates the portfolio whenever changes are pushed to the `incoming/` directory.
- **AI Integration**: Utilizes OpenAI's API to generate portfolio content dynamically.
- **Version Control**: Commits changes directly to the repository using GitHub Actions.
- **Node.js Compatibility**: Explicitly opts into Node.js 24 to silence deprecation warnings for Node.js 20.

---

## Workflow Trigger

The workflow is triggered on a `push` event to the repository, specifically when changes are made to files in the `incoming/` directory:

```yaml
on:
  push:
    paths:
      - 'incoming/**'
```

---

## Environment Variables

The workflow sets the following environment variable:

- `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`: Ensures compatibility with Node.js 24, silencing deprecation warnings for Node.js 20.

---

## Workflow Jobs

### 1. **Build Portfolio**

The `build_portfolio` job is responsible for executing the portfolio automation process. It runs on the latest Ubuntu environment (`ubuntu-latest`) and has write permissions for repository contents.

#### Steps:

1. **Checkout Repository**:
   - Uses the `actions/checkout@v4` action to clone the repository and access its contents.

   ```yaml
   - uses: actions/checkout@v4
   ```

2. **Setup Python**:
   - Configures Python 3.10 using the `actions/setup-python@v5` action.

   ```yaml
   - uses: actions/setup-python@v5
     with:
       python-version: '3.10'
   ```

3. **Install Dependencies**:
   - Installs the `openai` Python package, which is required for AI integration.

   ```yaml
   - name: Install Dependencies
     run: pip install openai
   ```

4. **Run AI Architect**:
   - Executes the `ai_architect.py` script located in the `.github/scripts/` directory. This script utilizes OpenAI's API to generate portfolio content.
   - Requires the `GH_MODELS_TOKEN` secret for authentication.

   ```yaml
   - name: Run AI Architect
     env:
       GITHUB_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
     run: python .github/scripts/ai_architect.py
   ```

5. **Auto Commit Changes**:
   - Uses the `stefanzweifel/git-auto-commit-action@v5` action to automatically commit changes made by the AI script to the repository.
   - The commit message is set to: "🤖 AI Automated Portfolio Build (GitHub Native AI)".

   ```yaml
   - uses: stefanzweifel/git-auto-commit-action@v5
     with:
       commit_message: "🤖 AI Automated Portfolio Build (GitHub Native AI)"
   ```

---

## Requirements

### Secrets

- **GH_MODELS_TOKEN**: A GitHub secret token required for authenticating the AI script. Ensure this token has the necessary permissions to access the repository.

### Dependencies

- **Python 3.10**: The workflow requires Python 3.10 to run the AI script.
- **OpenAI Python Library**: The `openai` library must be installed for the AI script to function.

---

## Usage

1. **Setup Repository**:
   - Add the `ai-portfolio.yml` file to the `.github/workflows/` directory of your repository.
   - Place the `ai_architect.py` script in the `.github/scripts/` directory.

2. **Configure Secrets**:
   - Add the `GH_MODELS_TOKEN` secret to your repository settings.

3. **Push Changes**:
   - Push changes to the `incoming/` directory to trigger the workflow.

4. **Monitor Workflow**:
   - Check the Actions tab in your repository to monitor the workflow execution.

---

## Commit Message

The workflow automatically commits changes with the following message:

```
🤖 AI Automated Portfolio Build (GitHub Native AI)
```

---

## Notes

- Ensure the `ai_architect.py` script is correctly configured to interact with OpenAI's API and generate portfolio content.
- The workflow is designed to run on `ubuntu-latest` and may require modifications for other environments.
- Test the workflow in a staging environment before deploying it to production.

---

## License

This workflow is licensed under the terms of your repository's license. Ensure compliance with OpenAI's API usage policies when using this workflow.