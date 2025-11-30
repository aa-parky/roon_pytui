# Contributing to roon-pytui

Thank you for your interest in contributing to roon-pytui! This document provides guidelines and information for contributors.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/roon_pytui.git
   cd roon_pytui
   ```

2. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run tests to verify setup**
   ```bash
   pytest
   ```

## Development Workflow

### Before Making Changes

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make sure all tests pass:
   ```bash
   pytest
   ```

### Making Changes

1. **Write your code** following the project style
2. **Add tests** for new functionality
3. **Update documentation** if needed

### Code Quality Checks

Before committing, run these checks locally:

```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type checking
mypy src/roon_pytui

# Run tests with coverage
pytest --cov=roon_pytui --cov-report=term
```

All of these checks will also run automatically in CI when you open a PR.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/unit/test_config_manager.py

# Run a specific test
pytest tests/unit/test_config_manager.py::TestConfigManager::test_load_empty_config

# Run with coverage
pytest --cov=roon_pytui --cov-report=html
```

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names: `test_<what>_<condition>_<expected_result>`
- Aim for good code coverage (minimum 50%, goal 80%)
- Mock external dependencies (Roon API, file system, etc.)

Example test:
```python
def test_config_manager_loads_empty_config_when_file_missing():
    """Test that ConfigManager returns empty config when file doesn't exist."""
    manager = ConfigManager(config_file="nonexistent.json")
    config = manager.load()
    assert config.core_id is None
```

## Pull Request Process

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** against the `main` branch

3. **Automated Checks**: The following will run automatically:
   - Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
   - Tests on Ubuntu, macOS, and Windows
   - Code coverage check (must be ≥50%)
   - Linting with ruff
   - Type checking with mypy
   - Security scanning
   - PR size labeling

4. **PR Review**:
   - Address any failing checks
   - Respond to reviewer feedback
   - Keep your PR up to date with `main`

5. **Merging**: Once approved and all checks pass, a maintainer will merge your PR

## Code Style

We use:
- **ruff** for linting and formatting (follows PEP 8)
- **mypy** for type checking (strict mode)
- Line length: 100 characters
- Type hints required for all functions

### Type Hints

All functions should have type hints:

```python
def connect(self, server: ServerInfo, token: Optional[str] = None) -> bool:
    """Connect to a Roon Core server.

    Args:
        server: ServerInfo for the server to connect to
        token: Optional authentication token from previous session

    Returns:
        True if connection initiated successfully, False otherwise
    """
    # Implementation
```

## Architecture Guidelines

- **Modular Design**: Each module has a single responsibility
- **Dependency Injection**: Inject dependencies rather than creating them
- **Immutable Models**: Use Pydantic models with `frozen=True`
- **Type Safety**: Use type hints and validate with mypy
- **Error Handling**: Use logging and provide clear error messages

## Commit Messages

Use clear, descriptive commit messages:

```
type(scope): Brief description

Longer description if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `chore`: Maintenance tasks

## CI/CD Workflows

### CI Workflow (`.github/workflows/ci.yml`)
- Runs on: Push to main/develop, PRs
- Tests across Python 3.8-3.12 and Ubuntu/macOS/Windows
- Coverage reporting with Codecov
- Package build verification

### Code Quality Workflow (`.github/workflows/code-quality.yml`)
- Runs on: Push to main/develop, PRs
- Linting with ruff
- Type checking with mypy
- Security scanning with bandit and safety
- Dependency review

### PR Workflow (`.github/workflows/pr.yml`)
- Runs on: Pull requests
- PR size labeling (XS/S/M/L/XL)
- Changed file analysis
- Test and lint only changed files
- Automated PR summary comments

## Coverage Requirements

- Minimum coverage: **50%** (goal: 80%)
- Coverage is checked in CI and will fail if below threshold
- View coverage report: `pytest --cov=roon_pytui --cov-report=html` then open `htmlcov/index.html`

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues and PRs first
- Ask questions in issues or PR comments

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.
