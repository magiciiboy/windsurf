# Python Standards Checker

A CLI tool to check Python standards in GitLab repositories.

## Project Structure

```
src/
└── python_standards_checker/
    ├── __init__.py
    ├── constants.py
    ├── standards/
    │   ├── __init__.py
    │   ├── base.py
    │   ├── python_version.py
    │   ├── project_spec.py
    │   ├── makefile.py
    │   ├── no_conda.py
    │   └── lock_file.py
    └── cli.py

tests/
├── unit/
├── integration/
│   └── test_python_standards_checker.py
└── __init__.py

pyproject.toml
README.md
```

## Installation

```bash
# Using Makefile
make venv    # Create virtual environment
make install # Install dependencies

# Or manually
pip install -e .

# Or install the package
pip install .
```

## Usage

```bash
# Check GitLab repository
python-standards-checker <project_id> [--token <gitlab_token>] [--url <gitlab_url>]

# Check local directory
python-standards-checker <directory_path> --directory
```

### Environment Variables

- `GITLAB_TOKEN`: GitLab private token (for GitLab mode)
- `GITLAB_URL`: GitLab instance URL (defaults to https://gitlab.com) (for GitLab mode)

```bash
export GITLAB_TOKEN=your_token_here
export GITLAB_URL=your_gitlab_url
```

## Standards Checked

The tool currently checks the following standards:

1. **Python Version (PY001)**
   - Category: Version
   - Standard: Python version MUST be at least 3.9
   - Severity: CRITICAL
   - Checks for Python version in setup.py or Dockerfile

2. **Project Specification (PY002)**
   - Category: Project Structure
   - Standard: Project MUST have a project specification
   - Severity: CRITICAL
   - Checks for the presence of pyproject.toml file

3. **Makefile (PY003)**
   - Category: Project Structure
   - Standard: Project SHOULD have Makefile at root level
   - Severity: RECOMMENDATION
   - Checks for the presence of Makefile

4. **No Conda (PY004)**
   - Category: Package Management
   - Standard: Project MUST NOT use conda
   - Severity: CRITICAL
   - Checks for conda usage in project files

5. **Lock File (PY005)**
   - Category: Package Management
   - Standard: Project SHOULD have a lock file (poetry.lock, pip-tools requirements.in, requirements.txt)
   - Severity: RECOMMENDATION
   - Checks for the presence of dependency lock files

## Package Management

The project uses pyproject.toml for package management with pip as the package manager. The project is configured to use hatch as the build system, providing a modern and flexible way to manage Python packages while maintaining pip compatibility.

## Testing

To run integration tests:

```bash
# Set GitLab credentials
export GITLAB_TOKEN=your_token  # or GITLAB_TEST_TOKEN
export GITLAB_URL=your_gitlab_url  # or GITLAB_TEST_URL

# Set test project ID
export GITLAB_PROJECT_ID=your_project_id  # or GITLAB_TEST_PROJECT_ID

pytest tests/integration/
```

The tests will use the first available environment variable in the following order:
- For token: GITLAB_TEST_TOKEN (preferred) or GITLAB_TOKEN
- For URL: GITLAB_TEST_URL (preferred) or GITLAB_URL
- For project ID: GITLAB_TEST_PROJECT_ID (preferred) or GITLAB_PROJECT_ID

## Example Output

The tool provides a checklist-style output:

```
Successfully connected to project: Project Name
[✗] [PY001] Python version MUST be at least 3.9
    - Got: None
    - Suggestion: Update your project's Python version requirement to at least 3.9
[✓] [PY002] Project SHOULD have a project specification
[✓] [PY003] Project SHOULD have Makefile at root level
[✓] [PY004] Project MUST NOT use conda
[✓] [PY005] Project SHOULD have a lock file
```

The tool also supports JSON output format by using the `--format json` flag.

```json
{
  "python_version": {
    "standard": ">3.8",
    "meets_standard": true,
    "value": "3.11"
  },
  "pyproject_toml": {
    "standard": "required",
    "meets_standard": true
  }
}
```