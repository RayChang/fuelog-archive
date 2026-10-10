"""
Fuelog Crawler Package

A CLI tool for data crawling, installable via uv tool install.
"""

try:
    from importlib.metadata import version

    __version__ = version("fuelog-crawler")
except ImportError:
    # Development fallback - read from pyproject.toml
    try:
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
            __version__ = pyproject["project"]["version"] + "-dev"
        else:
            __version__ = "0.1.0-dev"
    except Exception:
        # Ultimate fallback if tomllib or file reading fails
        __version__ = "0.1.0-dev"
