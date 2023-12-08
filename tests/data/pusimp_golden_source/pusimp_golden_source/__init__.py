# Copyright (C) 2023 by the pusimp authors
#
# This file is part of pusimp.
#
# SPDX-License-Identifier: MIT
"""Golden source for pusimp.

The goal of this package is to provide a mock system path, a mock contact URL, and a mock system package manager.
"""

import os

contact_url = "mock contact URL"
system_path = os.path.dirname(__file__)
system_package_manager = "mock system package manager"
