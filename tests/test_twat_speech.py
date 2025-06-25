"""Test suite for twat_speech."""

import logging

import pytest

from twat_speech import __version__ as pkg_version
from twat_speech.twat_speech import Config, process_data


def test_version() -> None:
    """Verify package exposes version."""
    assert pkg_version is not None
    # A more robust check could be to ensure it matches a pattern e.g., SemVer
    assert isinstance(pkg_version, str)


def test_process_data_empty_input_raises_value_error() -> None:
    """Test process_data raises ValueError for empty data."""
    with pytest.raises(ValueError, match="Input data cannot be empty"):
        process_data([])


def test_process_data_with_valid_data_no_config() -> None:
    """Test process_data with valid data and no config."""
    # Current implementation of process_data is a placeholder.
    # This test will need to be updated when actual logic is added.
    # For now, it expects an empty dict if data is provided.
    data = ["some", "data"]
    result = process_data(data)
    assert isinstance(result, dict)
    assert result["status"] == "completed"
    assert result["items_received"] == len(data)
    assert result["items_processed"] == len(data)
    assert result["config_name"] is None


def test_process_data_with_valid_data_and_config() -> None:
    """Test process_data with valid data and a config object."""
    data = ["item1", "item2"]
    config = Config(name="test_config", value=123, options={"opt1": True})
    result = process_data(data, config=config)
    assert isinstance(result, dict)
    assert result["status"] == "completed"
    assert result["items_received"] == len(data)
    assert result["items_processed"] == len(data)
    assert result["config_name"] == config.name


def test_process_data_debug_mode_logs_debug_message(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test process_data enables debug logging when debug=True."""
    data = ["debug_test"]
    # caplog is a pytest fixture to capture log output
    with caplog.at_level(logging.DEBUG, logger="twat_speech.twat_speech"):
        process_data(data, debug=True)
        assert "Debug mode enabled" in caplog.text

    # Ensure debug mode is not sticky (check if a subsequent call without debug=True doesn't log)
    caplog.clear()
    with caplog.at_level(logging.DEBUG, logger="twat_speech.twat_speech"):
        # Need to re-get the logger or use the specific logger instance if it's stored globally
        # For this test, we assume logger level resets or is not affected globally by one call.
        # A more robust way would be to check the logger's level directly if possible or
        # ensure the handler's level is reset.
        # However, the current implementation of process_data re-sets level on each call.
        process_data(data, debug=False)  # Or just process_data(data)
        assert "Debug mode enabled" not in caplog.text


def test_config_dataclass() -> None:
    """Test the Config dataclass instantiation and attributes."""
    name = "test_name"
    value = 42.0
    options = {"key": "val"}
    config = Config(name=name, value=value, options=options)
    assert config.name == name
    assert config.value == value
    assert config.options == options

    config_no_options = Config(name="no_opts", value="a_string")
    assert config_no_options.name == "no_opts"
    assert config_no_options.value == "a_string"
    assert config_no_options.options is None


# TODO: Add more tests as the functionality of process_data evolves.
# For example:
# - Tests for different types of data in the input list.
# - Tests for different configurations and their effects on the output.
# - Tests for how `config.options` are used.
