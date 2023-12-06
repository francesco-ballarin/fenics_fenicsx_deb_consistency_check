# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Definition of fixtures used by more than one file."""

import subprocess
import tempfile
import typing

import pytest

from virtualenv_class import VirtualEnv  # isort: skip


@pytest.fixture
def has_package() -> typing.Callable[[str, str], bool]:
    """Return if package is installed.

    Note that it is not safe to simply import the package in the current pytest environment,
    since the environment itself might change from one test to the other, but python packages
    can be imported only once and not unloaded.
    """
    def _(executable: str, package: str) -> bool:
        run_import = subprocess.run(f"{executable} -c 'import {package}'", shell=True, capture_output=True)
        if run_import.returncode == 0:
            return True
        else:
            """
            print(f"Importing {package} failed.\n"
                  f"stdout contains {run_import.stdout.decode().strip()}\n"
                  f"stderr contains {run_import.stderr.decode().strip()}\n")
            """
            return False
    return _


@pytest.fixture
def get_package_main_file() -> typing.Callable[[str, str], str]:
    """Get the path of the package main file."""
    def _(executable: str, package: str) -> str:
        run_import_file = subprocess.run(
            f"{executable} -c 'import {package}; print({package}.__file__)'", shell=True, capture_output=True)
        if run_import_file.returncode == 0:
            return run_import_file.stdout.decode().strip()
        else:
            raise ImportError(
                f"Importing {package} failed.\n"
                f"stdout contains {run_import_file.stdout.decode().strip()}\n"
                f"stderr contains {run_import_file.stderr.decode().strip()}\n")
    return _


@pytest.fixture
def virtual_env() -> VirtualEnv:
    """Generate a temporary virtual environment."""
    virtual_env_ = VirtualEnv(tempfile.mkdtemp())
    virtual_env_.create()
    return virtual_env_
