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


def test_dolfinx_import_success_without_local_packages() -> None:
    """Test that the dolfinx imports correctly without any extra local packages."""
    assert_backend_import_success_without_local_packages("dolfinx")


@pytest.mark.parametrize("dependencies_import_name,dependencies_pypi_name,dependencies_extra_error_message", [
    (["ufl"], ["fenics-ufl"], []),
    (["ffcx", "ufl"], ["fenics-ffcx", "fenics-ufl"], []),
])
def test_dolfinx_import_errors_with_local_packages(
    dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Test that the backend fails to import with extra local packages."""
    assert_backend_import_errors_with_local_packages(
        "dolfinx", dependencies_import_name, dependencies_pypi_name, dependencies_extra_error_message
    )


@pytest.mark.parametrize("dependencies_import_name,dependencies_apt_name", [
    (["ufl"], ["python3-ufl"]),
    (["ffcx"], ["python3-ffcx"]),
])
def test_dolfinx_import_errors_with_broken_packages(
    dependencies_import_name: typing.List[str], dependencies_apt_name: typing.List[str],
) -> None:
    """Test that the backend fails to import with broken local packages."""
    assert_backend_import_errors_with_broken_packages("dolfinx", dependencies_import_name, dependencies_apt_name)
