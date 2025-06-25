#!/usr/bin/env python3
"""twat_speech:

Created by Adam Twardoch
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration settings for twat_speech."""

    name: str
    value: str | int | float
    options: dict[str, Any] | None = None


def process_data(
    data: list[Any], config: Config | None = None, *, debug: bool = False
) -> dict[str, Any]:
    """Process the input data according to configuration.

    Args:
        data: Input data to process
        config: Optional configuration settings
        debug: Enable debug mode

    Returns:
        Processed data as a dictionary

    Raises:
        ValueError: If input data is invalid
    """
    # Store original logger level to restore it later if needed,
    # or decide if this function should directly manipulate the global logger level.
    # For simplicity, current approach directly sets level based on debug flag.
    original_level = logger.level
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled for process_data call.")
    elif logger.level > logging.INFO:  # e.g. if it was WARNING or ERROR
        logger.setLevel(logging.INFO)

    if not data:
        msg = "Input data cannot be empty"
        if debug:  # Restore level if we are about to raise an error
            logger.setLevel(original_level)
        raise ValueError(msg)

    logger.debug("Starting data processing with %d items.", len(data))

    # TODO: Implement actual data processing logic here.
    # The following is placeholder logic.
    if config:
        logger.info(
            "Processing with configuration: %s (value: %s)", config.name, config.value
        )
        if config.options:
            logger.debug("Configuration options: %s", config.options)
    else:
        logger.info("Processing without specific configuration.")

    # Simulate some processing
    processed_items_count = 0
    for item in data:
        logger.debug("Processing item: %s", item)
        # Simulate work on item
        processed_items_count += 1

    result: dict[str, Any] = {
        "status": "completed",
        "items_received": len(data),
        "items_processed": processed_items_count,
        "config_name": config.name if config else None,
    }
    logger.info("Data processing finished. %d items processed.", processed_items_count)

    if debug:  # Restore original logger level after successful processing in debug mode
        logger.setLevel(original_level)
        logger.debug(
            "Restored logger level to %s after process_data call.",
            logging.getLevelName(original_level),
        )

    return result


def main() -> None:
    """Main entry point for demonstrating twat_speech functionality."""
    logger.info("Starting twat_speech main demonstration.")

    # Example 1: Processing with configuration and debug mode
    try:
        logger.info("--- Example 1: Processing with config and debug ---")
        config1 = Config(
            name="audio_analysis",
            value="mfcc",
            options={"frames": 1024, "normalize": True},
        )
        data1 = ["sample_audio1.wav", "sample_audio2.wav"]
        result1 = process_data(data1, config=config1, debug=True)
        logger.info("Example 1 completed. Result: %s", result1)
    except ValueError as ve:
        logger.error("Example 1: ValueError: %s", ve)
    except Exception as e:
        logger.exception("Example 1: An unexpected error occurred: %s", e)

    logger.info("-" * 30)

    # Example 2: Processing with no configuration
    try:
        logger.info("--- Example 2: Processing without config ---")
        data2 = ["text_data_item"]
        result2 = process_data(data2)  # debug=False by default
        logger.info("Example 2 completed. Result: %s", result2)
    except ValueError as ve:
        logger.error("Example 2: ValueError: %s", ve)
    except Exception as e:
        logger.exception("Example 2: An unexpected error occurred: %s", e)

    logger.info("-" * 30)

    # Example 3: Attempting to process empty data (expect ValueError)
    try:
        logger.info("--- Example 3: Processing empty data (expecting ValueError) ---")
        config3 = Config(name="empty_test", value=0)
        process_data([], config=config3, debug=True)
        # This line should not be reached
        logger.info("Example 3 completed without expected error (THIS IS UNEXPECTED).")
    except ValueError as ve:
        logger.warning("Example 3: Caught expected ValueError: %s", ve)
    except Exception as e:
        logger.exception("Example 3: An unexpected error occurred: %s", e)

    logger.info("-" * 30)
    logger.info("twat_speech main demonstration finished.")
    # In a real CLI, you might exit with a status code here.
    # For this library module, the main() is primarily for demonstration.


if __name__ == "__main__":
    # This makes the script runnable and demonstrates its behavior.
    # BasicConfig is already called at module level, so logs will appear.
    main()
