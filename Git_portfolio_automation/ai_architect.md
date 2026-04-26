# ai_architect.py

## Overview

`ai_architect.py` is a Python script designed to automate the generation of detailed README documentation for scripts added or updated in a project repository. It leverages OpenAI's API to analyze code and generate high-quality documentation in Markdown format. The script is particularly useful for maintaining consistent and comprehensive documentation across multiple projects.

---

## Features

- **Automated README Generation**: Automatically generates detailed README files for new or updated scripts using AI.
- **AI-Powered Analysis**: Utilizes GitHub's native AI models (`gpt-4o` and `gpt-4o-mini`) for code analysis and documentation generation.
- **Retry Mechanism**: Implements a retry mechanism to handle API rate limits or transient errors.
- **Version Comparison**: For updated scripts, compares the old and new code to provide detailed release notes.
- **File Management**: Automatically moves processed scripts to their respective project folders and removes the original files from the incoming directory.
- **Fallback Documentation**: Provides a fallback template for README files in case AI generation fails.

---

## Requirements

- Python 3.8 or higher
- `openai` Python library
- Access to GitHub's internal AI servers with a valid API key

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Git_portfolio_automation.git
   cd Git_portfolio_automation
   ```

2. Install dependencies:
   ```bash
   pip install openai
   ```

3. Set up the `INCOMING_DIR` directory:
   - Create a folder named `incoming` in the root directory of the project.
   - Place the scripts you want to process inside this folder.

4. Configure the OpenAI client:
   - Replace the placeholder `REDACTED_BY_SYSADMIN` in the `api_key` parameter with your actual API key.

---

## Usage

1. Place the scripts you want to process in the `incoming` directory.
2. Run the script:
   ```bash
   python ai_architect.py
   ```
3. The script will:
   - Analyze the scripts in the `incoming` directory.
   - Generate a README file for each script in Markdown format.
   - Move the processed scripts and their corresponding README files to their respective project folders in the root directory.
   - Delete the original files from the `incoming` directory.

---

## Workflow

1. **Input Directory**: The script scans the `incoming` directory for project folders containing scripts.
2. **Script Analysis**:
   - If the script is new, the AI generates a README based on the provided code.
   - If the script is an update, the AI compares the old and new code to generate a README with a `🚀 Release Notes` section.
3. **Retry Mechanism**: If the AI API call fails due to rate limits or other errors, the script retries up to three times with exponential backoff.
4. **Output**:
   - The processed script is moved to its respective project folder in the root directory.
   - A README file in Markdown format is created in the same folder.
5. **Cleanup**: The original files in the `incoming` directory are deleted after processing.

---

## File Structure

After running the script, the project directory will be organized as follows:

```
Git_portfolio_automation/
│
├── incoming/                # Directory for unprocessed scripts
│   ├── project1/
│   │   ├── script1.py
│   │   ├── script2.py
│   │   └── ...
│   └── project2/
│       ├── script3.py
│       └── ...
│
├── project1/                # Processed project folder
│   ├── script1.py
│   ├── script1.md           # Auto-generated README
│   ├── script2.py
│   ├── script2.md           # Auto-generated README
│   └── ...
│
├── project2/                # Processed project folder
│   ├── script3.py
│   ├── script3.md           # Auto-generated README
│   └── ...
│
├── ai_architect.py          # Main script
└── requirements.txt         # Python dependencies
```

---

## Error Handling

- **Rate Limiting**: If the AI API returns a rate limit error (HTTP 429), the script will retry the request up to three times with exponential backoff.
- **Fallback Documentation**: If AI generation fails after all retries, the script generates a basic README template indicating that manual documentation is required.

---

## Configuration

- **INCOMING_DIR**: The directory where new or updated scripts are placed for processing. Default is `incoming`.
- **ROOT_DIR**: The root directory where processed project folders and scripts are stored. Default is the current directory (`.`).
- **MODELS_TO_TRY**: A list of AI models to use for documentation generation. Default is `['gpt-4o', 'gpt-4o-mini']`.

---

## Limitations

- Requires access to GitHub's internal AI servers and a valid API key.
- AI-generated documentation may require manual review and editing for accuracy.
- The script assumes a specific directory structure and may not work as intended if the structure is altered.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear and concise messages.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or support, please contact the repository maintainer:

- **Name**: [Your Name]
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile]