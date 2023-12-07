# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a consistency check between FEniCS/FEniCSx debian packages and local environment.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Test patches."""

import sys
import typing

import pytest

from virtualenv_class import VirtualEnv  # isort: skip


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


@pytest.mark.parametrize("backend,extra_packages,extra_packages_install,extra_packages_uninstall", [
    (
        "dolfin",
        ["ufl_legacy"],
        ["fenics-ufl-legacy@git+https://github.com/FEniCS/ufl-legacy.git@2022.3.0"],
        ["fenics-ufl-legacy"]
    ),
    (
        "dolfin",
        ["ufl"],
        ["fenics-ufl@git+https://github.com/FEniCS/ufl.git@2023.2.0"],
        ["fenics-ufl"]
    ),
    (
        "dolfin",
        ["FIAT", "ufl_legacy"],
        [
            "fenics-fiat@git+https://github.com/FEniCS/fiat.git",
            "fenics-ufl-legacy@git+https://github.com/FEniCS/ufl-legacy.git@2022.3.0"
        ],
        ["fenics-fiat", "fenics-ufl-legacy"]
    ),
    (
        "dolfin",
        ["ufl", "ufl_legacy"],
        [
            "fenics-ufl@git+https://github.com/FEniCS/ufl.git@2023.2.0",
            "fenics-ufl-legacy@git+https://github.com/FEniCS/ufl-legacy.git@2022.3.0"
        ],
        ["fenics-ufl", "fenics-ufl-legacy"]
    ),
    (
        "dolfinx",
        ["ufl"],
        ["fenics-ufl@git+https://github.com/FEniCS/ufl.git@2023.2.0"],
        ["fenics-ufl"]
    )
])
def test_backend_import_errors_with_local_packages(
    virtual_env: VirtualEnv, has_package: typing.Callable[[str, str], bool],
    get_package_main_file: typing.Callable[[str, str], str],
    backend: str, extra_packages: str, extra_packages_install: str, extra_packages_uninstall: str
) -> None:
    """Test that the backend fails to import with extra local packages."""
    if has_package(sys.executable, backend):
        for (extra_package, extra_package_install, extra_package_uninstall) in zip(
            extra_packages, extra_packages_install, extra_packages_uninstall
        ):
            virtual_env.install_package(extra_package_install)
            assert has_package(virtual_env.executable, extra_package)
            assert get_package_main_file(virtual_env.executable, extra_package).startswith(virtual_env.sys_path)
        assert not has_package(virtual_env.executable, backend)
        with pytest.raises(ImportError) as excinfo:
            get_package_main_file(virtual_env.executable, backend)
        import_error_text = str(excinfo.value)
        print(f"The following ImportError was raised:\n{import_error_text}")
        assert f"The following {backend} dependencies were imported from a local path" in import_error_text
        for (extra_package, extra_package_install, extra_package_uninstall) in zip(
            extra_packages, extra_packages_install, extra_packages_uninstall
        ):
            assert f"* {extra_package}: expected in" in import_error_text
            assert f"* run 'pip uninstall {extra_package_uninstall}' in a terminal" in import_error_text
    else:
        pytest.skip(f"{backend} not available")
