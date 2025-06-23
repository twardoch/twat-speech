# twat-speech

**twat-speech** is a Python library, part of the `twat` ecosystem, designed for processing speech-related data. Its primary goal is to provide a flexible and configurable way to handle various speech processing tasks. This project serves as a template and a functional module for developers working with speech data within Python environments, emphasizing modern tooling and best practices.

## Rationale

The `twat-speech` library was created to offer a standardized, extensible foundation for speech data manipulation and analysis. Many projects require common preprocessing, feature extraction, or transformation steps for speech signals. This library aims to encapsulate such functionalities in a reusable manner, integrated with modern Python development tools like Hatch, Ruff, Mypy, and `uv` for a streamlined development experience. It also serves as an example of how to structure a Python library with comprehensive QA, CI/CD, and clear contribution guidelines.

## Features

- Modern Python packaging with PEP 621 compliance using [Hatch](https://hatch.pypa.io/).
- Accelerated development workflows with [uv](https://github.com/astral-sh/uv) (used by Hatch automatically if available).
- Code formatting and linting with [Ruff](https://github.com/astral-sh/ruff).
- Static type checking with [Mypy](https://mypy-lang.org/).
- Versioning based on Git tags using [hatch-vcs](https://github.com/ofek/hatch-vcs).
- Comprehensive test suite using [pytest](https://pytest.org/).
- Automated CI/CD pipelines using GitHub Actions for testing, building, and releasing.
- Pre-commit hooks for maintaining code quality.

## Installation

To install `twat-speech` from PyPI:

```bash
pip install twat-speech
# Or using uv
uv pip install twat-speech
```

## Usage

```python
import twat_speech
from twat_speech import Config, process_data

# Example usage:
# The core function `process_data` is currently a placeholder.
# The following example demonstrates its expected interface.

# Initialize configuration (optional)
config = Config(name="my_settings", value="alpha", options={"mode": "fast", "threshold": 0.5})

# Sample data (e.g., a list of audio file paths, text transcriptions, or feature vectors)
# The exact nature of this data will depend on the implemented processing logic.
data_to_process = ["path/to/audio1.wav", "another_audio_sample.mp3", "text_input_example"]

# Process data
try:
    # The `process_data` function will contain the core logic of this library.
    # Currently, it returns an empty dictionary for any valid non-empty input.
    # When implemented, it will perform speech-related tasks based on the input data and config.
    print(f"Attempting to process: {data_to_process}")
    result = process_data(data_to_process, config=config, debug=True)
    print(f"Processing successful. Result: {result}")

    # Example of processing without a specific configuration
    result_no_config = process_data(["simple_item"])
    print(f"Processing with no config. Result: {result_no_config}")

except ValueError as e:
    # This error is raised if the input data list is empty.
    print(f"Error during processing: {e}")
except Exception as e:
    # Catch other potential errors
    print(f"An unexpected error occurred: {e}")

```
As the `process_data` function is developed, this section will be updated with more specific examples reflecting its actual capabilities (e.g., feature extraction, format conversion, etc.).

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development workflow management. Hatch will automatically use `uv` for faster environment and dependency management if `uv` is installed and available in your PATH. It's highly recommended to install `uv`.

### Prerequisites

- Python 3.10+
- [Git](https://git-scm.com/)
- [Hatch](https://hatch.pypa.io/latest/install/)
- (Recommended) [uv](https://github.com/astral-sh/uv#installation)

### Setup Development Environment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/twardoch/twat-speech.git
    cd twat-speech
    ```

2.  **Install Hatch (if not already installed):**
    ```bash
    pip install hatch
    # Or using uv
    uv pip install hatch
    ```

3.  **Install `uv` (recommended for faster performance):**
    Follow the installation instructions at [astral.sh/uv#installation](https://astral.sh/uv#installation).
    For example:
    ```bash
    # On macOS and Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    Verify installation:
    ```bash
    uv --version
    ```

4.  **Activate the Hatch environment:**
    Hatch will create and manage a virtual environment for the project.
    ```bash
    hatch shell
    ```
    This command automatically installs all dependencies defined in `pyproject.toml`. If `uv` is available, Hatch will use it, significantly speeding up this process.

5.  **Install pre-commit hooks:**
    This project uses pre-commit hooks to ensure code quality before committing.
    ```bash
    pre-commit install
    ```

### Common Development Tasks

All commands should be run from within the activated Hatch environment (`hatch shell`).

-   **Run tests:**
    ```bash
    hatch run test
    ```
    This executes the test suite using `pytest`.

-   **Run tests with coverage:**
    ```bash
    hatch run test-cov
    ```
    This generates a coverage report.

-   **Run linters and formatters:**
    Ruff is used for both linting and formatting.
    ```bash
    # Check for linting issues and formatting (does not modify files)
    hatch run lint:style
    # Format code and fix linting issues automatically
    hatch run lint:fmt
    ```

-   **Run static type checking:**
    ```bash
    hatch run lint:typing
    # Or directly
    # mypy src/twat_speech tests
    ```

-   **Build the package:**
    ```bash
    hatch build
    ```
    This will create wheel and sdist packages in the `dist/` directory.

### Codebase Structure

```
.
├── .github/                # GitHub Actions workflows
├── .vscode/                # VSCode settings (optional)
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

### Contribution Guidelines

We welcome contributions! Please follow these guidelines:

1.  **Branching:** Create a new branch for each feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/issue-number`.
2.  **Coding Standards:**
    *   Follow PEP 8 guidelines.
    *   Code is formatted and linted using Ruff. Ensure `hatch run lint:fmt` passes.
    *   Code is type-checked using Mypy. Ensure `hatch run lint:typing` passes.
    *   Write clear, concise, and well-commented code where necessary.
3.  **Testing:**
    *   Write tests for new features and bug fixes.
    *   Ensure all tests pass (`hatch run test`).
    *   Aim for high test coverage.
4.  **Commit Messages:**
    *   Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
    *   Example: `feat: add user authentication` or `fix: resolve issue with data parsing`.
5.  **Pull Requests (PRs):**
    *   Submit PRs to the `main` branch.
    *   Provide a clear description of the changes in your PR.
    *   Ensure all CI checks pass.
    *   Link to any relevant issues.
6.  **Versioning and Releases:**
    *   This project uses semantic versioning (SemVer) based on Git tags, managed by `hatch-vcs`.
    *   Releases are automated via GitHub Actions when a new tag (e.g., `v0.1.0`) is pushed.
    *   Maintainers will handle the tagging and release process.

## License

MIT License
```
