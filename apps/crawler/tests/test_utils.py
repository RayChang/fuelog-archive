"""Tests for date parsing and database configuration checks."""

from datetime import date

import pytest
import typer

from fuelog_crawler.config import FuelogCliConfig
from fuelog_crawler.exceptions import DatabaseConfigError
from fuelog_crawler.utils import check_database_config, parse_date_range


def test_parse_single_date():
    assert parse_date_range("2025-08-01") == (date(2025, 8, 1), None)


def test_parse_date_range():
    assert parse_date_range("2025-08-01:2025-08-10") == (
        date(2025, 8, 1),
        date(2025, 8, 10),
    )


@pytest.mark.parametrize("value", ["2025/08/01", "2025-08-10:2025-08-01", "today"])
def test_parse_date_range_rejects_invalid_input(value):
    with pytest.raises(typer.BadParameter):
        parse_date_range(value)


def test_check_database_config_reports_missing_fields():
    with pytest.raises(DatabaseConfigError, match="db_host, db_name"):
        check_database_config(
            FuelogCliConfig(db_user="u", db_password="p")  # noqa: S106
        )


def test_check_database_config_accepts_complete_config():
    config = FuelogCliConfig(
        db_host="localhost",
        db_name="fuelog",
        db_user="u",
        db_password="p",  # noqa: S106
    )
    check_database_config(config)
