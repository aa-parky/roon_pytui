# roon-pytui

[![CI](https://github.com/aa-parky/roon_pytui/actions/workflows/ci.yml/badge.svg)](https://github.com/aa-parky/roon_pytui/actions/workflows/ci.yml)
[![Code Quality](https://github.com/aa-parky/roon_pytui/actions/workflows/code-quality.yml/badge.svg)](https://github.com/aa-parky/roon_pytui/actions/workflows/code-quality.yml)
[![codecov](https://codecov.io/gh/aa-parky/roon_pytui/branch/main/graph/badge.svg)](https://codecov.io/gh/aa-parky/roon_pytui)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A beautiful, modular Terminal User Interface (TUI) for controlling Roon music servers, built with Python and Textual.

## Overview

roon-pytui provides a lightweight, keyboard-driven interface to interact with your Roon music system directly from the terminal. Built following Unix philosophy principles, each module does one thing well, making the codebase maintainable, testable, and extensible.

## Features

- 🎵 Browse and search your Roon music library
- ▶️ Playback controls (play, pause, skip, volume)
- 📋 Queue management
- 🎨 Beautiful terminal UI with Textual framework
- ⚡ Fast and lightweight
- 🧩 Modular architecture
- ✅ Test coverage (50%+ target, growing to 80%)

## Architecture

The project follows a modular design where each component has a single, well-defined responsibility:

```
roon_pytui/
├── connection/     # Roon API connection and discovery
├── browse/         # Library browsing and search
├── playback/       # Playback control operations
├── queue/          # Queue management
├── config/         # Configuration management
├── ui/             # Textual widgets and screens
└── models/         # Data models and types
```

## Prerequisites

- Python 3.8 or higher
- Roon Core server running on your network
- Terminal with 256-color support

## Installation

```bash
# Clone the repository
git clone https://github.com/aa-parky/roon_pytui.git
cd roon_pytui

# Install dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Run the TUI
roon-pytui

# First run will prompt for Roon Core discovery and authorization
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=roon_pytui --cov-report=html

# Run linter
ruff check .

# Format code
ruff format .

# Type checking
mypy roon_pytui
```

## Project Status & Tasks

### Phase 1: Foundation ✅
- [x] Research Roon Python API
- [x] Research Textual framework
- [x] Design modular architecture
- [x] Set up project structure
- [ ] Configure development environment
- [ ] Set up CI/CD pipeline

### Phase 2: Core Modules 🚧
- [ ] Implement connection module
  - [ ] Roon Core discovery
  - [ ] Authentication and token management
  - [ ] Connection state management
- [ ] Implement config module
  - [ ] Configuration file handling
  - [ ] Settings management
  - [ ] Credential storage
- [ ] Implement models module
  - [ ] Zone models
  - [ ] Track/Album/Artist models
  - [ ] Queue models

### Phase 3: Playback & Control 📋
- [ ] Implement playback module
  - [ ] Play/pause/stop controls
  - [ ] Volume control
  - [ ] Track navigation
  - [ ] Zone selection
- [ ] Implement queue module
  - [ ] View queue
  - [ ] Add/remove tracks
  - [ ] Reorder queue

### Phase 4: Browse & Search 📋
- [ ] Implement browse module
  - [ ] Library browsing
  - [ ] Search functionality
  - [ ] Artist/Album/Track views
  - [ ] Playlists

### Phase 5: User Interface 📋
- [ ] Implement UI module
  - [ ] Main application screen
  - [ ] Playback widget
  - [ ] Library browser widget
  - [ ] Queue widget
  - [ ] Help/keybindings screen

### Phase 6: Testing & Quality 📋
- [ ] Write unit tests for all modules
- [ ] Write integration tests
- [ ] Achieve 80%+ code coverage
- [ ] Add property-based tests
- [ ] Performance testing

### Phase 7: Documentation & Polish 📋
- [ ] API documentation
- [ ] User guide
- [ ] Keyboard shortcuts reference
- [ ] Configuration guide
- [ ] Contributing guidelines

## Testing

The project aims for 80%+ test coverage using pytest. Tests are organized to mirror the source structure:

```
tests/
├── unit/           # Unit tests for individual modules
├── integration/    # Integration tests
└── fixtures/       # Test fixtures and mock data
```

## CI/CD

GitHub Actions workflows automatically:
- Run tests on all PRs and commits
- Check code coverage (fails if < 80%)
- Run linting and type checking
- Build and validate package

## Technology Stack

- **[roonapi](https://pypi.org/project/roonapi/)**: Python interface to Roon API
- **[Textual](https://textual.textualize.io/)**: Modern TUI framework
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass and coverage remains >80%
5. Submit a pull request

## License

GPL-3.0 - See LICENSE file for details

## Resources

- [Roon API Documentation](https://github.com/pavoni/pyroon)
- [Textual Documentation](https://textual.textualize.io/)
- [Real Python Textual Tutorial](https://realpython.com/python-textual/)

## Acknowledgments

- Built on the excellent [pyroon](https://github.com/pavoni/pyroon) library by Greg Dowling
- UI framework by [Textualize.io](https://www.textualize.io/)
