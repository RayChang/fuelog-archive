"""
Fuelog Crawler - Command Line Interface

This module provides the main CLI functionality for the Fuelog Crawler tool.
It serves as the primary entry point for both the installed command and
module execution.

The CLI provides basic web crawling capabilities with optional advanced features.
"""

import typer

from . import __version__
from .commands import register_commands

app = typer.Typer(
    help="⛽️ Fuelog Crawler CLI Tool",
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
)

# Register all commands from the commands module
register_commands(app)


@app.command()
def info():
    """Show tool info."""
    print(f"🚀 Fuelog Crawler v{__version__}")
    print("📝 A CLI tool scaffold installable via uv tool install")
    print("🔧 Ready to start your development...")


def main():
    app()


if __name__ == "__main__":
    main()
