# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Mock package for pusimp tests.

This is the same as pusimp_package_two, except for the fact that pusimp.prevent_user_site_imports is
called before the imports of pusimp_dependency_one, pusimp_dependency_two and pusimp_dependency_three.
"""

import pusimp_golden_source

import pusimp

pusimp.prevent_user_site_imports(
    "pusimp_package_three", pusimp_golden_source.system_package_manager, pusimp_golden_source.contact_url,
    pusimp_golden_source.system_path,
    ["pusimp_dependency_one", "pusimp_dependency_two", "pusimp_dependency_three"],
    ["pusimp_dependency_one", "pusimp_dependency_two", "pusimp_dependency_three"],
    [False, False, True],
    ["", "", "pusimp_dependency_three is indeed an optional dependency."]
)

import pusimp_dependency_one  # noqa: E402, F401
import pusimp_dependency_two  # noqa: E402, F401

try:
    import pusimp_dependency_three  # noqa: F401
except ImportError:
    pass
