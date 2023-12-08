# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp for FEniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test DOLFIN patches."""

import typing

import pytest

from pusimp.utils import (  # isort: skip
    assert_package_import_errors_with_local_packages,
    assert_package_import_errors_with_broken_non_optional_packages,
    assert_package_import_success_with_allowed_local_packages,
    assert_package_import_success_with_broken_optional_packages,
    assert_package_import_success_without_local_packages
)

UFL_LEGACY_WARNING = "legacy dolfin codes must now import ufl_legacy instead of ufl"


def test_dolfin_import_success_without_local_packages() -> None:
    """Test that dolfin imports correctly without any extra local packages."""
    assert_package_import_success_without_local_packages(
        "dolfin", "/usr/lib/petsc/lib/python3/dist-packages/dolfin/__init__.py")


@pytest.mark.parametrize("dependencies_import_name,dependencies_pypi_name,dependencies_extra_error_message", [
    (["ufl_legacy"], ["fenics-ufl-legacy"], []),
    (["ufl"], ["fenics-ufl"], [UFL_LEGACY_WARNING]),
    (["FIAT", "ufl_legacy"], ["fenics-fiat", "fenics-ufl-legacy"], []),
    (["ufl", "ufl_legacy"], ["fenics-ufl", "fenics-ufl-legacy"], [UFL_LEGACY_WARNING])
])
def test_dolfin_import_errors_with_local_packages(
    dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Test that dolfin fails to import with extra local packages."""
    assert_package_import_errors_with_local_packages(
        "dolfin", dependencies_import_name, dependencies_pypi_name, dependencies_extra_error_message)


@pytest.mark.parametrize("dependencies_import_name,dependencies_pypi_name", [
    (["ufl_legacy"], ["fenics-ufl-legacy"]),
    (["ufl"], ["fenics-ufl"])
])
def test_dolfin_import_success_with_allowed_local_packages(
    dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str]
) -> None:
    """Test that dolfin imports correctly even with extra local packages when asked to allow user-site imports."""
    assert_package_import_success_with_allowed_local_packages(
        "dolfin", "/usr/lib/petsc/lib/python3/dist-packages/dolfin/__init__.py",
        dependencies_import_name, dependencies_pypi_name)


@pytest.mark.parametrize("dependencies_import_name", [
    # ["ufl_legacy"],  # cannot use this: it breaks ffc/compiler.py (line 121) too
    ["ffc"]
])
def test_dolfin_import_errors_with_broken_non_optional_packages(dependencies_import_name: typing.List[str]) -> None:
    """Test that dolfin fails to import when non-optional packages are broken."""
    assert_package_import_errors_with_broken_non_optional_packages("dolfin", dependencies_import_name)


@pytest.mark.parametrize("dependencies_import_name", [
    ["ufl"]
])
def test_dolfin_import_success_with_broken_optional_packages(dependencies_import_name: typing.List[str]) -> None:
    """Test that dolfin fails to import imports correctly when optional packages are broken."""
    assert_package_import_success_with_broken_optional_packages(
        "dolfin", "/usr/lib/petsc/lib/python3/dist-packages/dolfin/__init__.py", dependencies_import_name)
