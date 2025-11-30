"""Connection-related data models."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ConnectionState(str, Enum):
    """Connection state enumeration."""

    DISCONNECTED = "disconnected"
    DISCOVERING = "discovering"
    CONNECTING = "connecting"
    AUTHENTICATING = "authenticating"
    CONNECTED = "connected"
    ERROR = "error"


class ServerInfo(BaseModel):
    """Information about a discovered Roon server."""

    core_id: str = Field(..., description="Unique identifier for the Roon Core")
    core_name: str = Field(..., description="Display name of the Roon Core")
    display_version: str = Field(..., description="Version string of the Roon Core")
    host: str = Field(..., description="IP address or hostname of the server")
    http_port: int = Field(..., description="HTTP port number")

    model_config = ConfigDict(frozen=True)


class AuthenticationStatus(BaseModel):
    """Authentication status information."""

    is_authenticated: bool = Field(default=False, description="Whether authentication is complete")
    token: Optional[str] = Field(default=None, description="Authentication token if available")
    error_message: Optional[str] = Field(
        default=None, description="Error message if authentication failed"
    )
