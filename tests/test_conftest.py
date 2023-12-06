# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test fixtures defined in conftest."""

import os
import sys
import typing

import pytest

from virtualenv_class import VirtualEnv  # isort: skip


def test_has_numpy(has_package: typing.Callable[[str, str], bool]) -> None:
    """Test has_package fixture with a package (numpy) that is surely installed."""
    assert has_package(sys.executable, "numpy")


@pytest.mark.parametrize("backend", ["dolfin", "dolfinx"])
def test_has_backend(has_package: typing.Callable[[str, str], bool], backend: str) -> None:
    """Test has_package fixture with a backend (FEniCS or FEniCSx) that may or may not be installed."""
    pytest.importorskip(backend)
    # If pytest did not skip this test, then it means that the backend was installed
    # and the call below must return True
    assert has_package(sys.executable, backend)


@pytest.mark.parametrize("backend,enviornment_variable", [("dolfin", "HAS_FENICS"), ("dolfinx", "HAS_FENICSX")])
def test_backend_enviornment_variable(
    has_package: typing.Callable[[str, str], bool], backend: str, enviornment_variable: str
) -> None:
    """Test consistency between the result of the has_package fixture and the environment variables set on CI."""
    enviornment_variable_value = os.getenv(enviornment_variable)
    if enviornment_variable_value is not None:  # the environment variable was not exported
        assert enviornment_variable_value in ("true", "false")
        if has_package(sys.executable, backend):
            assert enviornment_variable_value == "true"
        else:
            assert enviornment_variable_value == "false"
    else:
        pytest.skip(f"Missing environment variable {enviornment_variable}")


def test_get_numpy_main_file(get_package_main_file: typing.Callable[[str, str], str]) -> None:
    """Test get_package_main_file fixture with a package (numpy) that is surely installed."""
    assert get_package_main_file(sys.executable, "numpy") == "/usr/lib/python3/dist-packages/numpy/__init__.py"


def test_virtual_env(virtual_env: VirtualEnv) -> None:
    """Test that the creation of a virtual environment is successful."""
    assert virtual_env.path.exists()


def test_install_in_virtual_env(
    virtual_env: VirtualEnv, has_package: typing.Callable[[str, str], bool],
    get_package_main_file: typing.Callable[[str, str], str]
) -> None:
    """Test that installation in a virtual environment is successful."""
    virtual_env.install_package("my-empty-package")
    assert has_package(virtual_env.executable, "my_empty_package")
    assert not has_package(sys.executable, "my_empty_package")
    module_file = get_package_main_file(virtual_env.executable, "my_empty_package")
    assert module_file.startswith(virtual_env.sys_path)
