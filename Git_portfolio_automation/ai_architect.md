# 🚀 Release Notes

### Changes in `ai_architect.py`:
1. **Enhanced Error Handling**:
   - Improved error handling in the `call_ai_with_retry` function to better manage rate-limiting scenarios by implementing exponential backoff (`2 ** attempt`).
   - Added detailed logging for errors, including specific messages for rate-limiting.

2. **Improved AI Response Parsing**:
   - Enhanced the parsing of AI-generated responses to handle cases where the response might be wrapped in code blocks (` ```markdown ` or ` ``` `).

3. **Fallback Documentation**:
   - Introduced a fallback mechanism to generate a basic README template when AI response generation fails. This ensures that a placeholder README is always created.

4. **Code Refactoring**:
   - Improved code readability and maintainability by adding comments and restructuring logic for clarity.
   - Consolidated redundant code for better maintainability.

5. **New Features**:
   - Added functionality to create a README file for each processed script, with the filename derived from the script's base name.
   - Enhanced the prompt to include instructions for generating a `🚀 Release Notes` section when updating existing scripts.

---

# Git Portfolio Automation - `ai_architect.py`

## Overview

The `ai_architect.py` script is a core component of the `Git_portfolio_automation` project. It automates the process of integrating new or updated scripts into project directories, generates detailed documentation in Markdown format, and ensures a seamless workflow for managing incoming scripts.

This script leverages GitHub's internal AI models to generate detailed README files for each script, providing a comprehensive overview of the code's functionality, usage, and changes. In cases where AI generation fails, a fallback mechanism ensures that a basic README template is created.

---

## Features

1. **Automated Script Processing**:
   - Automatically detects new or updated scripts in the `incoming` directory.
   - Moves scripts to their respective project directories under the root directory.

2. **AI-Powered Documentation**:
   - Uses GitHub's internal AI models (`gpt-4o` and `gpt-4o-mini`) to generate detailed README files for each script.
   - Includes a `🚀 Release Notes` section for updated scripts, highlighting changes from the previous version.

3. **Error Handling and Retry Mechanism**:
   - Implements a robust retry mechanism with exponential backoff for handling API rate limits and other transient errors.
   - Logs detailed error messages for debugging and monitoring.

4. **Fallback Documentation**:
   - Ensures that a basic README template is generated even if AI response generation fails.

5. **Customizable AI Models**:
   - Supports multiple AI models, allowing users to configure and prioritize models for generating documentation.

---

## Directory Structure

The script operates on the following directory structure:

```
.
├── incoming/
│   ├── project1/
│   │   ├── script1.py
│   │   ├── script2.py
│   ├── project2/
│       ├── script3.py
├── project1/
│   ├── script1.py
│   ├── script1.md
│   ├── script2.py
│   ├── script2.md
├── project2/
│   ├── script3.py
│   ├── script3.md
```

- **`incoming/`**: Temporary directory where new or updated scripts are placed for processing.
- **`project1/`, `project2/`, etc.**: Project directories where scripts are moved after processing.
- **`.md` files**: Generated README files for each script.

---

## How It Works

1. **Script Detection**:
   - The script scans the `incoming` directory for project folders containing new or updated scripts.

2. **AI Documentation Generation**:
   - For each script, the script generates a prompt for the AI model, including the script's content and, if applicable, the old version of the code.
   - The AI model generates a detailed README in Markdown format.

3. **Fallback Mechanism**:
   - If AI generation fails, a basic README template is created, indicating that manual documentation is required.

4. **File Management**:
   - The script moves processed scripts to their respective project directories.
   - The `incoming` directory is cleaned up after processing.

---

## Configuration

### AI Model Configuration

The script uses GitHub's internal AI models for documentation generation. The following models are currently supported:

- `gpt-4o`
- `gpt-4o-mini`

You can modify the `MODELS_TO_TRY` list to prioritize or add additional models.

### API Authentication

The script requires an API key to authenticate with GitHub's internal AI servers. The API key should be set in the `api_key` parameter when initializing the `OpenAI` client. Ensure that the API key is securely stored and not exposed in the code.

---

## Usage

1. Place new or updated scripts in the `incoming` directory, organized into project-specific subdirectories.
2. Run the script:
   ```bash
   python ai_architect.py
   ```
3. The script will process the scripts, move them to their respective project directories, and generate README files.

---

## Error Handling

- **Rate Limiting**:
  - If the AI API returns a rate-limiting error (HTTP 429), the script will retry the request with an exponential backoff strategy.

- **AI Generation Failure**:
  - If the AI fails to generate a response after three attempts, a fallback README template will be created.

---

## Dependencies

- Python 3.8+
- `openai` Python library
- File system access for reading/writing files and directories

Install dependencies using pip:

```bash
pip install openai
```

---

## Limitations

- The script relies on GitHub's internal AI models, which may not be accessible to all users.
- The fallback README template is generic and may require manual updates for detailed documentation.

---

## Future Enhancements

1. Add support for additional AI models and APIs.
2. Implement logging to a file for better traceability.
3. Add unit tests for improved reliability and maintainability.
4. Introduce a configuration file for easier customization of paths and settings.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.