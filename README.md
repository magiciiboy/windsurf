# GitLab Python Standards Checker

A CLI tool to check GitLab repositories against defined Python standards.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python gitlab_checker.py <project_id> [--token <gitlab_token>]
```

### Environment Variables

You can also set the GitLab token using an environment variable:

```bash
export GITLAB_TOKEN=your_token_here
```

## Standards Checked

1. Python version > 3.8
2. Project has specification in pyproject.toml file

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
