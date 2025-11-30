"""Unit tests for the configuration manager."""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from roon_pytui.config.manager import AppConfig, ConfigManager


@pytest.fixture
def temp_config_dir() -> Path:
    """Fixture providing a temporary config directory."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_config_manager_init(temp_config_dir: Path) -> None:
    """Test ConfigManager initialization."""
    manager = ConfigManager(temp_config_dir)

    assert manager.config_dir == temp_config_dir
    assert manager.config_file == temp_config_dir / "config.json"
    assert manager.config_dir.exists()


def test_config_manager_load_default(temp_config_dir: Path) -> None:
    """Test loading default config when file doesn't exist."""
    manager = ConfigManager(temp_config_dir)
    config = manager.load()

    assert isinstance(config, AppConfig)
    assert config.core_id is None
    assert config.token is None


def test_config_manager_save_and_load(temp_config_dir: Path) -> None:
    """Test saving and loading configuration."""
    manager = ConfigManager(temp_config_dir)

    config = AppConfig(
        core_id="test-core",
        core_name="Test Core",
        token="test-token",
        host="192.168.1.100",
        port=9100,
    )

    manager.save(config)
    loaded_config = manager.load()

    assert loaded_config.core_id == "test-core"
    assert loaded_config.core_name == "Test Core"
    assert loaded_config.token == "test-token"
    assert loaded_config.host == "192.168.1.100"
    assert loaded_config.port == 9100


def test_config_manager_update(temp_config_dir: Path) -> None:
    """Test updating configuration."""
    manager = ConfigManager(temp_config_dir)

    updated = manager.update(core_id="new-core", token="new-token")

    assert updated.core_id == "new-core"
    assert updated.token == "new-token"

    # Verify it was saved
    loaded = manager.load()
    assert loaded.core_id == "new-core"
    assert loaded.token == "new-token"


def test_config_manager_clear(temp_config_dir: Path) -> None:
    """Test clearing configuration."""
    manager = ConfigManager(temp_config_dir)

    manager.update(core_id="test", token="test")
    assert manager.config_file.exists()

    manager.clear()
    assert not manager.config_file.exists()
