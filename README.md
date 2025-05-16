# GitLab Python Standards Checker

A CLI tool to check GitLab repositories against defined Python standards.

## Project Structure

```
src/
├── gitlab_checker.py
├── __init__.py

tests/
├── unit/
├── integration/
│   └── test_gitlab_checker.py
└── __init__.py

requirements.txt
README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/gitlab_checker.py <project_id> [--token <gitlab_token>] [--url <gitlab_url>]
```

### Environment Variables

- `GITLAB_TOKEN`: GitLab private token
- `GITLAB_URL`: GitLab instance URL (defaults to https://gitlab.com)

```bash
export GITLAB_TOKEN=your_token_here
export GITLAB_URL=your_gitlab_url
````

## Standards Checked

1. Python version > 3.8
2. Project has specification in pyproject.toml file

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
