# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Definition of fixtures used by more than one file."""

import typing

import pytest


@pytest.fixture
def has_package() -> typing.Callable[[str], bool]:
    """Return if package is installed."""
    def _(package: str) -> bool:
        try:
            __import__(package)
        except ImportError:
            return False
        else:
            return True
    return _
