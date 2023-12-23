# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Test utility functions defined in pusimp.utils."""

import importlib
import os
import sys
import typing

import pytest

from pusimp.utils import (
    assert_has_package, assert_not_has_package, assert_package_import_error,
    assert_package_import_errors_with_broken_non_optional_packages, assert_package_import_errors_with_local_packages,
    assert_package_import_success_with_allowed_local_packages,
    assert_package_import_success_with_broken_optional_packages, assert_package_import_success_without_local_packages,
    assert_package_location, VirtualEnv)

import pusimp_golden_source  # isort: skip


def test_assert_has_package_success() -> None:
    """Test that assert_has_package succeeds with a package that is surely installed."""
    assert_has_package(sys.executable, "pytest")


def test_assert_has_package_failure() -> None:
    """Test that assert_has_package fails with a package that is surely not installed."""
    with pytest.raises(AssertionError) as excinfo:
        assert_has_package(sys.executable, "not_existing_package")
    assertion_error_text = str(excinfo.value)
    assert assertion_error_text.startswith("Importing not_existing_package was not successful")


def test_assert_not_has_package_success() -> None:
    """Test that assert_not_has_package succeeds with a package that is surely not installed."""
    assert_not_has_package(sys.executable, "not_existing_package")


def test_assert_not_has_package_failure() -> None:
    """Test that assert_not_has_package fails with a package that is surely installed."""
    with pytest.raises(AssertionError) as excinfo:
        assert_not_has_package(sys.executable, "pytest")
    assertion_error_text = str(excinfo.value)
    assert assertion_error_text.startswith("Importing pytest was unexpectedly successful")


def test_assert_package_location() -> None:
    """Test assert_package_location with a package that is surely installed."""
    assert_package_location(sys.executable, "pytest", pytest.__file__)


def test_assert_package_import_error() -> None:
    """Test assert_package_import_error with a package that is surely not installed."""
    assert_package_import_error(
        sys.executable, "not_existing_package", ["No module named 'not_existing_package'"], [], False
    )


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
            sys.executable, "my_empty_package", ["No module named 'my_empty_package'"], [], False
        )


def test_break_package_in_virtual_env() -> None:
    """Test breaking an existing package by a mock installation in a virtual environment."""
    with VirtualEnv() as virtual_env:
        virtual_env.break_package("pytest")
        assert_package_import_error(virtual_env.executable, "pytest", ["pytest was purposely broken."], [], False)
        assert_package_location(sys.executable, "pytest", pytest.__file__)


def generate_test_data_pypi_names(import_names: typing.List[str]) -> typing.List[str]:
    """Replace underscore with dash in import names, and add the git URL of the GitHub repo."""
    pusimp_version = importlib.metadata.version("pusimp")
    if "dev" in pusimp_version:
        data_tag = "main"
    else:
        data_tag = f"v{pusimp_version}"
    return [
        (
            f"'{import_name.replace('_', '-')} @ git+https://github.com/python-pusimp/pusimp.git@{data_tag}"
            f"#subdirectory=tests/data/{import_name}'"
        ) for import_name in import_names
    ]


@pytest.mark.parametrize("package_name", ["pusimp_package_one", "pusimp_package_two", "pusimp_package_three"])
def test_assert_package_import_success_without_local_packages_data_one_two_three(package_name: str) -> None:
    """Test assert_package_import_success_without_local_packages on the first three mock packages."""
    assert_package_import_success_without_local_packages(
        package_name, os.path.join(pusimp_golden_source.system_path, package_name, "__init__.py")
    )


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
        )
    ]
)
def test_assert_package_import_errors_with_local_packages_data_one_two_three(
    package_name: str, dependencies_import_name: typing.List[str], dependencies_extra_error_message: typing.List[str]
) -> None:
    """Test assert_package_import_errors_with_local_packages on the first three mock packages."""
    assert_package_import_errors_with_local_packages(
        package_name, dependencies_import_name, generate_test_data_pypi_names(dependencies_import_name),
        dependencies_extra_error_message
    )


@pytest.mark.parametrize(
    "package_name,dependencies_import_name",
    [
        ("pusimp_package_one", ["pusimp_dependency_two"]),
        ("pusimp_package_two", ["pusimp_dependency_two"]),
        ("pusimp_package_two", ["pusimp_dependency_three"]),
        ("pusimp_package_two", ["pusimp_dependency_two", "pusimp_dependency_three"]),
        ("pusimp_package_three", ["pusimp_dependency_two"]),
        ("pusimp_package_three", ["pusimp_dependency_three"]),
        ("pusimp_package_three", ["pusimp_dependency_two", "pusimp_dependency_three"])
    ]
)
def test_assert_package_import_success_with_allowed_local_packages_data_one_two_three(
    package_name: str, dependencies_import_name: typing.List[str]
) -> None:
    """Test assert_package_import_success_with_allowed_local_packages on the first three mock packages."""
    assert_package_import_success_with_allowed_local_packages(
        package_name, os.path.join(pusimp_golden_source.system_path, package_name, "__init__.py"),
        dependencies_import_name, generate_test_data_pypi_names(dependencies_import_name)
    )


@pytest.mark.parametrize(
    "package_name,dependencies_import_name,dependencies_optional",
    [
        ("pusimp_package_three", ["pusimp_dependency_two"], [False]),
        ("pusimp_package_three", ["pusimp_dependency_two", "pusimp_dependency_three"], [False, True])
    ]
)
def test_assert_package_import_errors_with_broken_non_optional_packages_data_one_two_three_success(
    package_name: str, dependencies_import_name: typing.List[str], dependencies_optional: typing.List[bool]
) -> None:
    """Test success of assert_package_import_errors_with_broken_non_optional_packages on the first three mock packages.

    The successful cases are the cases in which dependencies_import_name lists actual mandatory dependencies,
    and the import of the broken dependency happens after the call to pusimp.prevent_user_site_imports.
    """
    assert_package_import_errors_with_broken_non_optional_packages(
        package_name, dependencies_import_name, dependencies_optional
    )


@pytest.mark.parametrize(
    "package_name,dependencies_import_name,dependencies_optional",
    [
        ("pusimp_package_one", ["pusimp_dependency_two"], [False]),
        ("pusimp_package_two", ["pusimp_dependency_two"], [False]),
        ("pusimp_package_two", ["pusimp_dependency_two", "pusimp_dependency_three"], [False, True])
    ]
)
def test_assert_package_import_errors_with_broken_non_optional_packages_data_one_two_three_failure_position(
    package_name: str, dependencies_import_name: typing.List[str], dependencies_optional: typing.List[bool]
) -> None:
    """Test failure of assert_package_import_errors_with_broken_non_optional_packages on the first three mock packages.

    These failing cases are the cases in which the import of the broken mandatory dependency listed
    in dependencies_import_name happens before the call to pusimp.prevent_user_site_imports.
    """
    with pytest.raises(AssertionError) as excinfo:
        assert_package_import_errors_with_broken_non_optional_packages(
            package_name, dependencies_import_name, dependencies_optional
        )
    assertion_error_text = str(excinfo.value)
    assert assertion_error_text.startswith(
        f"{dependencies_import_name[0]} is broken was not found in the ImportError text, namely "
        f"Importing {package_name} was not successful"
    )
    assert f"{dependencies_import_name[0]} was purposely broken" in assertion_error_text


@pytest.mark.parametrize(
    "package_name,dependencies_import_name,dependencies_optional",
    [
        ("pusimp_package_two", ["pusimp_dependency_three"], [True]),
        ("pusimp_package_three", ["pusimp_dependency_three"], [True])
    ]
)
def test_assert_package_import_errors_with_broken_non_optional_packages_data_one_two_three_failure_only_optional(
    package_name: str, dependencies_import_name: typing.List[str], dependencies_optional: typing.List[bool]
) -> None:
    """Test failure of assert_package_import_errors_with_broken_non_optional_packages on the first three mock packages.

    These failing cases are the cases in which only optional dependencies have been listed in dependencies_import_name.
    """
    with pytest.raises(AssertionError) as excinfo:
        assert_package_import_errors_with_broken_non_optional_packages(
            package_name, dependencies_import_name, dependencies_optional
        )
    assertion_error_text = str(excinfo.value)
    assert f"Importing {package_name} was unexpectedly successful" in assertion_error_text


@pytest.mark.parametrize(
    "package_name,dependencies_import_name,dependencies_optional",
    [
        ("pusimp_package_one", ["pusimp_dependency_two"], [False]),
        ("pusimp_package_two", ["pusimp_dependency_two"], [False]),
        ("pusimp_package_two", ["pusimp_dependency_three"], [True]),
        ("pusimp_package_two", ["pusimp_dependency_two", "pusimp_dependency_three"], [False, True]),
        ("pusimp_package_three", ["pusimp_dependency_two"], [False]),
        ("pusimp_package_three", ["pusimp_dependency_three"], [True]),
        ("pusimp_package_three", ["pusimp_dependency_two", "pusimp_dependency_three"], [False, True])
    ]
)
def test_assert_package_import_success_with_broken_optional_packages_data_one_two_three(
    package_name: str, dependencies_import_name: typing.List[str], dependencies_optional: typing.List[bool]
) -> None:
    """Test success of assert_package_import_success_with_broken_optional_packages on the first three mock packages.

    The successful cases are the cases in which dependencies_import_name lists actual optional dependencies.
    """
    assert_package_import_success_with_broken_optional_packages(
        package_name, os.path.join(pusimp_golden_source.system_path, package_name, "__init__.py"),
        dependencies_import_name, dependencies_optional
    )
