# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test proposed patches."""

import sys
import typing

import pytest

# from virtualenv_class import VirtualEnv  # isort: skip


@pytest.mark.parametrize("backend", ["dolfin", "dolfinx"])
def test_backend_imports_without_local_packages(
    has_package: typing.Callable[[str, str], bool], get_package_main_file: typing.Callable[[str, str], str],
    backend: str
) -> None:
    """Test that the backend imports correctly without any extra local packages.

    Note that the call to has_package(backend) could in principle return False if the package is installed,
    but the import fails.
    However, with test_backend_enviornment_variable in test_conftest we verify that this is never the case.
    """
    if has_package(sys.executable, backend):
        assert get_package_main_file(sys.executable, backend) == (
            f"/usr/lib/petsc/lib/python3/dist-packages/{backend}/__init__.py")
    else:
        pytest.skip(f"{backend} not available")
