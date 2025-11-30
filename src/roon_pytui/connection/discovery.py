"""Roon server discovery using the Roon API."""

import logging
import os.path
import socket
from typing import List

from roonapi.constants import SOOD_MULTICAST_IP, SOOD_PORT
from roonapi.soodmessage import FormatException, SOODMessage

from ..models.connection import ServerInfo

logger = logging.getLogger(__name__)


class RoonDiscovery:
    """Handles discovery of Roon Core servers on the local network."""

    def __init__(self) -> None:
        """Initialize the discovery service."""
        pass

    def discover_servers(self, timeout: int = 5) -> List[ServerInfo]:
        """Discover Roon Core servers on the local network.

        Args:
            timeout: Discovery timeout in seconds

        Returns:
            List of discovered ServerInfo objects
        """
        logger.info(f"Starting Roon server discovery (timeout: {timeout}s)")

        try:
            # Read the SOOD query message from the roonapi package
            import roonapi

            roonapi_dir = os.path.dirname(os.path.abspath(roonapi.__file__))
            sood_file = os.path.join(roonapi_dir, ".soodmsg")

            with open(sood_file, "rb") as sood_query_file:
                query_msg = sood_query_file.read()

            servers = []
            seen_unique_ids = set()

            # Create UDP socket for discovery
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
                # Send multicast query
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
                sock.sendto(query_msg, (SOOD_MULTICAST_IP, SOOD_PORT))

                # Send broadcast query
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(query_msg, ("<broadcast>", SOOD_PORT))

                # Set timeout and listen for responses
                sock.settimeout(timeout)

                while True:
                    try:
                        data, server_addr = sock.recvfrom(1024)

                        # Parse the SOOD response message
                        try:
                            message = SOODMessage(data).as_dictionary
                            properties = message.get("properties", {})

                            host = server_addr[0]
                            unique_id = properties.get("unique_id", "")
                            name = properties.get("name", "Unknown")
                            display_version = properties.get("display_version", "Unknown")
                            http_port = int(properties.get("http_port", 9100))

                            # Skip duplicates (same server may respond to both
                            # multicast and broadcast)
                            if unique_id in seen_unique_ids:
                                logger.debug(f"Skipping duplicate server: {name} ({unique_id})")
                                continue

                            seen_unique_ids.add(unique_id)

                            # Create ServerInfo object
                            server = ServerInfo(
                                core_id=unique_id,
                                core_name=name,
                                display_version=display_version,
                                host=host,
                                http_port=http_port,
                            )

                            servers.append(server)
                            logger.info(
                                f"Discovered server: {server.core_name} "
                                f"({server.host}:{server.http_port})"
                            )

                        except FormatException as e:
                            logger.warning(f"Failed to parse SOOD message: {e.message}")
                            continue

                    except socket.timeout:
                        logger.debug("Discovery timeout reached")
                        break
                    except Exception as e:
                        logger.error(f"Error receiving discovery response: {e}")
                        break

            logger.info(f"Discovery complete. Found {len(servers)} server(s)")
            return servers

        except FileNotFoundError:
            logger.error("SOOD query file not found in roonapi package")
            return []
        except Exception as e:
            logger.error(f"Discovery failed: {e}")
            return []

    def stop(self) -> None:
        """Stop the discovery service.

        Note: This implementation doesn't use a background thread,
        so there's nothing to stop. This method is kept for API compatibility.
        """
        pass
