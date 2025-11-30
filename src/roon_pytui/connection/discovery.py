"""Roon server discovery using the Roon API."""

import logging
import os.path
import socket
from typing import List, Set

from roonapi.constants import SOOD_MULTICAST_IP, SOOD_PORT
from roonapi.soodmessage import FormatException, SOODMessage

from ..models.connection import ServerInfo

logger = logging.getLogger(__name__)


def _get_broadcast_addresses() -> Set[str]:
    """Get broadcast addresses for all network interfaces.

    Returns:
        Set of broadcast addresses
    """
    import netifaces

    broadcast_addrs = set()

    # Add the generic broadcast address
    broadcast_addrs.add("255.255.255.255")

    try:
        # Get all network interfaces
        for interface in netifaces.interfaces():
            try:
                addrs = netifaces.ifaddresses(interface)
                # Check for IPv4 addresses
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        # Get broadcast address if available
                        if "broadcast" in addr_info:
                            broadcast_addrs.add(addr_info["broadcast"])
            except (ValueError, KeyError) as e:
                logger.debug(f"Could not get broadcast address for {interface}: {e}")
                continue

    except Exception as e:
        logger.warning(f"Failed to enumerate network interfaces: {e}")

    logger.debug(f"Found broadcast addresses: {broadcast_addrs}")
    return broadcast_addrs


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
                # Bind to any available address to allow sending
                sock.bind(("", 0))

                # Enable reuse of address
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                # Try to enable reuse of port (not available on all platforms)
                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except (AttributeError, OSError):
                    # SO_REUSEPORT not available on this platform
                    pass

                # Send multicast query
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
                try:
                    sock.sendto(query_msg, (SOOD_MULTICAST_IP, SOOD_PORT))
                    logger.debug("Sent multicast discovery query")
                except OSError as e:
                    logger.warning(f"Failed to send multicast query: {e}")

                # Send broadcast queries to all network interfaces
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                broadcast_addrs = _get_broadcast_addresses()
                for bcast_addr in broadcast_addrs:
                    try:
                        sock.sendto(query_msg, (bcast_addr, SOOD_PORT))
                        logger.debug(f"Sent broadcast discovery query to {bcast_addr}")
                    except OSError as e:
                        logger.debug(f"Failed to send broadcast to {bcast_addr}: {e}")

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
