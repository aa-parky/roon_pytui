"""Roon server discovery using the Roon API."""

import logging
from typing import List, Optional

from roonapi import RoonDiscovery as RoonApiDiscovery

from ..models.connection import ServerInfo

logger = logging.getLogger(__name__)


class RoonDiscovery:
    """Handles discovery of Roon Core servers on the local network."""

    def __init__(self) -> None:
        """Initialize the discovery service."""
        self._discovery: Optional[RoonApiDiscovery] = None

    def discover_servers(self, timeout: int = 5) -> List[ServerInfo]:
        """Discover Roon Core servers on the local network.

        Args:
            timeout: Discovery timeout in seconds

        Returns:
            List of discovered ServerInfo objects
        """
        logger.info(f"Starting Roon server discovery (timeout: {timeout}s)")

        try:
            # Create a discovery instance
            self._discovery = RoonApiDiscovery(None)

            # The RoonApiDiscovery.all property returns a list of discovered servers
            # Each server is a dict with keys: core_id, core_name, display_version, host, http_port
            discovered = self._discovery.all

            servers = []
            for server_data in discovered:
                try:
                    server = ServerInfo(
                        core_id=server_data.get("core_id", ""),
                        core_name=server_data.get("core_name", "Unknown"),
                        display_version=server_data.get("display_version", "Unknown"),
                        host=server_data.get("host", ""),
                        http_port=server_data.get("http_port", 9100),
                    )
                    servers.append(server)
                    logger.info(f"Discovered server: {server.core_name} ({server.host})")
                except Exception as e:
                    logger.warning(f"Failed to parse server data: {e}")
                    continue

            logger.info(f"Discovery complete. Found {len(servers)} server(s)")
            return servers

        except Exception as e:
            logger.error(f"Discovery failed: {e}")
            return []

    def stop(self) -> None:
        """Stop the discovery service."""
        if self._discovery:
            try:
                self._discovery.stop()
            except Exception as e:
                logger.warning(f"Error stopping discovery: {e}")
            finally:
                self._discovery = None
