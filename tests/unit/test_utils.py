# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Test utility functions defined in pusimp.utils."""

import sys

import pytest

from pusimp.utils import (
    assert_package_import_error, assert_package_location, get_package_main_file, has_package, VirtualEnv)


def test_has_package() -> None:
    """Test has_package with a package that is surely installed."""
    assert has_package(sys.executable, "pytest", True)


def test_get_package_main_file() -> None:
    """Test get_package_main_file with a package that is surely installed."""
    assert get_package_main_file(sys.executable, "pytest") == pytest.__file__


def test_assert_package_location() -> None:
    """Test assert_package_location with a package that is surely installed."""
    assert_package_location(sys.executable, "pytest", pytest.__file__)


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
    """Test breaking an existing package by a mock installation in a virtual environment."""
    virtual_env = VirtualEnv()
    virtual_env.break_package("pytest")
    assert_package_import_error(virtual_env.executable, "pytest", ["pytest was purposely broken."])
    assert_package_location(sys.executable, "pytest", pytest.__file__)
