"""Configuration manager for storing and retrieving application settings."""

import json
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration model."""

    core_id: Optional[str] = Field(default=None, description="Last connected Roon Core ID")
    core_name: Optional[str] = Field(default=None, description="Last connected Roon Core name")
    token: Optional[str] = Field(default=None, description="Authentication token")
    host: Optional[str] = Field(default=None, description="Last connected host")
    port: Optional[int] = Field(default=None, description="Last connected port")


class ConfigManager:
    """Manages application configuration persistence."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize the configuration manager.

        Args:
            config_dir: Directory to store configuration files. Defaults to ~/.config/roon-pytui
        """
        if config_dir is None:
            config_dir = Path.home() / ".config" / "roon-pytui"

        self.config_dir = config_dir
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> AppConfig:
        """Load configuration from disk.

        Returns:
            AppConfig object with loaded settings, or default if file doesn't exist
        """
        if not self.config_file.exists():
            return AppConfig()

        try:
            with open(self.config_file) as f:
                data = json.load(f)
            return AppConfig(**data)
        except (json.JSONDecodeError, ValueError):
            # If config is corrupted, return default config
            return AppConfig()

    def save(self, config: AppConfig) -> None:
        """Save configuration to disk.

        Args:
            config: AppConfig object to save
        """
        self._ensure_config_dir()

        with open(self.config_file, "w") as f:
            json.dump(config.model_dump(), f, indent=2)

    def update(self, **kwargs: Any) -> AppConfig:
        """Update configuration with new values and save.

        Args:
            **kwargs: Configuration fields to update

        Returns:
            Updated AppConfig object
        """
        config = self.load()
        updated_data = config.model_dump()
        updated_data.update(kwargs)
        updated_config = AppConfig(**updated_data)
        self.save(updated_config)
        return updated_config

    def clear(self) -> None:
        """Clear all configuration data."""
        if self.config_file.exists():
            self.config_file.unlink()
