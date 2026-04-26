# AI Portfolio Architect

The `AI Portfolio Architect` is a GitHub Actions workflow designed to automate the generation and management of an AI-driven portfolio. This workflow is triggered by changes in the `incoming/` directory, processes the updates using an AI script, and commits the results back to the repository.

## Features

- **Automated Portfolio Updates**: Automatically processes files in the `incoming/` directory to update the portfolio using AI.
- **AI Integration**: Leverages OpenAI's API to generate or modify portfolio content.
- **GitHub Native Automation**: Uses GitHub Actions to streamline the workflow, including automated commits.
- **Node.js Compatibility**: Prepares for Node.js 24 compatibility by silencing Node.js 20 deprecation warnings.

---

## Workflow Overview

### Trigger

The workflow is triggered on a `push` event to the `incoming/` directory:

```yaml
on:
  push:
    paths:
      - 'incoming/**'
```

### Environment Variables

The workflow sets the following environment variable to ensure compatibility with Node.js 24:

```yaml
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

### Jobs

#### 1. **build_portfolio**

This job runs the portfolio automation process. Below are the steps involved:

1. **Checkout Repository**  
   The repository is checked out using the `actions/checkout@v4` action:
   ```yaml
   - uses: actions/checkout@v4
   ```

2. **Setup Python**  
   Python 3.10 is installed and configured using the `actions/setup-python@v5` action:
   ```yaml
   - uses: actions/setup-python@v5
     with:
       python-version: '3.10'
   ```

3. **Install Dependencies**  
   The required Python dependencies are installed. Currently, the workflow installs the `openai` library:
   ```yaml
   - name: Install Dependencies
     run: pip install openai
   ```

4. **Run AI Architect Script**  
   The core AI script (`ai_architect.py`) is executed. This script processes the files in the `incoming/` directory and generates the updated portfolio. The script uses the `GH_MODELS_TOKEN` secret for authentication:
   ```yaml
   - name: Run AI Architect
     env:
       GITHUB_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
     run: python .github/scripts/ai_architect.py
   ```

5. **Auto-Commit Changes**  
   The `stefanzweifel/git-auto-commit-action@v5` action is used to automatically commit the changes made by the AI script back to the repository:
   ```yaml
   - uses: stefanzweifel/git-auto-commit-action@v5
     with:
       commit_message: "🤖 AI Automated Portfolio Build (GitHub Native AI)"
   ```

---

## Prerequisites

1. **GitHub Repository**  
   Ensure that the repository contains the following:
   - An `incoming/` directory for new files or updates.
   - The AI script located at `.github/scripts/ai_architect.py`.

2. **Secrets**  
   Add the following secret to your repository:
   - `GH_MODELS_TOKEN`: A GitHub token with appropriate permissions for accessing the repository.

3. **Python Environment**  
   The AI script requires Python 3.10 and the `openai` library. These are automatically installed by the workflow.

---

## How to Use

1. Add or update files in the `incoming/` directory of your repository.
2. Push the changes to the repository.
3. The workflow will automatically trigger, process the files using the AI script, and commit the updated portfolio back to the repository.

---

## Customization

- **Python Version**: Update the `python-version` field in the `setup-python` step to use a different Python version.
- **Dependencies**: Modify the `Install Dependencies` step to include additional Python libraries if required by your AI script.
- **Commit Message**: Customize the commit message in the `git-auto-commit-action` step.

---

## Troubleshooting

- **Workflow Fails at "Run AI Architect" Step**:  
  Ensure that the `GH_MODELS_TOKEN` secret is correctly configured and has the necessary permissions.
  
- **Dependencies Not Found**:  
  Verify that the required dependencies are listed in the `Install Dependencies` step.

- **Node.js Deprecation Warnings**:  
  The workflow sets the `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` environment variable to address Node.js 20 deprecation warnings. If issues persist, ensure that all actions used in the workflow are compatible with Node.js 24.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).