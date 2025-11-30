"""Main TUI application using Textual framework."""

import logging
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Footer, Header, Label, Static

from ..config.manager import ConfigManager
from ..connection.discovery import RoonDiscovery
from ..connection.manager import ConnectionManager
from ..models.connection import AuthenticationStatus, ConnectionState, ServerInfo
from .screens import DiscoveryScreen

logger = logging.getLogger(__name__)


# Application info for Roon API
APP_INFO = {
    "extension_id": "com.roon_pytui",
    "display_name": "Roon PyTUI",
    "display_version": "0.1.0",
    "publisher": "roon-pytui",
    "email": "support@roon-pytui.local",
}


class ConnectionStatusWidget(Static):
    """Widget to display connection status."""

    def __init__(self) -> None:
        """Initialize the status widget."""
        super().__init__()
        self.status = ConnectionState.DISCONNECTED
        self.server_name: Optional[str] = None

    def update_status(self, status: ConnectionState, server_name: Optional[str] = None) -> None:
        """Update the connection status display.

        Args:
            status: Current connection state
            server_name: Name of the connected server, if any
        """
        self.status = status
        self.server_name = server_name
        self._refresh_display()

    def _refresh_display(self) -> None:
        """Refresh the status display."""
        status_text = self._get_status_text()
        status_color = self._get_status_color()

        self.update(f"[{status_color}]● {status_text}[/{status_color}]")

    def _get_status_text(self) -> str:
        """Get the status text based on current state."""
        if self.status == ConnectionState.CONNECTED and self.server_name:
            return f"Connected to {self.server_name}"
        elif self.status == ConnectionState.CONNECTING:
            return "Connecting..."
        elif self.status == ConnectionState.AUTHENTICATING:
            return "Waiting for authorization..."
        elif self.status == ConnectionState.DISCOVERING:
            return "Discovering servers..."
        elif self.status == ConnectionState.ERROR:
            return "Connection error"
        else:
            return "Disconnected"

    def _get_status_color(self) -> str:
        """Get the color for the current status."""
        if self.status == ConnectionState.CONNECTED:
            return "green"
        elif self.status in (
            ConnectionState.CONNECTING,
            ConnectionState.AUTHENTICATING,
            ConnectionState.DISCOVERING,
        ):
            return "yellow"
        elif self.status == ConnectionState.ERROR:
            return "red"
        else:
            return "grey"


class RoonTUI(App):
    """Main Roon TUI application."""

    CSS = """
    Screen {
        align: center middle;
    }

    #main-container {
        width: 80;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }

    #status-container {
        height: 3;
        margin-bottom: 1;
    }

    #content-container {
        height: auto;
        margin-bottom: 1;
    }

    #button-container {
        height: auto;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .info {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "discover", "Discover"),
        ("r", "reconnect", "Reconnect"),
    ]

    def __init__(self) -> None:
        """Initialize the application."""
        super().__init__()
        self.config_manager = ConfigManager()
        self.connection_manager = ConnectionManager(APP_INFO, self.config_manager)
        self.connection_manager.set_auth_callback(self._on_auth_status_change)
        self.discovery = RoonDiscovery()
        self.status_widget: Optional[ConnectionStatusWidget] = None

    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        yield Header()

        with Container(id="main-container"):
            yield Label("Roon PyTUI", classes="title")
            yield Label("Terminal User Interface for Roon", classes="info")

            with Vertical(id="status-container"):
                self.status_widget = ConnectionStatusWidget()
                yield self.status_widget

            with Vertical(id="content-container"):
                yield Label("Press 'd' to discover Roon servers", classes="info")
                yield Label("Press 'r' to reconnect to last server", classes="info")

            with Container(id="button-container"):
                yield Button("Discover Servers", id="btn-discover", variant="primary")
                yield Button("Reconnect", id="btn-reconnect", variant="default")
                yield Button("Quit", id="btn-quit", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        """Handle application mount event."""
        logger.info("Roon PyTUI started")

        # Try to reconnect to last known server
        if self.connection_manager.reconnect_from_config():
            if self.status_widget:
                self.status_widget.update_status(ConnectionState.CONNECTING)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events.

        Args:
            event: Button press event
        """
        button_id = event.button.id

        if button_id == "btn-discover":
            self.action_discover()
        elif button_id == "btn-reconnect":
            self.action_reconnect()
        elif button_id == "btn-quit":
            self.action_quit()

    def action_discover(self) -> None:
        """Discover Roon servers on the network."""
        logger.info("Starting server discovery")

        if self.status_widget:
            self.status_widget.update_status(ConnectionState.DISCOVERING)

        # Push the discovery screen
        self.push_screen(
            DiscoveryScreen(self.discovery, self.connection_manager), self._on_discovery_complete
        )

    def action_reconnect(self) -> None:
        """Reconnect to the last known server."""
        logger.info("Attempting to reconnect")

        if self.status_widget:
            self.status_widget.update_status(ConnectionState.CONNECTING)

        if not self.connection_manager.reconnect_from_config():
            self.notify("No saved server configuration found", severity="warning")
            if self.status_widget:
                self.status_widget.update_status(ConnectionState.DISCONNECTED)

    def _on_discovery_complete(self, server: Optional[ServerInfo]) -> None:
        """Handle completion of server discovery.

        Args:
            server: Selected server, or None if cancelled
        """
        if server:
            logger.info(f"Server selected: {server.core_name}")
            if self.status_widget:
                self.status_widget.update_status(ConnectionState.CONNECTED, server.core_name)
        else:
            logger.info("Discovery cancelled")
            if self.status_widget:
                self.status_widget.update_status(ConnectionState.DISCONNECTED)

    def _on_auth_status_change(self, status: AuthenticationStatus) -> None:
        """Handle authentication status changes.

        Args:
            status: New authentication status
        """
        if status.is_authenticated:
            logger.info("Authentication successful")
            self.notify("Successfully authenticated with Roon Core", severity="information")

            if self.status_widget and self.connection_manager.current_server:
                self.status_widget.update_status(
                    ConnectionState.CONNECTED, self.connection_manager.current_server.core_name
                )
        else:
            logger.warning(f"Authentication failed: {status.error_message}")
            self.notify(
                f"Authentication failed: {status.error_message or 'Unknown error'}",
                severity="error",
            )

            if self.status_widget:
                self.status_widget.update_status(ConnectionState.ERROR)

    def on_unmount(self) -> None:
        """Handle application unmount event."""
        logger.info("Shutting down Roon PyTUI")

        # Clean up connections
        self.connection_manager.disconnect()
        self.discovery.stop()
