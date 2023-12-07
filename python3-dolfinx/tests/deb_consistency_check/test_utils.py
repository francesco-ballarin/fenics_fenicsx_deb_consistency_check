# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a consistency check between FEniCS/FEniCSx debian packages and local environment.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test fixtures defined in conftest."""

import sys

from utils import VirtualEnv, assert_package_import_error, assert_package_location, get_package_main_file, has_package


def test_has_numpy() -> None:
    """Test has_package with a package that is surely installed."""
    assert has_package(sys.executable, "numpy")


def test_get_numpy_main_file() -> None:
    """Test get_package_main_file with a package that is surely installed."""
    assert get_package_main_file(sys.executable, "numpy") == "/usr/lib/python3/dist-packages/numpy/__init__.py"


def test_assert_numpy_location() -> None:
    """Test assert_package_location with a package that is surely installed."""
    assert_package_location(sys.executable, "numpy", "/usr/lib/python3/dist-packages/numpy/__init__.py")


def test_assert_package_import_error() -> None:
    """Test assert_package_import_error with a package that is surely not installed."""
    assert_package_import_error(sys.executable, "not_existing_package", ["No module named 'not_existing_package'"])


def test_virtual_env() -> None:
    """Test that the creation of a virtual environment is successful."""
    virtual_env = VirtualEnv()
    assert virtual_env.path.exists()


def test_install_package_in_virtual_env() -> None:
    """Test that installation in a virtual environment is successful."""
    virtual_env = VirtualEnv()
    virtual_env.install_package("my-empty-package")
    assert_package_location(
        virtual_env.executable, "my_empty_package", str(virtual_env.dist_path / "my_empty_package" / "__init__.py")
    )
    assert_package_import_error(
        sys.executable, "my_empty_package", ["No module named 'my_empty_package'"]
    )


def test_break_package_in_virtual_env() -> None:
    """Test breaking a system wide package by a mock installation in a virtual environment."""
    virtual_env = VirtualEnv()
    virtual_env.break_package("numpy")
    assert_package_import_error(virtual_env.executable, "numpy", ["numpy was purposely broken."])
    assert_package_location(sys.executable, "numpy", "/usr/lib/python3/dist-packages/numpy/__init__.py")
