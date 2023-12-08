# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Test that all mock packages in tests/data import correctly after installation.

It is preferable not to run this file together with tests/unit, since the mock packages should
be re-imported from scratch while carrying out unit tests.
"""

def test_data_one() -> None:
    """Test that the first mock package in tests/data import correctly after installation."""
    import pusimp_package_one  # noqa: F401


def test_data_two() -> None:
    """Test that the second mock package in tests/data import correctly after installation."""
    import pusimp_package_two  # noqa: F401


def test_data_three() -> None:
    """Test that the third mock package in tests/data import correctly after installation."""
    import pusimp_package_three  # noqa: F401
