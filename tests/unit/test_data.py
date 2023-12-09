# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Test imports of mock packages in tests/data."""

import os

import pytest

import pusimp_golden_source  # isort: skip


def test_data_one() -> None:
    """Test that the first mock package in tests/data import correctly."""
    import pusimp_package_one  # noqa: F401


def test_data_two() -> None:
    """Test that the second mock package in tests/data import correctly."""
    import pusimp_package_two  # noqa: F401


def test_data_three() -> None:
    """Test that the third mock package in tests/data import correctly."""
    import pusimp_package_three  # noqa: F401


def test_data_four() -> None:
    """Test that the fourth mock package in tests/data fails to import due to a missing mandatory dependency."""
    with pytest.raises(ImportError) as excinfo:
        import pusimp_package_four  # noqa: F401
    import_error_text = str(excinfo.value)
    assert import_error_text == (
        "pusimp_dependency_missing is missing. Its expected path was "
        f"{os.path.join(pusimp_golden_source.system_path, 'pusimp_dependency_missing', '__init__.py')}."
    )


def test_data_five() -> None:
    """Test that the fifth mock package in tests/data import correctly, because the missing dependency is optional."""
    import pusimp_package_five  # noqa: F401


def test_data_six() -> None:
    """Test that the sixth mock package in tests/data fails to import due to a broken mandatory dependency."""
    with pytest.raises(ImportError) as excinfo:
        import pusimp_package_six  # noqa: F401
    import_error_text = str(excinfo.value)
    assert import_error_text == (
        "pusimp_dependency_four is broken. Error on import was 'pusimp_dependency_four is a broken package.'."
    )


def test_data_seven() -> None:
    """Test that the seventh mock package in tests/data import correctly, because the broken dependency is optional."""
    import pusimp_package_seven  # noqa: F401
