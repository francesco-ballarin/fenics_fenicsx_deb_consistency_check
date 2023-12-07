# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a consistency check between FEniCS/FEniCSx debian packages and local environment.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Definition of fixtures used by more than one file."""


import os
import pathlib
import subprocess
import sys
import tempfile
import typing

import pytest
import virtualenv


def has_package(executable: str, package: str) -> bool:
    """Return if package is installed.

    Note that it is not safe to simply import the package in the current pytest environment,
    since the environment itself might change from one test to the other, but python packages
    can be imported only once and not unloaded.
    """
    run_import = subprocess.run(f"{executable} -c 'import {package}'", shell=True, capture_output=True)
    if run_import.returncode == 0:
        return True
    else:
        """
        print(f"Importing {package} was not successful.\n"
              f"stdout contains {run_import.stdout.decode().strip()}\n"
              f"stderr contains {run_import.stderr.decode().strip()}\n")
        """
        return False


def get_package_main_file(executable: str, package: str) -> str:
    """Get the path of the package main file."""
    run_import_file = subprocess.run(
        f"{executable} -c 'import {package}; print({package}.__file__)'", shell=True, capture_output=True)
    if run_import_file.returncode == 0:
        return run_import_file.stdout.decode().strip()
    else:
        raise ImportError(
            f"Importing {package} was not successful.\n"
            f"stdout contains {run_import_file.stdout.decode().strip()}\n"
            f"stderr contains {run_import_file.stderr.decode().strip()}\n")


def assert_package_location(executable: str, package: str, path: str) -> None:
    """Assert that a package imports from the expected location."""
    assert has_package(executable, package)
    assert get_package_main_file(executable, package) == path


def assert_package_import_error(executable: str, package: str, expected: typing.List[str]) -> None:
    """Assert that a package fails to imports with the expected text in the ImportError message."""
    assert not has_package(executable, package)
    with pytest.raises(ImportError) as excinfo:
        get_package_main_file(executable, package)
    import_error_text = str(excinfo.value)
    print(f"The following ImportError was raised:\n{import_error_text}")
    for expected_ in expected:
        assert expected_ in import_error_text, (
            f"{expected_} was not found in the ImportError text, namely {import_error_text}"
        )


def assert_backend_import_success_without_local_packages(backend: str) -> None:
    """Assert that the backend imports correctly without any extra local packages."""
    assert_package_location(sys.executable, backend, f"/usr/lib/petsc/lib/python3/dist-packages/{backend}/__init__.py")


def assert_backend_import_errors_with_local_packages(
    backend: str, dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Assert that the backend fails to import with extra local packages."""
    virtual_env = VirtualEnv()
    for (dependency_import_name, dependency_pypi_name) in zip(dependencies_import_name, dependencies_pypi_name):
        virtual_env.install_package(dependency_pypi_name)
        assert_package_location(
            virtual_env.executable, dependency_import_name,
            str(virtual_env.dist_path / dependency_import_name / "__init__.py")
        )
    dependencies_error_messages = ["dependencies were imported from a local path"]
    dependencies_error_messages.extend(
        f"* {dependency_import_name}: expected in" for dependency_import_name in dependencies_import_name
    )
    dependencies_error_messages.extend(
        f"* run 'pip uninstall {dependency_pypi_name}' in" for dependency_pypi_name in dependencies_pypi_name
    )
    dependencies_error_messages.extend(dependencies_extra_error_message)
    assert_package_import_error(virtual_env.executable, backend, dependencies_error_messages)


def assert_backend_import_errors_with_broken_packages(
    backend: str, dependencies_import_name: typing.List[str], dependencies_apt_name: typing.List[str],
) -> None:
    """Assert that the backend imports correctly when optional packages are broken."""
    virtual_env = VirtualEnv()
    for dependency_import_name in dependencies_import_name:
        virtual_env.break_package(dependency_import_name)
        assert_package_import_error(
            virtual_env.executable, dependency_import_name, [f"{dependency_import_name} was purposely broken."]
        )
    dependencies_error_messages: typing.List[str] = []
    dependencies_error_messages.extend(
        f"{dependency_import_name} is missing or broken" for dependency_import_name in dependencies_import_name
    )
    dependencies_error_messages.extend(
        f"fix it with 'apt install --reinstall {dependency_apt_name}'" for dependency_apt_name in dependencies_apt_name
    )
    assert_package_import_error(virtual_env.executable, backend, dependencies_error_messages)


def assert_backend_import_success_with_optional_packages(
    backend: str, dependencies_import_name: typing.List[str], dependencies_pypi_name: typing.List[str]
) -> None:
    """Assert that the backend fails to import with extra local packages."""
    virtual_env = VirtualEnv()
    for (dependency_import_name, dependency_pypi_name) in zip(dependencies_import_name, dependencies_pypi_name):
        virtual_env.install_package(dependency_pypi_name)
        assert_package_location(
            virtual_env.executable, dependency_import_name,
            str(virtual_env.dist_path / dependency_import_name / "__init__.py")
        )
    assert_package_location(
        virtual_env.executable, backend, f"/usr/lib/petsc/lib/python3/dist-packages/{backend}/__init__.py"
    )


class VirtualEnv(object):
    """Helper class to create a temporary virtual environment.

    Forked and simplified from https://github.com/pyscaffold/pyscaffold/blob/master/tests/virtualenv.py .
    """

    def __init__(self) -> None:
        self.path = pathlib.Path(tempfile.mkdtemp()) / "venv"
        self.dist_path = (
            self.path / "lib" / ("python" + str(sys.version_info.major) + "." + str(sys.version_info.minor))
            / "site-packages"
        )
        self.executable = str(self.path / "bin" / "python3")
        self.env = dict(os.environ)
        self.env.pop("PYTHONPATH", None)  # ensure isolation
        self.create()

    def create(self) -> None:
        """Create a virtual environment, and add it to sys.path."""
        args = [str(self.path), "--python", sys.executable, "--system-site-packages", "--no-wheel"]
        virtualenv.cli_run(args, env=self.env)

    def install_package(self, package: str) -> None:
        """Install a package in the virtual environment."""
        run_install = subprocess.run(
            f"{self.executable} -m pip install --ignore-installed --break-system-packages {package}",
            shell=True, capture_output=True)
        if run_install.returncode != 0:
            raise RuntimeError(
                f"Installing {package} was not successful.\n"
                f"stdout contains {run_install.stdout.decode()}\n"
                f"stderr contains {run_install.stderr.decode()}\n")

    def break_package(self, package: str) -> None:
        """Install a mock package in the virtual environment which errors out."""
        (self.dist_path / package).mkdir()
        with (self.dist_path / package / "__init__.py").open("w") as init_file:
            init_file.write(f"raise ImportError('{package} was purposely broken.')")
