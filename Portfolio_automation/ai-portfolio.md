# AI Portfolio Architect Automation

## Overview

The `ai-portfolio.yml` workflow is designed to automate the process of building and updating an AI-driven portfolio using GitHub Actions. This workflow leverages Python and OpenAI's API to dynamically generate portfolio content based on incoming changes. It ensures seamless integration, automated updates, and efficient management of portfolio assets.

---

## Features

- **Automated Portfolio Updates**: Automatically triggers on changes to files in the `incoming/` directory.
- **AI-Driven Content Generation**: Utilizes OpenAI's API to generate portfolio content dynamically.
- **GitHub Native AI Integration**: Commits updates directly to the repository with a clear commit message.
- **Node.js Compatibility**: Prepares for Node.js 24 to silence deprecation warnings for Node.js 20.

---

## Workflow Trigger

The workflow is triggered on `push` events to the repository, specifically when changes are made to files under the `incoming/` directory.

```yaml
on:
  push:
    paths:
      - 'incoming/**'
```

---

## Environment Variables

### Node.js Compatibility
The workflow sets the environment variable `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` to `true` to opt into Node.js 24 early and silence deprecation warnings for Node.js 20.

```yaml
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

### Secrets
The workflow requires a GitHub secret `GH_MODELS_TOKEN` to authenticate and interact with the OpenAI API.

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
```

---

## Workflow Jobs

### 1. `build_portfolio`

This job handles the entire automation process for building and updating the portfolio.

#### **Runs-on**
The job runs on the latest Ubuntu environment.

```yaml
runs-on: ubuntu-latest
```

#### **Permissions**
The job is granted write access to the repository contents to commit changes.

```yaml
permissions:
  contents: write
```

#### **Steps**

1. **Checkout Repository**
   - Uses the `actions/checkout` action to clone the repository.

   ```yaml
   - uses: actions/checkout@v4
   ```

2. **Setup Python**
   - Configures Python 3.10 using the `actions/setup-python` action.

   ```yaml
   - uses: actions/setup-python@v5
     with:
       python-version: '3.10'
   ```

3. **Install Dependencies**
   - Installs the required Python package `openai` for interacting with the OpenAI API.

   ```yaml
   - name: Install Dependencies
     run: pip install openai
   ```

4. **Run AI Architect**
   - Executes the `ai_architect.py` script located in `.github/scripts/` to generate portfolio content. The script uses the `GH_MODELS_TOKEN` secret for authentication.

   ```yaml
   - name: Run AI Architect
     env:
       GITHUB_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
     run: python .github/scripts/ai_architect.py
   ```

5. **Commit Changes**
   - Automatically commits the generated portfolio updates using the `git-auto-commit-action`.

   ```yaml
   - uses: stefanzweifel/git-auto-commit-action@v5
     with:
       commit_message: "🤖 AI Automated Portfolio Build (GitHub Native AI)"
   ```

---

## Prerequisites

1. **GitHub Secrets**:
   - Ensure the `GH_MODELS_TOKEN` secret is configured in your repository settings. This token is required for authenticating with the OpenAI API.

2. **Python Script**:
   - The `ai_architect.py` script must be located in the `.github/scripts/` directory. This script is responsible for generating portfolio content.

3. **Incoming Directory**:
   - Changes to files in the `incoming/` directory will trigger the workflow.

---

## Commit Message

The workflow uses the following commit message for automated updates:

```
🤖 AI Automated Portfolio Build (GitHub Native AI)
```

---

## Usage

1. Push changes to the `incoming/` directory.
2. The workflow will automatically execute, generating and committing portfolio updates.
3. Review the updated portfolio in the repository.

---

## Notes

- Ensure the `ai_architect.py` script is properly configured to handle portfolio generation using OpenAI's API.
- The workflow is designed to be extensible and can be modified to include additional steps or dependencies as needed.

---

## Troubleshooting

- **Missing `GH_MODELS_TOKEN` Secret**:
  Ensure the secret is added to the repository settings under `Settings > Secrets and variables > Actions`.

- **Python Dependency Issues**:
  Verify that the `openai` package is correctly installed and compatible with Python 3.10.

- **Node.js Warnings**:
  The environment variable `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` is set to silence Node.js 20 deprecation warnings. Ensure your actions are compatible with Node.js 24.

---

## License

This workflow is licensed under the [MIT License](LICENSE).