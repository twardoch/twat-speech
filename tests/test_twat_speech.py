"""Test suite for twat_speech."""

import logging
import re
from typing import Any

import pytest

from twat_speech import __version__ as pkg_version
from twat_speech.twat_speech import Config, process_data, main


def test_version() -> None:
    """Verify package exposes version."""
    assert pkg_version is not None
    assert isinstance(pkg_version, str)
    # Test that version follows semantic versioning pattern (including hatch-vcs post-release versions)
    semver_pattern = r"^\d+\.\d+\.\d+(?:\.post\d+)?(?:\+.+)?$"
    assert re.match(semver_pattern, pkg_version), f"Version {pkg_version} doesn't match SemVer pattern"


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


def test_process_data_with_different_data_types() -> None:
    """Test process_data handles different data types in input."""
    mixed_data = ["string", 42, {"key": "value"}, [1, 2, 3]]
    result = process_data(mixed_data)
    assert result["status"] == "completed"
    assert result["items_processed"] == len(mixed_data)


def test_process_data_with_config_options() -> None:
    """Test process_data handles config options correctly."""
    data = ["test_item"]
    config = Config(
        name="complex_config",
        value="test_value",
        options={"option1": "value1", "option2": 42, "option3": True}
    )
    result = process_data(data, config=config, debug=True)
    assert result["config_name"] == "complex_config"
    assert result["status"] == "completed"


def test_process_data_logger_level_restoration() -> None:
    """Test that logger level is properly restored after debug mode."""
    import logging
    from twat_speech.twat_speech import logger
    
    original_level = logger.level
    data = ["test"]
    
    # Call with debug=True
    process_data(data, debug=True)
    
    # Verify logger level is restored
    assert logger.level == original_level


def test_main_function_execution(caplog: pytest.LogCaptureFixture) -> None:
    """Test main function executes without errors."""
    with caplog.at_level(logging.INFO):
        main()
        
    # Check that main function logged expected messages
    assert "Starting twat_speech main demonstration" in caplog.text
    assert "twat_speech main demonstration finished" in caplog.text
    assert "Example 1: Processing with config and debug" in caplog.text
    assert "Example 2: Processing without config" in caplog.text
    assert "Example 3: Processing empty data" in caplog.text


def test_config_with_different_value_types() -> None:
    """Test Config dataclass with different value types."""
    # Test with string value
    config_str = Config(name="str_config", value="test_string")
    assert config_str.value == "test_string"
    
    # Test with int value
    config_int = Config(name="int_config", value=42)
    assert config_int.value == 42
    
    # Test with float value
    config_float = Config(name="float_config", value=3.14)
    assert config_float.value == 3.14


def test_process_data_large_dataset() -> None:
    """Test process_data with larger dataset."""
    large_data = [f"item_{i}" for i in range(1000)]
    result = process_data(large_data)
    assert result["items_received"] == 1000
    assert result["items_processed"] == 1000
    assert result["status"] == "completed"


def test_process_data_error_handling_with_debug() -> None:
    """Test error handling preserves debug state."""
    import logging
    from twat_speech.twat_speech import logger
    
    original_level = logger.level
    
    # Test that logger level is restored even when error occurs
    with pytest.raises(ValueError):
        process_data([], debug=True)
    
    # Logger level should be restored after error
    assert logger.level == original_level


# Benchmark test for performance monitoring
def test_process_data_performance_benchmark() -> None:
    """Basic performance test for process_data."""
    data = [f"item_{i}" for i in range(100)]
    config = Config(name="perf_test", value="benchmark")
    
    import time
    start_time = time.time()
    result = process_data(data, config=config)
    end_time = time.time()
    
    # Should complete within reasonable time (adjust threshold as needed)
    assert end_time - start_time < 1.0  # Should complete in under 1 second
    assert result["status"] == "completed"
