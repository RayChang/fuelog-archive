"""Tests for CLI command registration and the fetch command."""

from typer.testing import CliRunner

from fuelog_crawler.cli import app

runner = CliRunner()


def test_commands_are_registered():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    for command in ("fetch", "info", "config"):
        assert command in result.output


def test_fetch_accepts_date_range():
    result = runner.invoke(app, ["fetch", "-b", "CPC", "-d", "2025-08-01:2025-08-10"])

    assert result.exit_code == 0
    assert "2025-08-01 to 2025-08-10" in result.output


def test_fetch_rejects_invalid_date():
    result = runner.invoke(app, ["fetch", "-b", "CPC", "-d", "not-a-date"])

    assert result.exit_code == 1
    assert "Invalid date format" in result.output
