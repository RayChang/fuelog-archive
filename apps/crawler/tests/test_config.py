"""Tests for the persistent CLI configuration."""

from pathlib import Path

import pytest

from fuelog_crawler.config import FuelogCliConfig


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    """Keep config files out of the real home directory."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    return tmp_path


def test_load_creates_default_config_file(isolated_home):
    config = FuelogCliConfig.load_from_file()

    assert config.db_port == 5432
    assert (isolated_home / ".fuelog" / "config.json").exists()


def test_saved_values_survive_reload():
    config = FuelogCliConfig.load_from_file()
    config.set_field("db_host", "localhost")
    config.save_to_file()

    assert FuelogCliConfig.load_from_file().db_host == "localhost"


def test_set_field_converts_string_input():
    config = FuelogCliConfig()

    config.set_field("db_port", "6543")
    config.set_field("db_ssl", "false")
    config.set_field("rate_limit", "2.5")

    assert config.db_port == 6543
    assert config.db_ssl is False
    assert config.rate_limit == 2.5


def test_unknown_field_is_rejected():
    config = FuelogCliConfig()

    with pytest.raises(ValueError, match="does not exist"):
        config.set_field("nope", "1")
    with pytest.raises(ValueError, match="does not exist"):
        config.get_field("nope")
