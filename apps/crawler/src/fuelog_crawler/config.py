import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class FuelogCliConfig(BaseModel):
    # Crawler settings
    rate_limit: float = 1.0  # seconds between requests
    user_agent: str = "Fuelog-Crawler/0.1.0"
    timeout: int = 30
    output_format: str = "json"

    # Optional fields for advanced configuration
    max_depth: int | None = None
    follow_links: bool = True

    # Database connection settings
    db_host: str | None = Field(default=None, description="PostgreSQL host")
    db_port: int | None = Field(default=5432, description="PostgreSQL port")
    db_name: str | None = Field(default=None, description="Database name")
    db_user: str | None = Field(default=None, description="Database username")
    db_password: str | None = Field(default=None, description="Database password")
    db_ssl: bool = Field(default=True, description="Use SSL for database connection")

    @classmethod
    def get_config_path(cls) -> Path:
        """Get the path to the configuration file."""
        config_dir = Path.home() / ".fuelog"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"

    @classmethod
    def load_from_file(cls) -> "FuelogCliConfig":
        """Load configuration from file, create default if not exists."""
        config_path = cls.get_config_path()

        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except (json.JSONDecodeError, Exception):  # noqa: S110
                # If config file is corrupted, create new default
                pass

        # Create default config and save it
        config = cls()
        config.save_to_file()
        return config

    def save_to_file(self) -> None:
        """Save current configuration to file."""
        config_path = self.get_config_path()

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, indent=2, ensure_ascii=False)

    def get_field(self, key: str) -> Any:
        """Get a specific configuration field value."""
        if not hasattr(self, key):
            raise ValueError(f"Configuration field '{key}' does not exist")
        return getattr(self, key)

    def set_field(self, key: str, value: Any) -> None:
        """Set a specific configuration field value with validation."""
        if not hasattr(self, key):
            raise ValueError(f"Configuration field '{key}' does not exist")

        # Get field info from the model
        field_info = self.__class__.model_fields.get(key)
        if not field_info:
            raise ValueError(f"Invalid configuration field '{key}'")

        # Type conversion based on field annotation
        field_type = field_info.annotation

        # Handle Union types (e.g., str | None)
        if hasattr(field_type, "__args__"):
            args = getattr(field_type, "__args__", None)
            if args:
                # Get the first non-None type for conversion
                for arg in args:
                    if arg is not type(None):
                        field_type = arg
                        break

        # Convert value to appropriate type
        if field_type is bool:
            if isinstance(value, str):
                value = value.lower() in ("true", "1", "yes", "on")
        elif field_type is int:
            value = int(value)
        elif field_type is float:
            value = float(value)
        elif field_type is str:
            value = str(value)

        # Set the value
        setattr(self, key, value)

    def list_fields(self) -> dict[str, dict[str, Any]]:
        """List all configuration fields with their current values and descriptions."""
        result: dict[str, dict[str, Any]] = {}

        for field_name, field_info in self.__class__.model_fields.items():
            current_value = getattr(self, field_name)
            description = field_info.description or "No description"

            result[field_name] = {
                "value": current_value,
                "description": description,
                "type": str(field_info.annotation),
            }

        return result
