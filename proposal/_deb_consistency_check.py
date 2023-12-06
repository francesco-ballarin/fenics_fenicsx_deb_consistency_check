# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Checks that FEniCS/FEniCSx components are not being imported from non-system wide locations."""

import os

FENICS_SKIP_DEB_CONSISTENCY_CHECK = os.getenv("FENICS_SKIP_DEB_CONSISTENCY_CHECK") is not None

if not FENICS_SKIP_DEB_CONSISTENCY_CHECK:
    CONTACT_ON_ERROR = "Please report this error on https://fenicsproject.discourse.group/ ."

    system_install_path = os.path.dirname(os.path.dirname(__file__))
    assert system_install_path.startswith("/usr/lib"), (
        "Did something change in debian/ubuntu packaging for this path to change?\n"
        + f"Expected {system_install_path} to start with /usr/lib.\n\n"
        + CONTACT_ON_ERROR
    )

    backend_name = os.path.basename(os.path.dirname(__file__))
    assert backend_name in ("dolfin", "dolfinx"), (
        "Did something change in debian/ubuntu packaging for this assert to fail?\n"
        + f"Got unexpected value {backend_name}.\n\n"
        + CONTACT_ON_ERROR
    )

    if backend_name == "dolfin":
        backend_dependencies = {
            "dijitso": "/usr/lib/python3/dist-packages/dijitso/__init__.py",
            "ffc": "/usr/lib/python3/dist-packages/ffc/__init__.py",
            "FIAT": "/usr/lib/python3/dist-packages/FIAT/__init__.py",
            "ufl_legacy": "/usr/lib/python3/dist-packages/ufl_legacy/__init__.py"
        }
        # Add ufl too, if dolfin and dolfinx are installed simultaneously, since users
        # typically end up manually installing it because downstream dependencies have not updated yet
        # their codebase to use ufl_legacy instead of ufl
        try:
            __import__("ufl")
        except ImportError:
            pass
        else:
            backend_dependencies.update({
                "ufl": "/usr/lib/python3/dist-packages/ufl/__init__.py",
            })
        fenics_name = "FEniCS"
    elif backend_name == "dolfinx":
        backend_dependencies = {
            "basix": "/usr/lib/python3/dist-packages/basix/__init__.py",
            "ffcx": "/usr/lib/python3/dist-packages/ffcx/__init__.py",
            "ufl": "/usr/lib/python3/dist-packages/ufl/__init__.py"
        }
        fenics_name = "FEniCSx"
    else:
        raise RuntimeError("This case was never supposed to happen." + CONTACT_ON_ERROR)

    non_system_wide_dependencies = dict()
    for dependency_name, dependency_module_system_path in backend_dependencies.items():
        dependency_module = __import__(dependency_name)
        if dependency_module.__file__ != dependency_module_system_path:
            assert dependency_module.__file__ is not None
            non_system_wide_dependencies[dependency_name] = {
                "expected": dependency_module_system_path,
                "actual": dependency_module.__file__
            }

    dependencies_to_pypi_name = {
        "basix": "fenics-basix",
        "dijitso": "fenics-dijitso",
        "ffc": "fenics-ffc",
        "ffcx": "fenics-ffcx",
        "FIAT": "fenics-fiat",
        "ufl": "fenics-ufl",
        "ufl_legacy": "fenics-ufl-legacy"
    }
    if len(non_system_wide_dependencies):
        non_system_wide_dependencies_error = (
            f"The following {backend_name} dependencies were imported from a local path, "
            "rather than the system wide one:\n"
        )
        for dependency_name, dependency_info in non_system_wide_dependencies.items():
            non_system_wide_dependencies_error += (
                f"* {dependency_name}: expected in {dependency_info['expected']}, "
                f"but imported from {dependency_info['actual']}\n"
            )

        non_system_wide_dependencies_error += "\n"
        non_system_wide_dependencies_error += (
            f"This typically happens when manually pip install-ing core {fenics_name} components, "
            "which end up replacing the system wide installation provided by apt install.\n"
            f"Please remove manually pip install-ed {fenics_name} components as follows:\n"
        )
        for dependency_name, dependency_info in non_system_wide_dependencies.items():
            non_system_wide_dependencies_error += (
                f"* run 'pip uninstall {dependencies_to_pypi_name[dependency_name]}' in a terminal, "
                "and verify that you are prompted to confirm removal of files in "
                f"{os.path.dirname(dependency_info['actual'])}\n"
            )

        non_system_wide_dependencies_error += "\n"
        non_system_wide_dependencies_error += (
            f"If you are sure that you want to use manually pip install-ed core {fenics_name} components "
            "instead of system wide ones, you can disable this check by exporting the "
            "FENICS_SKIP_DEB_CONSISTENCY_CHECK environment variable. Note, however, that this may "
            "break the system wide installation.\n"
        )
        non_system_wide_dependencies_error += (
            "If you believe that this message appears incorrectly, "
            "report this on https://fenicsproject.discourse.group/ ."
        )

        raise ImportError(non_system_wide_dependencies_error)
