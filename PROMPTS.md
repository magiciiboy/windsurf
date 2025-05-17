Build a CLI tool to check Python standards in GitLab repositories.

## Checking Process

### 1. File-based Checks
- Uses GitLab API to retrieve repository files
- Checks for presence of required files
- Validates file contents where applicable

### 2. Dependency Checks
- Evaluates Python version requirements
- Scans for forbidden dependencies (conda)
- Parses version specifiers

### 3. Version Checking
- Uses semantic versioning for comparisons
- Handles various version specifiers (>=, >, ~=, ==)
- Validates against minimum requirement (3.9)

## Output Formats

The checker supports two output formats:

1. **JSON**
   - Machine-readable format
   - Includes detailed standard information
   - Contains detected versions
   - Used for programmatic integration

2. **Checklist**
   - Human-readable format
   - Uses colored indicators:
     - ✓ (green) for passing standards
     - ✗ (red) for critical failures
     - ⚠ (orange) for recommendations

## Integration

The checker can be integrated with GitLab through:
- GitLab API for repository access
- Environment variables for authentication
- CI/CD pipelines for automated checks

## Usage

The checker can be run with these parameters:
- Project ID (required)
- GitLab token (required)
- GitLab URL (optional)
- Output format (json/checklist, default: checklist)

## Color Coding

The checker uses ANSI color codes for terminal output:
- Green: ✓ for passing standards
- Red: ✗ for critical failures
- Orange: ⚠ for recommendations
- Reset: Returns to normal terminal color
