# Python Standards Checker - How It Works

This document provides a comprehensive overview of the Python standards implemented in the checker, their properties, and the detailed checking process for each standard.

## Standards Overview

### 1. Python Version Standard
- **Standard**: Python version MUST be at least 3.9
- **Severity**: CRITICAL
- **Type**: version
- **Recommendation**: Update your project's Python version requirement to at least 3.9

#### Checking Process:
- Checks multiple files for Python version specification:
  1. `pyproject.toml` (project.requires-python)
  2. `setup.py` (python_requires)
  3. `Dockerfile` (python:3.x)
- Version must be >=3.9 (using semantic versioning)
- Supports version specifiers like: 
  - `>=3.9`
  - `>3.8`
  - `~=3.9`
  - `==3.9`

### 2. pyproject.toml Standard
- **Standard**: Project SHOULD have a pyproject.toml specification
- **Severity**: RECOMMENDATION
- **Type**: file
- **Recommendation**: Create a pyproject.toml file to specify project metadata and dependencies

#### Checking Process:
- Checks for presence of `pyproject.toml` at root level
- Validates TOML syntax
- Does not validate contents beyond existence

### 3. Makefile Standard
- **Standard**: Project SHOULD have Makefile at root level
- **Severity**: RECOMMENDATION
- **Type**: file
- **Recommendation**: Create a Makefile at the root of your project to define build and automation targets

#### Checking Process:
- Checks for presence of `Makefile` at root level
- Does not validate contents

### 4. No Conda Standard
- **Standard**: Project MUST NOT use conda
- **Severity**: CRITICAL
- **Type**: dependency
- **Recommendation**: Remove conda dependencies and use uv, poetry, or pip instead

#### Checking Process:
- Checks for conda usage in multiple locations:
  1. File names:
    - `environment.yml`
    - `.condarc`
    - `*.conda`
    - `*.yml`
    - `*.yaml`
  2. `.gitlab-ci.yml`:
    - Searches for 'conda' in content
  3. Shell scripts (`*.sh`):
    - Searches for conda commands

### 5. Lock File Standard
- **Standard**: Project SHOULD have a lock file (poetry.lock, pip-tools requirements.in, requirements.txt)
- **Severity**: RECOMMENDATION
- **Type**: file
- **Recommendation**: Create a lock file to ensure consistent dependency versions across environments

#### Checking Process:
- Checks for presence of any of these files:
  - `requirements.txt`
  - `poetry.lock`
  - `requirements.in` (pip-tools)
