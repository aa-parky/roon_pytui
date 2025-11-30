# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

roon-pytui is a Terminal User Interface (TUI) application for controlling Roon music servers, built with Python and Textual. It follows Unix philosophy principles with a modular architecture where each component has a single, well-defined responsibility.

## Development Commands

### Installation
```bash
# Install in development mode with all dev dependencies
pip install -e ".[dev]"
```

### Running the Application
```bash
# Run the TUI application
roon-pytui

# Or run directly via Python module
python -m roon_pytui.main
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=roon_pytui --cov-report=html

# Run a single test file
pytest tests/unit/test_config_manager.py

# Run a specific test
pytest tests/unit/test_config_manager.py::TestConfigManager::test_load_empty_config
```

### Code Quality
```bash
# Run linter (check only)
ruff check .

# Format code
ruff format .

# Type checking
mypy src/roon_pytui

# Run all checks together
ruff check . && ruff format . && mypy src/roon_pytui
```

## Architecture

### Module Structure

The codebase is organized into focused modules:

- **`connection/`**: Handles Roon API connection lifecycle
  - `discovery.py`: Network discovery of Roon Core servers via UDP broadcast
  - `manager.py`: Connection state management, authentication, and token persistence

- **`config/`**: Configuration persistence
  - `manager.py`: Manages JSON config file at `~/.config/roon-pytui/config.json`
  - Stores server details, authentication tokens, and user preferences

- **`models/`**: Data models using Pydantic
  - `connection.py`: `ConnectionState` enum, `ServerInfo`, and `AuthenticationStatus` models
  - All models are immutable and type-safe

- **`ui/`**: Textual framework components
  - `app.py`: Main `RoonTUI` application, connection status widget, and app lifecycle
  - `screens.py`: `DiscoveryScreen` modal for server discovery and selection

- **`main.py`**: Entry point with logging configuration

### Key Design Patterns

**Dependency Injection**: `ConfigManager` is injected into `ConnectionManager` to enable easy testing and reduce coupling.

**Callback Pattern**: `ConnectionManager` uses callbacks for authentication status changes, decoupling connection logic from UI updates. The UI registers a callback via `set_auth_callback()` to receive `AuthenticationStatus` updates.

**Connection Lifecycle**:
1. `DISCONNECTED` → User initiates discovery or reconnect
2. `DISCOVERING` → `RoonDiscovery.discover()` scans network
3. `CONNECTING` → `ConnectionManager.connect()` creates `RoonApi` instance
4. `AUTHENTICATING` → Waiting for user to authorize in Roon Core
5. `CONNECTED` → Token received and persisted to config
6. `ERROR` → Connection/authentication failed

**Token Management**: Authentication tokens are automatically saved to the config file on successful authentication and reused on reconnect via `reconnect_from_config()`.

### Important Implementation Details

**Roon API Integration**:
- Uses the `roonapi` Python library (pyroon fork)
- Discovery via UDP broadcast (default 5 second timeout)
- WebSocket-based communication once connected
- State changes from Roon API trigger `_on_state_change()` callback in `ConnectionManager`
- The `RoonApi` object is created in `ConnectionManager.connect()` with optional token reuse

**Configuration Storage**:
- Platform-independent paths using standard config directory
- JSON format for human readability and easy debugging
- Located at `~/.config/roon-pytui/config.json`
- Stores: `core_id`, `core_name`, `host`, `port`, `token`

**Textual UI Framework**:
- Reactive UI updates via Textual's event system
- CSS-like styling defined in `RoonTUI.CSS`
- Modal screens pushed/popped using `push_screen()` and `pop_screen()`
- Keyboard bindings: `q` (quit), `d` (discover), `r` (reconnect)

**Logging**:
- Application logs written to `~/.config/roon-pytui/roon-pytui.log`
- Log level INFO by default
- Use `logger.debug()`, `logger.info()`, `logger.warning()`, `logger.error()` throughout

## Testing Strategy

Target: 50%+ test coverage (enforced in pyproject.toml), with goal to increase to 80%

**Current Coverage**: ~27% (core modules tested, UI needs integration tests)

**Test Organization**:
- `tests/unit/`: Unit tests for individual modules
- `tests/integration/`: Integration tests (to be added)
- Mirror the source structure in test file naming

**Key Testing Considerations**:
- Mock Roon API calls for unit tests (no real Roon server needed)
- Use pytest fixtures for common test data (ServerInfo, config files)
- Test error scenarios: network failures, authentication rejection, missing config
- UI tests require Textual's testing utilities

## Key Files Reference

- `src/roon_pytui/connection/manager.py:58-98`: `ConnectionManager.connect()` - handles connection and authentication setup
- `src/roon_pytui/connection/manager.py:100-129`: `_on_state_change()` - processes Roon API state changes and token persistence
- `src/roon_pytui/ui/app.py:87-267`: `RoonTUI` - main application class with lifecycle management
- `src/roon_pytui/models/connection.py:9-17`: `ConnectionState` enum - all possible connection states
- `src/roon_pytui/config/manager.py`: `ConfigManager` - handles all config file operations

## Configuration

**pyproject.toml settings**:
- Python 3.8+ required
- Line length: 100 characters (ruff)
- Test coverage fails if < 50% (goal: 80%)
- Mypy strict mode enabled

**Dependencies**:
- `roonapi`: Roon API client
- `textual`: TUI framework
- `pydantic`: Data validation

## Current Limitations

- Only connects to one Roon Core at a time
- No playback controls yet (Phase 3)
- No library browsing yet (Phase 4)
- UI integration tests not yet implemented
- Requires Roon Core on local network for discovery

## Development Workflow

1. Make changes to source files in `src/roon_pytui/`
2. Add/update tests in `tests/`
3. Run `ruff format .` to format code
4. Run `ruff check .` to lint
5. Run `pytest --cov=roon_pytui` to verify tests pass and coverage is maintained
6. Run `mypy src/roon_pytui` to verify type safety

## CI/CD

The project has comprehensive GitHub Actions workflows:

### Main Workflows
- **CI** (`.github/workflows/ci.yml`): Tests on Python 3.8-3.12 across Ubuntu/macOS/Windows, coverage reporting, package building
- **Code Quality** (`.github/workflows/code-quality.yml`): Ruff linting, mypy type checking, security scanning with bandit/safety
- **PR** (`.github/workflows/pr.yml`): PR-specific checks, size labeling, changed file analysis, automated comments

### Key Features
- All checks must pass before merging
- Coverage must be ≥50% (enforced, goal is 80%)
- Codecov integration for coverage tracking
- Dependabot for automated dependency updates (Mondays at 09:00)
- Security scanning with bandit and safety
- Automated PR size labeling (XS/S/M/L/XL)

### Documentation
- Contributing guidelines: `.github/CONTRIBUTING.md`
- Detailed CI docs: `.github/CI.md`
- Issue templates for bugs and features
- PR template with checklist
