# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a simple library to prevent user-site imports on a specific set of dependencies.
#
# SPDX-License-Identifier: MIT
"""Prevent user-site imports on a specific set of dependencies."""

import importlib
import os
import typing


def check(
    package_name: str,
    system_manager: str,
    contact_url: str,
    dependencies_expected_prefix: str,
    dependencies_import_name: typing.List[str],
    dependencies_pypi_name: typing.List[str],
    dependencies_optional: typing.List[bool],
    dependencies_extra_error_message: typing.List[str]
) -> None:
    """Prevent user-site imports on a specific set of dependencies."""
    assert len(dependencies_import_name) == len(dependencies_pypi_name)
    assert len(dependencies_import_name) == len(dependencies_optional)
    assert len(dependencies_import_name) == len(dependencies_extra_error_message)

    allow_user_site_imports_env_name = f"{package_name}_allow_user_site_imports".upper()
    allow_user_site_imports_env_value = os.getenv(allow_user_site_imports_env_name) is not None

    if not allow_user_site_imports_env_value:
        user_site_dependencies: typing.List[
            typing.Optional[typing.Dict[str, str]]
        ] = [None] * len(dependencies_import_name)
        for (dependency_id, dependency_import_name) in enumerate(dependencies_import_name):
            dependency_module_expected_path = f"{dependencies_expected_prefix}/{dependency_import_name}/__init__.py"
            broken_dependencies_error = (
                f"{dependency_import_name} is MISSING_OR_BROKEN."
            )
            if not os.path.exists(dependency_module_expected_path) and not dependencies_optional[dependency_id]:
                raise ImportError(
                    broken_dependencies_error.replace("MISSING_OR_BROKEN", "missing"))
            try:
                dependency_module = importlib.import_module(dependency_import_name)
            except ImportError as dependency_module_import_error:
                if not dependencies_optional[dependency_id]:
                    raise ImportError(
                        broken_dependencies_error.replace(
                            "MISSING_OR_BROKEN", f"broken. Error on import was '{dependency_module_import_error}'"))
            else:
                if dependency_module.__file__ != dependency_module_expected_path:
                    assert dependency_module.__file__ is not None
                    user_site_dependencies[dependency_id] = {
                        "expected": dependency_module_expected_path,
                        "actual": dependency_module.__file__
                    }

        if any([isinstance(dependency_info, dict) for dependency_info in user_site_dependencies]):
            user_site_dependencies_error = (
                f"The following {package_name} dependencies were imported from a local path:\n"
            )
            for (dependency_id, dependency_info) in enumerate(user_site_dependencies):
                if isinstance(dependency_info, dict):
                    user_site_dependencies_error += (
                        f"* {dependencies_import_name[dependency_id]}: expected in {dependency_info['expected']}, "
                        f"but imported from {dependency_info['actual']}.\n"
                    )

            user_site_dependencies_error += "\n"
            user_site_dependencies_error += (
                f"This typically happens when manually pip install-ing {package_name} dependencies, "
                "which end up replacing the installation provided by {system_manager}.\n"
                f"Please remove manually pip install-ed {package_name} components as follows:\n"
            )
            for (dependency_id, dependency_info) in enumerate(user_site_dependencies):
                if isinstance(dependency_info, dict):
                    user_site_dependencies_error += (
                        f"* run 'pip uninstall {dependencies_pypi_name[dependency_id]}' in a terminal, "
                        "and verify that you are prompted to confirm removal of files in "
                        f"{os.path.dirname(dependency_info['actual'])}."
                        f"{dependencies_extra_error_message[dependency_id]}\n"
                    )

            user_site_dependencies_error += "\n"
            user_site_dependencies_error += (
                f"If you are sure that you want to use manually pip install-ed {package_name} dependencies "
                "instead of the ones provided by {system_manager}, you can disable this check by exporting the "
                f"{allow_user_site_imports_env_name} environment variable. Note, however, that this may "
                "break the installation provided by {system_manager}.\n"
            )
            user_site_dependencies_error += (
                "If you believe that this message appears incorrectly, "
                f"report this at {contact_url} ."
            )

            raise ImportError(user_site_dependencies_error)
