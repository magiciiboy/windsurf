# Python Standards Checker

A CLI tool to check Python standards in GitLab repositories.

## Project Structure

```
src/
└── python_standards_checker/
    ├── __init__.py
    

tests/
├── unit/
├── integration/
│   └── test_gitlab_checker.py
└── __init__.py

pyproject.toml
hatch.toml
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
python-standards-checker <project_id> [--token <gitlab_token>] [--url <gitlab_url>]
```

### Environment Variables

- `GITLAB_TOKEN`: GitLab private token
- `GITLAB_URL`: GitLab instance URL (defaults to https://gitlab.com)

```bash
export GITLAB_TOKEN=your_token_here
export GITLAB_URL=your_gitlab_url
````

## Standards Checked

1. Python version >= 3.9
2. Project has specification in pyproject.toml file

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

```json
{
  "python_version": {
    "standard": ">3.8",
    "meets_standard": true,
    "detected_version": "3.11"
  },
  "pyproject_toml": {
    "standard": "required",
    "meets_standard": true
  }
}
```
