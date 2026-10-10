from datetime import UTC, date, datetime

import typer

from .config import FuelogCliConfig
from .exceptions import DatabaseConfigError


def parse_date_range(date_input: str) -> tuple[date, date | None]:
    """
    Parse date string into (start_date, end_date).
    Supports:
    - '2025-08-01' → (2025-08-01, None)
    - '2025-08-01:2025-08-10' → (2025-08-01, 2025-08-10)
    """
    try:
        if ":" in date_input:
            start_str, end_str = date_input.split(":")
            start = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=UTC).date()
            end = datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=UTC).date()
            if end < start:
                raise ValueError("End date cannot be earlier than start date")
            return start, end
        else:
            single = (
                datetime.strptime(date_input, "%Y-%m-%d").replace(tzinfo=UTC).date()
            )
            return single, None
    except ValueError as e:
        raise typer.BadParameter(f"Failed to parse date format: {e}") from e


def check_database_config(config: FuelogCliConfig) -> None:
    """
    Check if all required database configuration parameters are set.

    Args:
        config: FuelogCliConfig instance

    Raises:
        DatabaseConfigError: If any required database parameter is missing
    """
    required_params: dict[str, str | int | None] = {
        "db_host": config.db_host,
        "db_port": config.db_port,
        "db_name": config.db_name,
        "db_user": config.db_user,
        "db_password": config.db_password,
    }

    missing_params = [
        param for param, value in required_params.items() if value is None
    ]

    if missing_params:
        missing_list = ", ".join(missing_params)
        raise DatabaseConfigError(
            f"Missing required database configuration parameters: {missing_list}. "
            "Please set these parameters in your config and try again."
        )


def test_database_connection(config: FuelogCliConfig) -> bool:
    """
    Test database connection with the provided configuration.

    Args:
        config: FuelogCliConfig instance

    Returns:
        bool: True if connection successful

    Raises:
        DatabaseConfigError: If connection fails or config is invalid
    """
    # First check if all required parameters are set
    check_database_config(config)

    try:
        # Try to import psycopg2 or asyncpg for PostgreSQL connection
        try:
            import psycopg2  # type: ignore[import-untyped]

            connection_lib = "psycopg2"
        except ImportError:
            try:
                import asyncpg  # type: ignore[import-not-found]

                connection_lib = "asyncpg"
            except ImportError:
                raise DatabaseConfigError(
                    "No PostgreSQL driver found. Please install psycopg2 or asyncpg: "
                    "pip install psycopg2-binary or pip install asyncpg"
                ) from None

        # Test connection based on available library
        if connection_lib == "psycopg2":
            conn = psycopg2.connect(
                host=config.db_host,
                port=config.db_port,
                database=config.db_name,
                user=config.db_user,
                password=config.db_password,
                sslmode="require" if config.db_ssl else "disable",
                connect_timeout=5,
            )
            conn.close()

        elif connection_lib == "asyncpg":
            import asyncio

            async def test_asyncpg():
                conn = await asyncpg.connect(
                    host=config.db_host,
                    port=config.db_port,
                    database=config.db_name,
                    user=config.db_user,
                    password=config.db_password,
                    ssl="require" if config.db_ssl else "disable",
                    command_timeout=5,
                )
                await conn.close()

            asyncio.run(test_asyncpg())

        return True

    except Exception as e:
        raise DatabaseConfigError(
            f"Failed to connect to database: {e}. "
            "Please check your database configuration and ensure the database is "
            "accessible."
        ) from e
