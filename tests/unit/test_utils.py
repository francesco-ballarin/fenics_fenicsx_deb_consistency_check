# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Test utility functions defined in pusimp.utils."""

import sys
import typing

import pytest

from pusimp.utils import (
    assert_package_import_error, assert_package_import_errors_with_local_packages, assert_package_location,
    get_package_main_file, has_package, VirtualEnv)


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
    with VirtualEnv() as virtual_env:
        assert virtual_env.path.exists()


def test_install_package_in_virtual_env() -> None:
    """Test that installation in a virtual environment is successful."""
    with VirtualEnv() as virtual_env:
        virtual_env.install_package("my-empty-package")
        assert_package_location(
            virtual_env.executable, "my_empty_package", str(virtual_env.dist_path / "my_empty_package" / "__init__.py")
        )
        assert_package_import_error(
            sys.executable, "my_empty_package", ["No module named 'my_empty_package'"]
        )


def test_break_package_in_virtual_env() -> None:
    """Test breaking an existing package by a mock installation in a virtual environment."""
    with VirtualEnv() as virtual_env:
        virtual_env.break_package("pytest")
        assert_package_import_error(virtual_env.executable, "pytest", ["pytest was purposely broken."])
        assert_package_location(sys.executable, "pytest", pytest.__file__)


def generate_test_data_pypi_names(import_names: typing.List[str]) -> typing.List[str]:
    """Replace underscore with dash in import names, and add the git URL of the GitHub repo."""
    return [
        (
            f"'{import_name.replace('_', '-')} @ git+https://github.com/python-pusimp/pusimp.git@main"
            f"#subdirectory=tests/data/{import_name}'"
        ) for import_name in import_names
    ]


@pytest.mark.parametrize(
    "package_name,dependencies_import_name,dependencies_extra_error_message",
    [
        ("pusimp_package_one", ["pusimp_dependency_two"], ["pusimp_dependency_two is mandatory."]),
        ("pusimp_package_two", ["pusimp_dependency_two"], ["pusimp_dependency_two is mandatory."]),
        ("pusimp_package_two", ["pusimp_dependency_three"], ["pusimp_dependency_three is optional."]),
        (
            "pusimp_package_two", ["pusimp_dependency_two", "pusimp_dependency_three"],
            ["pusimp_dependency_two is mandatory.", "pusimp_dependency_three is optional."]
        ),
        ("pusimp_package_three", ["pusimp_dependency_two"], ["pusimp_dependency_two is mandatory."]),
        ("pusimp_package_three", ["pusimp_dependency_three"], ["pusimp_dependency_three is optional."]),
        (
            "pusimp_package_three", ["pusimp_dependency_two", "pusimp_dependency_three"],
            ["pusimp_dependency_two is mandatory.", "pusimp_dependency_three is optional."]
        ),
    ]
)
def test_assert_package_import_errors_with_local_packages_data_one_two_three(
    package_name: str, dependencies_import_name: typing.List[str], dependencies_extra_error_message: typing.List[str]
) -> None:
    """Test that assert_package_import_errors_with_local_packages on the first three mock package in tests/data."""
    assert_package_import_errors_with_local_packages(
        package_name, dependencies_import_name, generate_test_data_pypi_names(dependencies_import_name),
        dependencies_extra_error_message
    )
