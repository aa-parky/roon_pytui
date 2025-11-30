"""Unit tests for the connection manager."""

import pytest
from unittest.mock import MagicMock, patch

from roon_pytui.connection.manager import ConnectionManager
from roon_pytui.models.connection import ConnectionState, ServerInfo


@pytest.fixture
def app_info() -> dict:
    """Fixture providing app info."""
    return {
        "extension_id": "com.test",
        "display_name": "Test",
        "display_version": "1.0.0",
        "publisher": "test",
        "email": "test@test.com",
    }


@pytest.fixture
def server_info() -> ServerInfo:
    """Fixture providing server info."""
    return ServerInfo(
        core_id="test-core-id",
        core_name="Test Core",
        display_version="1.0",
        host="192.168.1.100",
        http_port=9100,
    )


def test_connection_manager_init(app_info: dict) -> None:
    """Test ConnectionManager initialization."""
    manager = ConnectionManager(app_info)

    assert manager.state == ConnectionState.DISCONNECTED
    assert manager.api is None
    assert manager.current_server is None


def test_connection_manager_state_property(app_info: dict) -> None:
    """Test ConnectionManager state property."""
    manager = ConnectionManager(app_info)

    assert manager.state == ConnectionState.DISCONNECTED
    assert isinstance(manager.state, ConnectionState)
