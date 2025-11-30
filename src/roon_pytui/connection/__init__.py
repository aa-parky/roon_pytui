"""Connection module for Roon API discovery and authentication."""

from .discovery import RoonDiscovery
from .manager import ConnectionManager

__all__ = ["RoonDiscovery", "ConnectionManager"]
