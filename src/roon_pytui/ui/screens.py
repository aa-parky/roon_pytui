"""UI screens for the Roon TUI application."""

import logging
from typing import List, Optional

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView

from ..connection.discovery import RoonDiscovery
from ..connection.manager import ConnectionManager
from ..models.connection import ServerInfo

logger = logging.getLogger(__name__)


class DiscoveryScreen(Screen):
    """Screen for discovering and selecting Roon servers."""

    CSS = """
    DiscoveryScreen {
        align: center middle;
    }

    #discovery-container {
        width: 70;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }

    .discovery-title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .discovery-info {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #server-list {
        height: 10;
        margin-bottom: 1;
    }

    #button-container {
        height: auto;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    ListItem {
        padding: 1 2;
    }

    .server-name {
        text-style: bold;
        color: $accent;
    }

    .server-details {
        color: $text-muted;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "select", "Select"),
    ]

    def __init__(
        self,
        discovery: RoonDiscovery,
        connection_manager: ConnectionManager,
    ) -> None:
        """Initialize the discovery screen.

        Args:
            discovery: RoonDiscovery instance
            connection_manager: ConnectionManager instance
        """
        super().__init__()
        self.discovery = discovery
        self.connection_manager = connection_manager
        self.servers: List[ServerInfo] = []
        self.selected_server: Optional[ServerInfo] = None

    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        with Container(id="discovery-container"):
            yield Label("Discover Roon Servers", classes="discovery-title")
            yield Label(
                "Searching for Roon Core servers on your network...",
                classes="discovery-info",
            )

            yield ListView(id="server-list")

            with Container(id="button-container"):
                yield Button("Select", id="btn-select", variant="primary")
                yield Button("Refresh", id="btn-refresh", variant="default")
                yield Button("Cancel", id="btn-cancel", variant="error")

    def on_mount(self) -> None:
        """Handle screen mount event."""
        self._discover_servers()

    def _discover_servers(self) -> None:
        """Discover Roon servers and populate the list."""
        logger.info("Discovering Roon servers")

        # Clear existing servers
        self.servers = []
        server_list = self.query_one("#server-list", ListView)
        server_list.clear()

        # Discover servers
        discovered = self.discovery.discover_servers(timeout=5)

        if not discovered:
            logger.warning("No servers discovered")
            server_list.append(
                ListItem(Label("No Roon servers found. Make sure Roon Core is running."))
            )
            return

        # Add discovered servers to the list
        self.servers = discovered
        for server in self.servers:
            server_item = ListItem(
                Vertical(
                    Label(server.core_name, classes="server-name"),
                    Label(
                        f"{server.host}:{server.http_port} - {server.display_version}",
                        classes="server-details",
                    ),
                )
            )
            server_list.append(server_item)

        logger.info(f"Found {len(self.servers)} server(s)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events.

        Args:
            event: Button press event
        """
        button_id = event.button.id

        if button_id == "btn-select":
            self.action_select()
        elif button_id == "btn-refresh":
            self._discover_servers()
        elif button_id == "btn-cancel":
            self.action_cancel()

    def action_select(self) -> None:
        """Select the highlighted server and connect."""
        if not self.servers:
            self.app.notify("No servers available to select", severity="warning")
            return

        server_list = self.query_one("#server-list", ListView)

        if server_list.index is None or server_list.index >= len(self.servers):
            self.app.notify("Please select a server from the list", severity="warning")
            return

        selected_server = self.servers[server_list.index]
        logger.info(f"Selected server: {selected_server.core_name}")

        # Connect to the selected server
        if self.connection_manager.connect(selected_server):
            self.app.notify(
                f"Connecting to {selected_server.core_name}. Please authorize in Roon.",
                severity="information",
            )
            self.selected_server = selected_server
            self.dismiss(selected_server)
        else:
            self.app.notify("Failed to connect to server", severity="error")

    def action_cancel(self) -> None:
        """Cancel discovery and return to main screen."""
        logger.info("Discovery cancelled")
        self.dismiss(None)
