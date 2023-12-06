# Copyright (C) 2023 Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Checks that FEniCS/FEniCSx components are not being imported from non-system wide locations."""

import os

FENICS_SKIP_DEB_CONSISTENCY_CHECK = os.getenv("FENICS_SKIP_DEB_CONSISTENCY_CHECK") is not None

if not FENICS_SKIP_DEB_CONSISTENCY_CHECK:
    CONTACT_ON_ASSERT = "\n\nPlease report this error on https://fenicsproject.discourse.group/"

    system_install_path = os.path.dirname(os.path.dirname(__file__))
    assert system_install_path == "/usr/lib/petsc/lib/python3/dist-packages", (
        "Did something change in debian/ubuntu packaging for this path to change?" + CONTACT_ON_ASSERT
    )

    backend_name = os.path.basename(os.path.dirname(__file__))
    assert backend_name in ("dolfin", "dolfinx"), (
        "Did something change in debian/ubuntu packaging for this assert to fail?" + CONTACT_ON_ASSERT
    )
