# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a consistency check between FEniCS/FEniCSx debian packages and local environment.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test patches."""

import typing

import pytest

from utils import (  # isort: skip
    assert_backend_import_errors_with_broken_packages, assert_backend_import_errors_with_local_packages,
    assert_backend_import_success_without_local_packages
)

UFL_LEGACY_WARNING = "legacy dolfin codes must now import ufl_legacy instead of ufl"


def test_dolfin_import_success_without_local_packages() -> None:
    """Test that the dolfin imports correctly without any extra local packages."""
    assert_backend_import_success_without_local_packages("dolfin")


@pytest.mark.parametrize("dependencies_import_name,dependencies_pypi_name,dependencies_extra_error_message", [
    (["ufl_legacy"], ["fenics-ufl-legacy"], []),
    (["ufl"], ["fenics-ufl"], [UFL_LEGACY_WARNING]),
    (["FIAT", "ufl_legacy"], ["fenics-fiat", "fenics-ufl-legacy"], []),
    (["ufl", "ufl_legacy"], ["fenics-ufl", "fenics-ufl-legacy"], [])
])
def test_dolfin_import_errors_with_local_packages(
    dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Test that the backend fails to import with extra local packages."""
    assert_backend_import_errors_with_local_packages(
        "dolfin", dependencies_import_name, dependencies_pypi_name, dependencies_extra_error_message
    )


@pytest.mark.parametrize("dependencies_import_name,dependencies_apt_name", [
    # (["ufl_legacy"], ["python3-ufl-legacy"]),  # cannot use this: it breaks ffc/compiler.py, line 121
    (["ffc"], ["python3-ffc"]),
])
def test_dolfin_import_errors_with_broken_packages(
    dependencies_import_name: typing.List[str], dependencies_apt_name: typing.List[str],
) -> None:
    """Test that the backend fails to import with broken local packages."""
    assert_backend_import_errors_with_broken_packages("dolfin", dependencies_import_name, dependencies_apt_name)
