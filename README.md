# twat-speech

**`twat-speech`** is a Python library, part of the `twat` ecosystem, designed to provide a solid foundation for speech processing tasks. It serves as both a functional module and an extensible template for developers looking to build, test, and maintain speech-related applications using modern Python tools and best practices.

## Rationale

The `twat-speech` library was created to offer a standardized, extensible foundation for speech data manipulation and analysis. Many projects require common preprocessing, feature extraction, or transformation steps for speech signals. This library aims to encapsulate such functionalities in a reusable manner, integrated with modern Python development tools like Hatch, Ruff, Mypy, and `uv` for a streamlined development experience. It also serves as an example of how to structure a Python library with comprehensive QA, CI/CD, and clear contribution guidelines.

## Features Overview

*   **Modern Python Development:** Built with PEP 621 compliance using [Hatch](https://hatch.pypa.io/).
*   **Accelerated Workflows:** Supports [uv](https://github.com/astral-sh/uv) for fast environment and dependency management (used by Hatch automatically if available).
*   **High Code Quality:** Enforced through [Ruff](https://github.com/astral-sh/ruff) for linting and formatting, and [Mypy](https://mypy-lang.org/) for static type checking.
*   **Automated Versioning:** Git tag-based versioning powered by [hatch-vcs](https://github.com/ofek/hatch-vcs).
*   **Robust Testing:** Comprehensive test suite using [pytest](https://pytest.org/).
*   **CI/CD:** Automated testing, building, and releasing via GitHub Actions.
*   **Pre-commit Hooks:** For maintaining code standards before commits.
*   **`twat` Ecosystem Plugin:** Designed to integrate as a plugin.

---

## Part 1: General Information

This part of the documentation is for a wider audience, including those who may want to use `twat-speech` or understand its general purpose.

### What is `twat-speech`?

`twat-speech` aims to simplify the development of applications that handle speech data. While its core processing logic is designed to be extended, it provides a structured environment for common tasks such as:

*   Preprocessing audio data (e.g., normalization, resampling – *future capability*)
*   Extracting acoustic features (e.g., MFCCs, spectrograms – *future capability*)
*   Interfacing with speech recognition models or services (*future capability*)
*   Managing configurations for different speech processing pipelines.

The library is built with a focus on robustness, configurability, and a clean development experience.

### Who is it for?

`twat-speech` is for:

*   **Python Developers:** Anyone building applications that involve audio or speech data.
*   **Researchers:** Those who need a reliable framework for experimenting with speech processing algorithms.
*   **Hobbyists:** Individuals exploring speech technology and looking for a well-structured starting point.
*   **Users of the `twat` ecosystem:** If you're already using other `twat` tools, `twat-speech` integrates naturally as a plugin.

### Why is it useful?

*   **Modern Tooling:** Leverages Hatch, Ruff, Mypy, and pytest, ensuring code quality and maintainability.
*   **Extensible by Design:** Its core functions are meant to be expanded or replaced by more specific speech processing logic.
*   **Best Practices Template:** Serves as an excellent example of setting up a Python library with comprehensive QA, CI/CD, and clear contribution guidelines.
*   **Accelerated Development:** Helps you get started quickly on speech-related projects without boilerplate setup.
*   **`twat` Ecosystem Integration:** Designed to work as a plugin within the broader `twat` family of tools.

### Installation

You can install `twat-speech` from PyPI using `pip` or `uv`:

```bash
# Using pip
pip install twat-speech

# Or using uv (recommended for faster performance)
uv pip install twat-speech
```

### Usage

#### Programmatic Usage

The primary way to use `twat-speech` is by importing it into your Python projects. The library centers around a `process_data` function and a `Config` class for managing settings.

```python
import twat_speech
from twat_speech import Config, process_data

# Initialize configuration (optional)
# This allows you to define specific parameters for your speech processing tasks.
config = Config(
    name="my_custom_settings",
    value="alpha_params",
    options={"mode": "detailed_analysis", "threshold": 0.75}
)

# Sample data: This would typically be a list of audio file paths,
# raw audio data, or other speech-related inputs.
# The exact nature depends on the implemented processing logic.
data_to_process = ["path/to/audio1.wav", "another_audio_sample.mp3"]

# Process data
try:
    # The process_data function is currently a placeholder.
    # In a fully implemented version, it would perform speech-specific tasks
    # based on the input data and configuration.
    print(f"Attempting to process: {data_to_process} with config: {config.name}")
    result = process_data(data_to_process, config=config, debug=True)
    print(f"Processing successful. Result: {result}")

    # Example of processing without a specific configuration
    result_no_config = process_data(["simple_item.flac"])
    print(f"Processing with no config. Result: {result_no_config}")

except ValueError as e:
    # This error is raised if the input data list is empty.
    print(f"Error during processing: {e}")
except Exception as e:
    # Catch other potential errors
    print(f"An unexpected error occurred: {e}")

```
**Note:** The `process_data` function in the current version contains placeholder logic. As the library evolves, this function will be updated to perform actual speech processing tasks. The example above illustrates its intended interface.

#### Command-Line Demonstration

`twat-speech` includes a demonstration script within the library that you can run to see its basic operation and logging output. This is not a full-fledged CLI application but serves to illustrate the library's current capabilities.

To run the demonstration, navigate to the root directory of the project (if you have cloned the repository) or ensure `twat_speech` is in your Python path, then execute:

```bash
# If you are in the root of the cloned repository:
python src/twat_speech/twat_speech.py
```
Or, if the package is installed in your environment:
```bash
python -m twat_speech.twat_speech
```

This will run the `main()` function in `twat_speech.py`, which executes a few examples of calling `process_data`, including one that intentionally triggers an error, showcasing the logging and error handling.

---

## Part 2: Technical Details

This section provides a deeper dive into the codebase, development practices, and contribution guidelines for `twat-speech`.

### How the Code Works

The core logic of `twat-speech` resides primarily in `src/twat_speech/twat_speech.py`.

#### `src/twat_speech/twat_speech.py`

*   **`Config` Dataclass:**
    ```python
    from dataclasses import dataclass
    from typing import Any

    @dataclass
    class Config:
        name: str
        value: str | int | float
        options: dict[str, Any] | None = None
    ```
    This simple dataclass is used to pass structured configuration settings to processing functions. It holds a `name` for the configuration set, a primary `value`, and an optional dictionary `options` for more granular settings.

*   **`process_data(data: list[Any], config: Config | None = None, *, debug: bool = False) -> dict[str, Any]`:**
    This is the main function intended for data processing.
    *   **Parameters:**
        *   `data: list[Any]`: A list of items to be processed. The exact type of items (e.g., file paths, raw data) will depend on the specific implementation of the processing logic.
        *   `config: Config | None = None`: An optional `Config` object to guide the processing.
        *   `debug: bool = False`: A keyword-only argument. If `True`, it enables detailed debug logging for the function call.
    *   **Current Logic:** As of the current version, this function contains placeholder logic. It:
        1.  Adjusts the global logger level to `DEBUG` if `debug=True`, and restores it afterward.
        2.  Raises a `ValueError` if the input `data` list is empty.
        3.  Logs information about the data being processed and the configuration being used (if any).
        4.  Simulates item processing by iterating through the input `data`.
        5.  Returns a dictionary containing a status message, counts of items received and processed, and the name of the configuration used.
    *   **Extensibility:** This function is designed to be the primary point for implementing actual speech processing algorithms. Future development will replace the placeholder logic with concrete operations.

*   **`main() -> None`:**
    This function serves as a runnable demonstration of the library's capabilities. When `src/twat_speech/twat_speech.py` is executed as a script, `main()` is called. It showcases:
    1.  How to initialize `Config` objects.
    2.  How to call `process_data` with and without a `Config`, and with `debug` mode enabled/disabled.
    3.  An example of `process_data` handling an expected `ValueError` (when called with empty data).
    It utilizes the `logging` module to provide informative output about its operations.

*   **Logging:**
    The module configures basic logging using `logging.basicConfig` at the module level. The `process_data` function demonstrates dynamic adjustment of logging levels based on its `debug` parameter.

#### Project Structure and Tooling

The `pyproject.toml` file is central to the project's structure, dependency management, and tooling.

*   **Project Management with Hatch:**
    *   [Hatch](https://hatch.pypa.io/) is used for build processes, environment management, and running scripts.
    *   It uses `hatchling` as the build backend and `hatch-vcs` to derive the project version from Git tags (e.g., `v0.1.0`). The version is written to `src/twat_speech/__version__.py`.
*   **Code Quality Tools:**
    *   **[Ruff](https://github.com/astral-sh/ruff):** Used for extremely fast Python linting and code formatting. Configuration in `pyproject.toml`.
    *   **[Mypy](https://mypy-lang.org/):** Used for static type checking. Configuration in `pyproject.toml`.
*   **Testing with Pytest:**
    *   [pytest](https://pytest.org/) is the testing framework. Tests are in `tests/`. Configuration in `pyproject.toml`.
*   **Codebase Structure Overview:**
    ```
    .
    ├── .github/                # GitHub Actions workflows (CI/CD)
    ├── src/
    │   └── twat_speech/        # Main source code for the library
    │       ├── __init__.py
    │       ├── __version__.py  # Version managed by hatch-vcs
    │       └── twat_speech.py  # Core logic
    ├── tests/                  # Test suite
    │   └── test_twat_speech.py
    ├── .gitignore
    ├── .pre-commit-config.yaml # Pre-commit hook configurations
    ├── LICENSE
    ├── README.md               # This file
    └── pyproject.toml          # Project metadata and build configuration (PEP 621)
    ```

### Development and Contribution

We welcome contributions! Please adhere to the following guidelines.

#### Development Environment Setup

1.  **Prerequisites:**
    *   Python 3.10+
    *   [Git](https://git-scm.com/)
    *   [Hatch](https://hatch.pypa.io/latest/install/)
    *   (Highly Recommended) [uv](https://github.com/astral-sh/uv#installation) for significantly faster dependency management. Hatch will use `uv` automatically if available.

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/twardoch/twat-speech.git
    cd twat-speech
    ```

3.  **Install Hatch (if not already installed):**
    ```bash
    pip install hatch  # Or: uv pip install hatch
    ```

4.  **Install `uv` (Recommended):**
    Follow instructions at [astral.sh/uv#installation](https://astral.sh/uv#installation). E.g., for macOS/Linux:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

5.  **Activate Hatch Environment:**
    This creates a virtual environment and installs project dependencies.
    ```bash
    hatch shell
    ```

6.  **Install Pre-commit Hooks:**
    This helps maintain code quality by running checks before each commit.
    ```bash
    pre-commit install
    ```

#### Common Development Tasks

All commands should be run from within the activated Hatch environment (`hatch shell`).

*   **Run Tests:**
    ```bash
    hatch run test  # or simply: pytest
    ```
*   **Run Tests with Coverage:**
    ```bash
    hatch run test-cov
    ```
*   **Linting and Formatting (Ruff):**
    *   Check for issues (no changes made): `hatch run lint:style`
    *   Format code and fix issues: `hatch run lint:fmt`
*   **Static Type Checking (Mypy):**
    ```bash
    hatch run lint:typing
    ```
*   **Build the Package:**
    Creates wheel and sdist packages in `dist/`.
    ```bash
    hatch build
    ```

#### Coding Standards

*   **PEP 8:** Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
*   **Formatting & Linting:** Code is automatically formatted and linted by Ruff. Ensure `hatch run lint:fmt` passes.
*   **Type Hinting:** Use type hints. Ensure `hatch run lint:typing` (Mypy) passes.
*   **Comments:** Write clear comments for complex logic.

#### Testing

*   Write tests for new features/fixes in `tests/`.
*   Ensure all tests pass (`hatch run test`) and aim for high coverage.

#### Commit Messages

*   Follow [Conventional Commits](https://www.conventionalcommits.org/).
    *   Examples: `feat: add whisper ASR integration`, `fix: correct RMS energy calculation`.

#### Branching Strategy

*   Create branches from `main`: `feature/your-feature-name` or `bugfix/issue-id`.

#### Pull Requests (PRs)

*   Submit PRs to the `main` branch.
*   Provide clear descriptions and ensure CI checks pass.
*   Link to relevant issues.

#### Versioning and Releases

*   Semantic Versioning (SemVer: `MAJOR.MINOR.PATCH`) via `hatch-vcs` from Git tags.
*   Maintainers handle tagging and releases (automated via GitHub Actions).

## Project Links

*   **Documentation:** [https://github.com/twardoch/twat-speech#readme](https://github.com/twardoch/twat-speech#readme)
*   **Issue Tracker:** [https://github.com/twardoch/twat-speech/issues](https://github.com/twardoch/twat-speech/issues)
*   **Source Code:** [https://github.com/twardoch/twat-speech](https://github.com/twardoch/twat-speech)

## License

`twat-speech` is distributed under the terms of the MIT license. See the `LICENSE` file for details.
