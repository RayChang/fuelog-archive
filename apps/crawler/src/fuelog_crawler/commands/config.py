"""
Config management commands for Fuelog CLI.
"""

from typing import Annotated

import typer

from ..config import FuelogCliConfig

# Create a sub-application for config commands
config_app = typer.Typer(help="⚙️ Manage Fuelog configuration")


@config_app.command("list")
def config_list() -> None:
    """List all configuration parameters."""
    config = FuelogCliConfig.load_from_file()
    fields = config.list_fields()

    print("📋 Current Fuelog Configuration:")
    print("=" * 50)

    for field_name, field_info in fields.items():
        value = field_info["value"]
        description = field_info["description"]

        # Mask sensitive fields
        if "password" in field_name.lower():
            display_value = "***" if value else None
        else:
            display_value = value

        print(f"{field_name:15} = {display_value}")
        print(f"{'':15}   {description}")
        print()


@config_app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Configuration key to set")],
    value: Annotated[str, typer.Argument(help="Value to set")],
) -> None:
    """Set a configuration parameter."""
    try:
        config = FuelogCliConfig.load_from_file()
        config.set_field(key, value)
        config.save_to_file()

        # Show confirmation
        display_value = "***" if "password" in key.lower() else value
        print(f"✅ Set {key} = {display_value}")

    except ValueError as e:
        print(f"❌ Error: {e}")
        raise typer.Exit(1) from e
    except Exception as e:
        print(f"❌ Failed to set configuration: {e}")
        raise typer.Exit(1) from e


@config_app.command("get")
def config_get(
    key: Annotated[str, typer.Argument(help="Configuration key to get")],
) -> None:
    """Get a configuration parameter value."""
    try:
        config = FuelogCliConfig.load_from_file()
        value = config.get_field(key)

        # Mask sensitive fields
        if "password" in key.lower():
            display_value = "***" if value else None
        else:
            display_value = value

        print(f"{key} = {display_value}")

    except ValueError as e:
        print(f"❌ Error: {e}")
        raise typer.Exit(1) from e
    except Exception as e:
        print(f"❌ Failed to get configuration: {e}")
        raise typer.Exit(1) from e


@config_app.command("path")
def config_path() -> None:
    """Show the path to the configuration file."""
    config_path = FuelogCliConfig.get_config_path()
    print(f"📁 Configuration file: {config_path}")

    if config_path.exists():
        print("✅ File exists")
    else:
        print("⚠️  File does not exist (will be created on first use)")
