# Copyright (C) PyScaffold contributors, Francesco Ballarin, Drew Parsons
#
# This file is part of a proposal for FEniCS/FEniCSx debian packaging.
#
# SPDX-License-Identifier: MIT
"""Helper class to create a virtual environment.

Forked and simplified from https://github.com/pyscaffold/pyscaffold/blob/master/tests/virtualenv.py .
"""

import os
import pathlib
import subprocess
import sys

import virtualenv


class VirtualEnv:
    """Helper class to create a virtual environment."""

    def __init__(self, path: str) -> None:
        self.path = pathlib.Path(path) / "venv"
        self.sys_path = str(
            self.path / "lib" / ("python" + str(sys.version_info.major) + "." + str(sys.version_info.minor))
            / "site-packages"
        )
        self.executable = str(self.path / "bin" / "python3")
        self.env = dict(os.environ)
        self.env.pop("PYTHONPATH", None)  # ensure isolation

    def create(self) -> None:
        """Create a virtual environment, and add it to sys.path."""
        args = [str(self.path), "--python", sys.executable, "--system-site-packages", "--no-wheel"]
        virtualenv.cli_run(args, env=self.env)

    def install_package(self, package: str) -> None:
        """Install a package in the virtual environment."""
        run_install = subprocess.run(
            f"{self.executable} -m pip install --ignore-installed {package}", shell=True, capture_output=True)
        if run_install.returncode != 0:
            raise RuntimeError(
                f"Installing {package} failed.\n"
                f"stdout contains {run_install.stdout.decode()}\n"
                f"stderr contains {run_install.stderr.decode()}\n")
