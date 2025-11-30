# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Fixed Roon server discovery mechanism that was causing "'method' object is not iterable" error
- Rewrote `RoonDiscovery` class to properly parse SOOD (Service-Oriented Object Discovery) messages
- Discovery now correctly extracts server name, version, unique ID, host, and port from network responses
- Implemented proper deduplication to handle servers responding to both multicast and broadcast queries

### Changed
- Discovery implementation no longer relies on `RoonDiscovery.all` property from roonapi
- Now directly implements SOOD protocol parsing for better control and error handling
- Improved logging throughout discovery process

## [0.1.0] - 2025-11-30

### Added
- Initial project structure with modular architecture
- Server discovery functionality using Roon SOOD protocol
- Authentication and token management
- Configuration persistence in `~/.config/roon-pytui/`
- Connection state management with callbacks
- Basic TUI interface using Textual framework
- Main application screen with connection status
- Discovery screen for server selection
- Keyboard shortcuts (q=quit, d=discover, r=reconnect)
- Notification system
- Comprehensive logging to `~/.config/roon-pytui/roon-pytui.log`
- Unit tests for core modules
- Development tooling (pytest, ruff, mypy)
- Documentation (README, QUICKSTART, PROJECT_SUMMARY)

### Technical Details
- Python 3.8+ support (tested with 3.11)
- Dependencies: roonapi, textual, pydantic
- Modular package structure with separation of concerns
- Type hints throughout codebase
- Pydantic models for data validation
