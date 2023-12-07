# Consistency check between FEniCS/FEniCSx debian packages and local environment

These patches aims at adding an automated way to warn users of FEniCS/FEniCSx debian/ubuntu packages that they are loading core FEniCS/FEniCSx components from a local path, rather than the system wide install path managed by `apt`.

The logic of the consistency check is implemented in [in a single python file](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/blob/main/python3-dolfinx/patches/_deb_consistency_check.py), which would get automatically imported upon patching either [`dolfin/__init__.py`](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/blob/main/python3-dolfin/patches/patch_dolfin_init.patch) or [`dolfinx/__init__.py`](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/blob/main/python3-dolfinx/patches/patch_dolfinx_init.patch).

Tests on a sane configuration (which ships only `apt` packages) and on several dirty configurations (which have one or more local packages overriding system ones) are carried out in a pytest file for either [dolfin](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/blob/main/python3-dolfin/tests/deb_consistency_check/test_dolfin_patches.py) or [dolfinx](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/blob/main/python3-dolfinx/tests/deb_consistency_check/test_dolfinx_patches.py) and run on [GitHub actions](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/actions) by means of a [workflow file](https://github.com/francesco-ballarin/fenics_fenicsx_deb_consistency_check/blob/main/.github/workflows/ci.yml).

A sample error on a dirty configuration is the following (the terminal will handle line wrapping of long lines automatically):
```
ImportError: The following FEniCS dependencies were imported from a local path, rather than the system wide one:
* ufl_legacy: expected in /usr/lib/python3/dist-packages/ufl_legacy/__init__.py, but imported from /tmp/tmpceznic04/venv/lib/python3.11/site-packages/ufl_legacy/__init__.py.
* ufl: expected in /usr/lib/python3/dist-packages/ufl/__init__.py, but imported from /tmp/tmpceznic04/venv/lib/python3.11/site-packages/ufl/__init__.py.

This typically happens when manually pip install-ing core FEniCS components, which end up replacing the system wide installation provided by apt install.
Please remove manually pip install-ed FEniCS components as follows:
* run 'pip uninstall fenics-ufl-legacy' in a terminal, and verify that you are prompted to confirm removal of files in /tmp/tmpceznic04/venv/lib/python3.11/site-packages/ufl_legacy.
* run 'pip uninstall fenics-ufl' in a terminal, and verify that you are prompted to confirm removal of files in /tmp/tmpceznic04/venv/lib/python3.11/site-packages/ufl. Be aware that legacy dolfin codes must now import ufl_legacy instead of ufl, see https://fenicsproject.discourse.group/t/announcement-ufl-legacy-and-legacy-dolfin/11583 .

If you are sure that you want to use manually pip install-ed core FEniCS components instead of system wide ones, you can disable this check by exporting the FENICS_SKIP_DEB_CONSISTENCY_CHECK environment variable. Note, however, that this may break the system wide installation.
If you believe that this message appears incorrectly, report this on https://fenicsproject.discourse.group/ .
```
