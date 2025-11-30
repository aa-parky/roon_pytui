"""Connection manager for handling Roon API connections and authentication."""

import logging
from typing import Callable, Optional

from roonapi import RoonApi

from ..config.manager import ConfigManager
from ..models.connection import AuthenticationStatus, ConnectionState, ServerInfo

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages connection and authentication with Roon Core servers."""

    def __init__(
        self,
        app_info: dict,
        config_manager: Optional[ConfigManager] = None,
    ) -> None:
        """Initialize the connection manager.

        Args:
            app_info: Application information dict for Roon API
            config_manager: Configuration manager instance
        """
        self.app_info = app_info
        self.config_manager = config_manager or ConfigManager()
        self._api: Optional[RoonApi] = None
        self._state = ConnectionState.DISCONNECTED
        self._current_server: Optional[ServerInfo] = None
        self._auth_callback: Optional[Callable[[AuthenticationStatus], None]] = None

    @property
    def state(self) -> ConnectionState:
        """Get the current connection state."""
        return self._state

    @property
    def api(self) -> Optional[RoonApi]:
        """Get the RoonApi instance if connected."""
        return self._api

    @property
    def current_server(self) -> Optional[ServerInfo]:
        """Get information about the currently connected server."""
        return self._current_server

    def set_auth_callback(self, callback: Callable[[AuthenticationStatus], None]) -> None:
        """Set a callback to be notified of authentication status changes.

        Args:
            callback: Function to call with AuthenticationStatus updates
        """
        self._auth_callback = callback

    def connect(self, server: ServerInfo, token: Optional[str] = None) -> bool:
        """Connect to a Roon Core server.

        Args:
            server: ServerInfo for the server to connect to
            token: Optional authentication token from previous session

        Returns:
            True if connection initiated successfully, False otherwise
        """
        logger.info(f"Connecting to {server.core_name} at {server.host}:{server.http_port}")

        try:
            self._state = ConnectionState.CONNECTING
            self._current_server = server

            # Create RoonApi instance
            # The token parameter allows us to reuse a previously authorized token
            self._api = RoonApi(
                self.app_info,
                token=token,
                host=server.host,
                port=server.http_port,
            )

            # Register the authorization callback
            self._api.register_state_callback(self._on_state_change)

            # Start the connection
            self._state = ConnectionState.AUTHENTICATING
            logger.info("Connection initiated, waiting for authentication")

            return True

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self._state = ConnectionState.ERROR
            self._notify_auth_status(
                AuthenticationStatus(is_authenticated=False, error_message=str(e))
            )
            return False

    def _on_state_change(self, event: str, changed_items: list) -> None:
        """Handle state changes from the Roon API.

        Args:
            event: The event type
            changed_items: List of changed items
        """
        logger.debug(f"State change: event={event}, items={changed_items}")

        # Check if we're authorized
        if self._api and hasattr(self._api, "token") and self._api.token:
            logger.info("Authentication successful")
            self._state = ConnectionState.CONNECTED

            # Save the token for future use
            if self._current_server:
                self.config_manager.update(
                    core_id=self._current_server.core_id,
                    core_name=self._current_server.core_name,
                    token=self._api.token,
                    host=self._current_server.host,
                    port=self._current_server.http_port,
                )

            self._notify_auth_status(
                AuthenticationStatus(is_authenticated=True, token=self._api.token)
            )
        else:
            logger.info("Waiting for authorization from Roon Core")

    def _notify_auth_status(self, status: AuthenticationStatus) -> None:
        """Notify the auth callback of status changes.

        Args:
            status: AuthenticationStatus to send to callback
        """
        if self._auth_callback:
            try:
                self._auth_callback(status)
            except Exception as e:
                logger.error(f"Error in auth callback: {e}")

    def disconnect(self) -> None:
        """Disconnect from the current Roon Core server."""
        logger.info("Disconnecting from Roon Core")

        if self._api:
            try:
                self._api.stop()
            except Exception as e:
                logger.warning(f"Error during disconnect: {e}")
            finally:
                self._api = None

        self._state = ConnectionState.DISCONNECTED
        self._current_server = None

    def reconnect_from_config(self) -> bool:
        """Attempt to reconnect using saved configuration.

        Returns:
            True if reconnection was attempted, False if no saved config exists
        """
        config = self.config_manager.load()

        if not config.core_id or not config.host or not config.port:
            logger.info("No saved configuration found")
            return False

        logger.info(f"Attempting to reconnect to {config.core_name}")

        # Create ServerInfo from saved config
        server = ServerInfo(
            core_id=config.core_id,
            core_name=config.core_name or "Unknown",
            display_version="Unknown",
            host=config.host,
            http_port=config.port,
        )

        return self.connect(server, token=config.token)
