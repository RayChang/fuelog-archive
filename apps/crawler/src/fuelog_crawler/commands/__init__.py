"""Commands module for Fuelog Crawler."""

import typer


def register_commands(app: typer.Typer) -> None:
    """Register all commands to the Typer app."""
    from .config import config_app
    from .get_retail_price import get_retail_price

    app.command(name="fetch", help="⛽️ Fetch fuel retail price.", no_args_is_help=True)(
        get_retail_price
    )

    # Add config sub-application
    app.add_typer(
        config_app,
        name="config",
        help="⚙️ Manage Fuelog configuration",
        no_args_is_help=True,
    )

    # Future commands can be added here:
    # from .update_database import update_fuel_database
    # app.command()(update_fuel_database)
