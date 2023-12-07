# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a consistency check between FEniCS/FEniCSx debian packages and local environment.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Checks that FEniCS/FEniCSx components are not being imported from non-system wide locations."""

import importlib
import os
import typing


def _deb_consistency_check(
    fenics_name: str,
    dependencies_import_name: typing.List[str],
    dependencies_apt_name: typing.List[str],
    dependencies_pypi_name: typing.List[str],
    dependencies_optional: typing.List[bool],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Carry out a consistency check between FEniCS/FEniCSx debian packages and local environment."""
    assert len(dependencies_import_name) == len(dependencies_apt_name)
    assert len(dependencies_import_name) == len(dependencies_pypi_name)
    assert len(dependencies_import_name) == len(dependencies_optional)
    assert len(dependencies_import_name) == len(dependencies_extra_error_message)

    skip_deb_consistency_check_env_name = f"{fenics_name.upper()}_SKIP_DEB_CONSISTENCY_CHECK"
    skip_deb_consistency_check_env_value = os.getenv(skip_deb_consistency_check_env_name) is not None

    if not skip_deb_consistency_check_env_value:
        non_system_wide_dependencies: typing.List[
            typing.Optional[typing.Dict[str, str]]
        ] = [None] * len(dependencies_import_name)
        for (dependency_id, dependency_import_name) in enumerate(dependencies_import_name):
            dependency_module_system_path = f"/usr/lib/python3/dist-packages/{dependency_import_name}/__init__.py"
            broken_dependencies_error = (
                f"{dependency_import_name} is missing or broken. "
                f"Please try to fix it with 'apt install --reinstall {dependencies_apt_name[dependency_id]}'."
            )
            if not os.path.exists(dependency_module_system_path) and not dependencies_optional[dependency_id]:
                raise ImportError(broken_dependencies_error)
            try:
                dependency_module = importlib.import_module(dependency_import_name)
            except ImportError:
                if not dependencies_optional[dependency_id]:
                    raise ImportError(broken_dependencies_error)
            else:
                if dependency_module.__file__ != dependency_module_system_path:
                    assert dependency_module.__file__ is not None
                    non_system_wide_dependencies[dependency_id] = {
                        "expected": dependency_module_system_path,
                        "actual": dependency_module.__file__
                    }

        if any([isinstance(dependency_info, dict) for dependency_info in non_system_wide_dependencies]):
            non_system_wide_dependencies_error = (
                f"The following {fenics_name} dependencies were imported from a local path, "
                "rather than the system wide one:\n"
            )
            for (dependency_id, dependency_info) in enumerate(non_system_wide_dependencies):
                if isinstance(dependency_info, dict):
                    non_system_wide_dependencies_error += (
                        f"* {dependencies_import_name[dependency_id]}: expected in {dependency_info['expected']}, "
                        f"but imported from {dependency_info['actual']}.\n"
                    )

            non_system_wide_dependencies_error += "\n"
            non_system_wide_dependencies_error += (
                f"This typically happens when manually pip install-ing core {fenics_name} components, "
                "which end up replacing the system wide installation provided by apt install.\n"
                f"Please remove manually pip install-ed {fenics_name} components as follows:\n"
            )
            for (dependency_id, dependency_info) in enumerate(non_system_wide_dependencies):
                if isinstance(dependency_info, dict):
                    non_system_wide_dependencies_error += (
                        f"* run 'pip uninstall {dependencies_pypi_name[dependency_id]}' in a terminal, "
                        "and verify that you are prompted to confirm removal of files in "
                        f"{os.path.dirname(dependency_info['actual'])}."
                        f"{dependencies_extra_error_message[dependency_id]}\n"
                    )

            non_system_wide_dependencies_error += "\n"
            non_system_wide_dependencies_error += (
                f"If you are sure that you want to use manually pip install-ed core {fenics_name} components "
                "instead of system wide ones, you can disable this check by exporting the "
                f"{skip_deb_consistency_check_env_name} environment variable. Note, however, that this may "
                "break the system wide installation.\n"
            )
            non_system_wide_dependencies_error += (
                "If you believe that this message appears incorrectly, "
                "report this on https://fenicsproject.discourse.group/ ."
            )

            raise ImportError(non_system_wide_dependencies_error)
