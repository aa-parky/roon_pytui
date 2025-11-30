# CI/CD Documentation

This document describes the Continuous Integration and Continuous Deployment setup for roon-pytui.

## Overview

The project uses GitHub Actions for CI/CD with three main workflows:
1. **CI Workflow** - Comprehensive testing and building
2. **Code Quality Workflow** - Linting, type checking, and security
3. **PR Workflow** - Pull request specific checks and automation

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### `test`
- **Purpose**: Test across multiple Python versions and operating systems
- **Matrix**: Python 3.8-3.12 on Ubuntu, macOS, Windows
- **Steps**:
  - Checkout code
  - Set up Python with pip caching
  - Install dependencies
  - Run pytest with verbose output
  - Upload test results as artifacts

#### `coverage`
- **Purpose**: Measure and report test coverage
- **Runs on**: Ubuntu with Python 3.11
- **Steps**:
  - Run pytest with coverage
  - Check 80% coverage threshold
  - Upload to Codecov
  - Generate HTML coverage report
  - Comment coverage on PRs
- **Artifacts**: Coverage HTML report (30 days retention)

#### `build`
- **Purpose**: Verify package builds correctly
- **Steps**:
  - Build source and wheel distributions
  - Validate with twine
  - Upload dist artifacts
- **Artifacts**: Built packages (30 days retention)

### 2. Code Quality Workflow (`.github/workflows/code-quality.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### `lint`
- **Purpose**: Check code style and formatting
- **Tools**: ruff
- **Checks**:
  - Linting rules (pycodestyle, pyflakes, isort, flake8-bugbear, etc.)
  - Code formatting consistency
- **Output**: GitHub annotations on problematic lines

#### `type-check`
- **Purpose**: Verify type safety
- **Tool**: mypy (strict mode)
- **Checks**:
  - Type hints completeness
  - Type consistency
  - Return type accuracy
- **Artifacts**: mypy cache (7 days retention)

#### `security`
- **Purpose**: Scan for security vulnerabilities
- **Tools**:
  - bandit: Security linting for Python code
  - safety: Check dependencies for known vulnerabilities
- **Artifacts**: Security reports in JSON (30 days retention)
- **Note**: Continues on error (informational only)

#### `dependency-review`
- **Purpose**: Review dependency changes in PRs
- **When**: Only on pull requests
- **Checks**: New dependencies for security issues
- **Threshold**: Fails on moderate or higher severity

### 3. PR Workflow (`.github/workflows/pr.yml`)

**Triggers:**
- Pull requests (opened, synchronize, reopened, ready_for_review)
- Only runs on non-draft PRs

**Jobs:**

#### `pr-info`
- **Purpose**: Analyze and summarize PR changes
- **Provides**:
  - Total files changed
  - Python files changed
  - Test files changed
  - Author information
- **Action**: Posts summary comment on PR

#### `test-changes`
- **Purpose**: Test code affected by PR
- **Features**:
  - Identifies changed Python files
  - Runs full test suite with coverage
  - Posts coverage results as PR comment
  - Warns if coverage below 80%

#### `lint-changes`
- **Purpose**: Lint only changed files for faster feedback
- **Runs**: ruff check and format on modified Python files
- **Benefit**: Quick feedback loop for contributors

#### `size-label`
- **Purpose**: Auto-label PRs by size
- **Labels**:
  - `size/XS`: < 10 lines changed
  - `size/S`: 10-99 lines changed
  - `size/M`: 100-499 lines changed
  - `size/L`: 500-999 lines changed
  - `size/XL`: 1000+ lines changed
- **Action**: Automatically updates size label as PR changes

## Dependabot (`.github/dependabot.yml`)

**Purpose**: Automatically update dependencies

**Configuration:**

### Python Dependencies
- **Schedule**: Weekly on Mondays at 09:00
- **Limits**: Up to 5 open PRs
- **Grouping**: All patch updates grouped together
- **Labels**: `dependencies`, `python`
- **Commit prefix**: `deps:`

### GitHub Actions
- **Schedule**: Weekly on Mondays at 09:00
- **Limits**: Up to 3 open PRs
- **Labels**: `dependencies`, `github-actions`
- **Commit prefix**: `ci:`

## Artifacts and Retention

| Artifact | Retention | Workflow |
|----------|-----------|----------|
| Test Results | 7 days | CI |
| Coverage Report | 30 days | CI |
| Built Packages | 30 days | CI |
| mypy Cache | 7 days | Code Quality |
| Security Reports | 30 days | Code Quality |

## Status Badges

The following badges are displayed in README.md:

1. **CI Status**: Overall CI workflow status
2. **Code Quality Status**: Code quality checks status
3. **Codecov**: Coverage percentage
4. **Python Version**: Supported Python versions
5. **License**: Project license

Badges automatically update based on workflow runs.

## Coverage Reporting

### Codecov Integration

**Setup Required:**
1. Sign up at [codecov.io](https://codecov.io)
2. Add your repository
3. Get your `CODECOV_TOKEN`
4. Add as GitHub secret: Settings → Secrets → Actions → New repository secret
   - Name: `CODECOV_TOKEN`
   - Value: Your token

**Note**: Without the token, coverage upload will continue but won't fail the build.

### Coverage Requirements

- **Minimum**: 80% (enforced in `pyproject.toml`)
- **Check**: Runs on every PR and push
- **Report**: HTML report available as artifact
- **Visibility**: Coverage badge in README

## Local Development

Run the same checks locally before pushing:

```bash
# Full test suite
pytest -v

# With coverage
pytest --cov=roon_pytui --cov-report=html --cov-report=term

# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy src/roon_pytui

# Build package
python -m build
twine check dist/*
```

## Troubleshooting

### Tests Failing Locally But Passing in CI
- Check Python version matches
- Ensure dependencies are up to date: `pip install -e ".[dev]" --upgrade`
- Clear pytest cache: `rm -rf .pytest_cache`

### Coverage Below Threshold
- Run locally: `pytest --cov=roon_pytui --cov-report=html`
- Open `htmlcov/index.html` to see uncovered lines
- Add tests for uncovered code

### Linting Failures
- Auto-fix: `ruff check . --fix`
- Format: `ruff format .`
- Check output: `ruff check . --output-format=grouped`

### Type Checking Failures
- Run locally: `mypy src/roon_pytui --show-error-codes`
- Add type hints to untyped functions
- Use `Optional[T]` for nullable types

### Security Scan Warnings
- Review bandit report: Download artifact from Actions
- Address high-severity issues
- Use `# nosec` comment with justification if false positive

## Maintenance

### Adding New Workflows

1. Create file in `.github/workflows/`
2. Use descriptive name and clear triggers
3. Add appropriate jobs with error handling
4. Test on a branch first
5. Document in this file

### Updating Python Versions

When dropping/adding Python versions:

1. Update `pyproject.toml`:
   - `requires-python`
   - `classifiers`
2. Update workflow matrices in:
   - `.github/workflows/ci.yml`
3. Update badges in README.md
4. Test all versions before release

### Secrets Management

Required secrets (Settings → Secrets → Actions):
- `CODECOV_TOKEN`: For Codecov integration (optional but recommended)

## Performance Optimization

Current workflow runtimes (approximate):
- **CI**: 15-20 minutes (full matrix)
- **Code Quality**: 3-5 minutes
- **PR**: 2-4 minutes

Tips to improve:
1. Use caching (already implemented for pip)
2. Run jobs in parallel (already implemented)
3. Fail fast on obvious errors
4. Use matrix strategy wisely

## Best Practices

1. **Always run checks locally before pushing**
2. **Keep workflows simple and maintainable**
3. **Use caching to speed up builds**
4. **Fail fast on critical errors**
5. **Provide clear error messages**
6. **Keep artifact retention reasonable**
7. **Document workflow changes**
8. **Monitor workflow costs** (GitHub Actions minutes)
