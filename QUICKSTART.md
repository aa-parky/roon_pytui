# Quick Start Guide

## Initial Setup

This project has been set up with the basic structure for a Roon TUI application focusing on server discovery and authentication.

### Prerequisites

- Python 3.11.13 (or Python 3.8+)
- A Roon Core server running on your local network
- Terminal with 256-color support

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd /home/ubuntu/roon-pytui
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install the package in development mode:**
   ```bash
   pip install -e ".[dev]"
   ```

### Running the Application

**Note:** The application is currently in initial development. The TUI interface has been created but requires a running Roon Core server on your network for full functionality.

To run the application:

```bash
source venv/bin/activate
roon-pytui
```

Or run directly with Python:

```bash
source venv/bin/activate
python -m roon_pytui.main
```

### First Run

On first run, the application will:

1. Display the main screen with connection status
2. Allow you to discover Roon servers on your network (press 'd' or click "Discover Servers")
3. Present a list of discovered servers
4. Connect to the selected server
5. Wait for authorization from Roon Core (you'll need to authorize the connection in your Roon app)

### Key Features Implemented

- **Server Discovery**: Automatic discovery of Roon Core servers on the local network
- **Authentication**: Token-based authentication with Roon Core
- **Configuration Management**: Persistent storage of connection settings
- **Connection State Management**: Tracks connection status and handles reconnection
- **TUI Interface**: Beautiful terminal interface built with Textual

### Project Structure

```
roon-pytui/
├── src/roon_pytui/
│   ├── connection/          # Roon API connection and discovery
│   │   ├── discovery.py     # Server discovery logic
│   │   └── manager.py       # Connection and authentication management
│   ├── config/              # Configuration management
│   │   └── manager.py       # Config persistence
│   ├── models/              # Data models
│   │   └── connection.py    # Connection-related models
│   ├── ui/                  # Textual UI components
│   │   ├── app.py          # Main application
│   │   └── screens.py      # Discovery screen
│   └── main.py             # Entry point
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests (to be added)
│   └── fixtures/           # Test fixtures (to be added)
├── pyproject.toml          # Project configuration
└── README.md               # Project documentation
```

### Development Commands

**Run tests:**
```bash
pytest
```

**Run tests with coverage:**
```bash
pytest --cov=roon_pytui --cov-report=html
```

**Lint code:**
```bash
ruff check .
```

**Format code:**
```bash
ruff format .
```

**Type checking:**
```bash
mypy src/roon_pytui
```

### Configuration

Configuration is stored in `~/.config/roon-pytui/config.json` and includes:
- Last connected Roon Core ID and name
- Authentication token
- Server host and port

Logs are stored in `~/.config/roon-pytui/roon-pytui.log`

### Keyboard Shortcuts

- `q` - Quit the application
- `d` - Discover Roon servers
- `r` - Reconnect to last server
- `Esc` - Cancel/Go back
- `Enter` - Select/Confirm

### Next Steps

The following features are planned for future development:

1. **Playback Controls**: Play, pause, stop, volume control
2. **Library Browsing**: Browse artists, albums, tracks
3. **Queue Management**: View and manage playback queue
4. **Search**: Search across your music library
5. **Zone Selection**: Choose which Roon zone to control

### Troubleshooting

**No servers found:**
- Ensure Roon Core is running on your network
- Check that your firewall allows network discovery
- Verify you're on the same network as Roon Core

**Authentication fails:**
- Check Roon Core settings for pending authorization requests
- Authorize the "Roon PyTUI" extension in Roon

**Connection issues:**
- Check logs in `~/.config/roon-pytui/roon-pytui.log`
- Try clearing config: `rm ~/.config/roon-pytui/config.json`
- Restart the application

### Contributing

This is an initial implementation. Contributions are welcome! Please:

1. Write tests for new functionality
2. Ensure code passes linting (`ruff check`)
3. Format code (`ruff format`)
4. Update documentation

### License

GPL-3.0 - See LICENSE file for details
