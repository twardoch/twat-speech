# SPDX-FileCopyrightText: 2024-present Adam Twardoch <adam+github@twardoch.com>
#
# SPDX-License-Identifier: MIT
"""
twat-speech package.
"""
try:
    from .__version__ import __version__
except ImportError:
    # Fallback version if the package is not installed and __version__.py is not generated
    # This is useful for local development before the first build with hatch-vcs
    __version__ = "0.0.0.dev0"

from .twat_speech import Config, process_data

__all__ = ["__version__", "Config", "process_data"]
