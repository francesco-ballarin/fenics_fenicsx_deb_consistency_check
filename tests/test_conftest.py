# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test fixtures defined in conftest."""

import os
import typing

import pytest


def test_has_numpy(has_package: typing.Callable[[str], bool]) -> None:
    """Test has_package fixture with a package that is surely installed."""
    assert has_package("numpy")


@pytest.mark.parametrize("backend", ["dolfin", "dolfinx"])
def test_has_backend(has_package: typing.Callable[[str], bool], backend: str) -> None:
    """Test has_package fixture with a backend (FEniCS or FEniCSx) that may or may not be installed."""
    pytest.importorskip(backend)
    # If pytest did not skip this test, then it means that the backend was installed
    # and the call below must return True
    assert has_package(backend)


@pytest.mark.parametrize("backend,enviornment_variable", [("dolfin", "HAS_FENICS"), ("dolfinx", "HAS_FENICSX")])
def test_backend_enviornment_variable(
    has_package: typing.Callable[[str], bool], backend: str, enviornment_variable: str
) -> None:
    """Test consistency between the result of the has_package fixture and the environment variables set on CI."""
    enviornment_variable_value = os.getenv(enviornment_variable)
    assert enviornment_variable_value in ("true", "false")
    if has_package(backend):
        assert enviornment_variable_value == "true"
    else:
        assert enviornment_variable_value == "false"
