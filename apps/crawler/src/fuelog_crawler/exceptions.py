class FuelogCliError(Exception):
    """Base exception for Fuelog CLI errors."""


class NetworkError(FuelogCliError):
    """Network-related errors."""


class DatabaseConfigError(FuelogCliError):
    """Database configuration error."""
