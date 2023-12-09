# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Test imports of mock packages in tests/data."""

import importlib
import os
import shutil
import sys
import tempfile

import pytest

import pusimp_golden_source  # isort: skip


def test_data_one() -> None:
    """Test that the first mock package in tests/data import correctly."""
    import pusimp_package_one  # noqa: F401


def test_data_two() -> None:
    """Test that the second mock package in tests/data import correctly."""
    import pusimp_package_two  # noqa: F401


def test_data_three() -> None:
    """Test that the third mock package in tests/data import correctly."""
    import pusimp_package_three  # noqa: F401


def test_data_four() -> None:
    """Test that the fourth mock package in tests/data fails to import due to a missing mandatory dependency."""
    with pytest.raises(ImportError) as excinfo:
        import pusimp_package_four  # noqa: F401
    import_error_text = str(excinfo.value)
    print(f"The following ImportError was raised:\n{import_error_text}")
    assert import_error_text == (
        "pusimp_dependency_missing is missing. Its expected path was "
        f"{os.path.join(pusimp_golden_source.system_path, 'pusimp_dependency_missing', '__init__.py')}."
    )


def test_data_five() -> None:
    """Test that the fifth mock package in tests/data import correctly, because the missing dependency is optional."""
    import pusimp_package_five  # noqa: F401


def test_data_six() -> None:
    """Test that the sixth mock package in tests/data fails to import due to a broken mandatory dependency."""
    with pytest.raises(ImportError) as excinfo:
        import pusimp_package_six  # noqa: F401
    import_error_text = str(excinfo.value)
    print(f"The following ImportError was raised:\n{import_error_text}")
    assert import_error_text == (
        "pusimp_dependency_four is broken. Error on import was 'pusimp_dependency_four is a broken package.'."
    )


def test_data_seven() -> None:
    """Test that the seventh mock package in tests/data import correctly, because the broken dependency is optional."""
    import pusimp_package_seven  # noqa: F401


def test_data_eight_nine() -> None:
    """Test that the eighth/ninth mock package in tests/data fails to import due to dependencies from user site.

    Note that the eighth and ninth mock package are tested in the same function, rather than two separate functions,
    because they both the depend on pusimp_dependency_five and pusimp_dependency_six, which will get replaced
    by an user-site installation inside this test. However, since the python interpreter only loads a module once,
    we have to be sure that every mock package that requires pusimp_dependency_five and pusimp_dependency_six operates
    in the same environment.
    """
    mock_system_site_path = pusimp_golden_source.system_path
    mock_user_site_path = tempfile.mkdtemp()
    sys.path.insert(0, mock_user_site_path)
    for dependency_import_name in ("pusimp_dependency_five", "pusimp_dependency_six"):
        dependency_user_site = os.path.join(mock_user_site_path, dependency_import_name)
        os.makedirs(dependency_user_site)
        with open(os.path.join(dependency_user_site, "__init__.py"), "w") as init_file:
            init_file.write("# created by pytest")
    try:
        for pusimp_package in ("pusimp_package_eight", "pusimp_package_nine"):
            with pytest.raises(ImportError) as excinfo:
                importlib.import_module(pusimp_package)
            import_error_text = str(excinfo.value)
            print(f"The following ImportError was raised:\n{import_error_text}")
            assert (
                f"The following {pusimp_package} dependencies were imported from a local path" in import_error_text)
            assert (
                "which end up replacing the installation provided by mock system package manager" in import_error_text)
            assert (
                "believe that this message appears incorrectly, report this at mock contact URL ." in import_error_text)
            for (dependency_import_name, dependency_optional_string) in (
                ("pusimp_dependency_five", "mandatory"),
                ("pusimp_dependency_six", "optional")
            ):
                assert (
                    f"* {dependency_import_name}: expected in "
                    f"{os.path.join(mock_system_site_path, dependency_import_name, '__init__.py')}, "
                    f"but imported from "
                    f"{os.path.join(mock_user_site_path, dependency_import_name, '__init__.py')}."
                ) in import_error_text
                dependency_pypi_name = dependency_import_name.replace("_", "-")
                assert (
                    f"* run 'pip uninstall {dependency_pypi_name}' in a terminal, "
                    f"and verify that you are prompted to confirm removal of files in "
                    f"{os.path.join(mock_user_site_path, dependency_import_name)}. "
                    f"{dependency_import_name} is {dependency_optional_string}."
                ) in import_error_text
    finally:
        del sys.path[0]
        shutil.rmtree(mock_user_site_path, ignore_errors=True)
