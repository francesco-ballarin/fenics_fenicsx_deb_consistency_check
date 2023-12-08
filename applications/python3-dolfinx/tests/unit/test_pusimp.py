# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp for FEniCSx.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test DOLFINx patches."""

import typing

import pytest

from pusimp.utils import (  # isort: skip
    assert_package_import_errors_with_local_packages,
    assert_package_import_errors_with_broken_non_optional_packages,
    assert_package_import_success_with_allowed_local_packages,
    assert_package_import_success_without_local_packages
)


def test_dolfinx_import_success_without_local_packages() -> None:
    """Test that dolfinx imports correctly without any extra local packages."""
    assert_package_import_success_without_local_packages(
        "dolfinx", "/usr/lib/petsc/lib/python3/dist-packages/dolfinx/__init__.py")


@pytest.mark.parametrize("dependencies_import_name,dependencies_pypi_name,dependencies_extra_error_message", [
    (["ufl"], ["fenics-ufl"], []),
    (["ffcx", "ufl"], ["fenics-ffcx", "fenics-ufl"], [])
])
def test_dolfinx_import_errors_with_local_packages(
    dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Test that dolfinx fails to import with extra local packages."""
    assert_package_import_errors_with_local_packages(
        "dolfinx", dependencies_import_name, dependencies_pypi_name, dependencies_extra_error_message)



@pytest.mark.parametrize("dependencies_import_name,dependencies_pypi_name", [
    (["ufl"], ["fenics-ufl"])
])
def test_dolfinx_import_success_with_allowed_local_packages(
    dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str]
) -> None:
    """Test that dolfinx imports correctly even with extra local packages when asked to allow user-site imports."""
    assert_package_import_success_with_allowed_local_packages(
        "dolfinx", "/usr/lib/petsc/lib/python3/dist-packages/dolfinx/__init__.py",
        dependencies_import_name, dependencies_pypi_name)


@pytest.mark.parametrize("dependencies_import_name", [
    ["ufl"],
    ["ffcx"]
])
def test_dolfinx_import_errors_with_broken_non_optional_packages(dependencies_import_name: typing.List[str]) -> None:
    """Test that dolfinx fails to import with broken local packages."""
    assert_package_import_errors_with_broken_non_optional_packages("dolfinx", dependencies_import_name)
