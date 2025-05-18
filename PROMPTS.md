Build StandardsInspector

A CLI tool to check standards in GitLab repositories and best practices.

## Project Structure

```
windsurf/
├── src/
│   └── python_standards_checker/
│       ├── __init__.py
│       ├── cli.py
│       ├── constants.py
│       ├── utils.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── gitlab.py
│       │   └── local.py
│       └── standards/
│           ├── __init__.py
│           ├── base.py
│           ├── python_version.py
│           ├── project_spec.py
│           ├── lock_file.py
│           ├── makefile.py
│           └── no_conda.py
├── tests/
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_version_support.py
│   └── integration/
│       ├── __init__.py
│       └── test_python_standards_checker.py
├── pyproject.toml
├── README.md
└── PROMPTS.md
```

## Requirements

### Core Requirements
- Python 3.9 or higher
- GitLab API access for GitLab mode
- Local file system access for local mode

### Python Dependencies
- `packaging` for version parsing
- `gitlab` for GitLab API integration
- `pytoml` for TOML file parsing
- `pytest` for testing
- `black` for code formatting
- `mypy` for type checking
- `pylint` for code analysis

## Implementation Details

### Repository Layer
- Abstract base class `BaseRepository` in `repositories/base.py`
- `GitLabRepository` for GitLab integration with caching
- `LocalRepository` for local file system access
- Methods:
  - `get_files()`: List files in repository
  - `read_file_content()`: Read file content
  - `test_connection()`: Verify repository access

### Standards Layer
- Abstract base class `BaseStandard` in `standards/base.py`
- Specific standards:
  - `PythonVersionStandard`: Python version requirement
  - `ProjectSpecStandard`: Project specification
  - `LockFileStandard`: Dependency lock file
  - `MakefileStandard`: Makefile presence
  - `NoCondaStandard`: Conda usage check
- Caching for file operations
- Version parsing and comparison

### CLI Implementation
- Argument parsing with `argparse`
- Source type selection (gitlab/local)
- Environment variable support
- Output formatting (checklist/JSON)
- Standard filtering (include/exclude)

### Version Support
- Minimum version requirement: Python 3.9
- Version specification parsing
- Version comparison using `packaging.version`
- Regex patterns for version detection

## Project Setup

### Development Setup
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -e .
```

3. Install development tools:
```bash
pip install -e .[dev]
```

### Testing
```bash
make test
```

### Formatting
```bash
make format
```

### Linting
```bash
make lint
```

## Code Structure

### Core Components
1. `repositories/`
   - Repository abstraction layer
   - GitLab and Local implementations
   - File operations with caching

2. `standards/`
   - Standard checking logic
   - Version parsing
   - File pattern matching

3. `cli.py`
   - Command line interface
   - Argument parsing
   - Output formatting

4. `utils.py`
   - Version support utilities
   - File operations
   - Constants

### Constants
- ANSI color codes
- File patterns
- Version regex patterns
- Standard codes and severities

### Testing Structure
1. Unit tests
   - Version support
   - Utility functions
   - Standard implementations

2. Integration tests
   - Full tool execution
   - GitLab integration
   - Local repository tests

## Usage Patterns

### GitLab Mode
```bash
standards-inspector --source gitlab --project-id <project_id> --token <gitlab_token>
```

### Local Mode
```bash
standards-inspector --source local --directory <directory_path>
```

### Environment Variables
- `GITLAB_TOKEN`: GitLab private token
- `GITLAB_URL`: GitLab instance URL

### Output Formats
- Checklist (default)
- JSON

### Standard Filtering
- Include specific standards
- Exclude specific standards
- Standard codes: PY001, PY002, etc.

## Design Decisions

1. Repository Abstraction
   - Clean separation of repository implementations
   - Consistent interface for different sources
   - Caching for performance optimization

2. Standard Implementation
   - Base class for common functionality
   - Clear separation of concerns
   - Easy to add new standards

3. Version Handling
   - Robust version parsing
   - Flexible version specification
   - Clear minimum requirements

4. Error Handling
   - Graceful failure
   - Clear error messages
   - Environment variable fallbacks
