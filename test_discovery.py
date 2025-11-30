#!/usr/bin/env python3
"""Test script to diagnose Roon discovery issues."""

import logging
import sys

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from roon_pytui.connection.discovery import RoonDiscovery

logger = logging.getLogger(__name__)

def main():
    """Run discovery test."""
    logger.info("=" * 60)
    logger.info("Roon Discovery Diagnostic Test")
    logger.info("=" * 60)
    logger.info("")
    logger.info("This will attempt to discover Roon servers on your network.")
    logger.info("Make sure:")
    logger.info("  1. Roon Core is running")
    logger.info("  2. Your computer is on the same network as Roon Core")
    logger.info("  3. No firewall is blocking UDP traffic")
    logger.info("")
    logger.info("Starting discovery (10 second timeout)...")
    logger.info("")

    discovery = RoonDiscovery()
    servers = discovery.discover_servers(timeout=10)

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"Discovery complete. Found {len(servers)} server(s)")
    logger.info("=" * 60)

    if servers:
        for i, server in enumerate(servers, 1):
            logger.info(f"\nServer {i}:")
            logger.info(f"  Name: {server.core_name}")
            logger.info(f"  ID: {server.core_id}")
            logger.info(f"  Host: {server.host}")
            logger.info(f"  Port: {server.http_port}")
            logger.info(f"  Version: {server.display_version}")
    else:
        logger.warning("\nNo servers found. Possible issues:")
        logger.warning("  - Roon Core is not running")
        logger.warning("  - Roon Core is on a different network")
        logger.warning("  - Firewall is blocking discovery (UDP port 9003)")
        logger.warning("  - Network doesn't support multicast/broadcast")
        logger.warning("")
        logger.warning("Try checking:")
        logger.warning("  1. Can you access Roon from other devices on this network?")
        logger.warning("  2. Is your Mac's firewall enabled? (System Settings → Network)")
        logger.warning("  3. Are you connected via WiFi or Ethernet?")

if __name__ == "__main__":
    main()
