# pusimp - prevent user-site imports

**pusimp** is a python library to prevent user-site imports of specific dependencies of a package. The typical scenario for using **pusimp** is in combination with a system manager (e.g., `apt` for Debian), to prevent dependencies from being loaded from user-site instead of the location provided by the system manager.

**pusimp** is currently developed and maintained at [Università Cattolica del Sacro Cuore](https://www.unicatt.it/) by [Dr. Francesco Ballarin](https://www.francescoballarin.it), in collaboration with [Prof. Drew Parsons](https://web.unica.it/unica/page/en/drewf_parsons) at [Università degli Studi di Cagliari](https://www.unica.it/).

## The acronym
**pusimp** is an acronym for "**p**revent **u**ser-**s**ite **imp**orts". However, an internet search reveals that PUSIMP is also a slang term that stands for "Put yourself in my position". In agreement with the slang meaning, **pusimp** reports an informative (although, arguably, quite long) error message to guide the user towards solving the conflict in their dependencies.

## Content

The logic of **pusimp** is implemented in [a single python file](https://github.com/python-pusimp/pusimp/blob/main/pusimp/prevent_user_site_imports.py), which exposes the function `pusimp.prevent_user_site_imports`. **pusimp** can be `pip install`ed from this repository.

## Sample usage

Assume to be the maintainer of a package named `my_package`, with website `https://www.my.package`.
`my_package` depends on the auxiliary packages `my_dependency_one`, `my_dependency_two`, and optionally on `my_dependency_three`.
Furthermore, assume that all four packages are installed by the system manager `my_apt` at the path `/usr/lib/python3.x/site-packages`, and that the three dependencies are available on `pypi` as `my-dependency-one`, `my-dependency-two` and `my-dependency-three`. The corresponding sample usage in this case is:
```
import pusimp
pusimp.prevent_user_site_imports(
    "my_package", "my_apt", "https://www.my.package",
    "/usr/lib/python3.x/site-packages",
    ["my_dependency_one", "my_dependency_two", "my_dependency_three"],
    ["my-dependency-one", "my-dependency-two", "my-dependency-three"],
    [False, False, True],
    [
        "Additional message for my_dependency_one.",
        "",
        "Maybe inform the user that my_dependency_three is optional."
    ]
)
```
A sample error on a configuration with some packages installed on a user-site is the following (the terminal will automatically handle line wrapping of long lines):
```
TODO -> copy error message
```

## Applications

- Preventing user-site imports in `dolfin` and `dolfinx` packaged for Debian/Ubuntu.
    - `dolfin`: [patch file](https://github.com/python-pusimp/pusimp/blob/main/applications/python3-dolfin/patches/patch_dolfin_init.patch), [unit tests](https://github.com/python-pusimp/pusimp/blob/main/applications/python3-dolfin/tests/unit/test_pusimp.py).
    - `dolfinx`: [patch file](https://github.com/python-pusimp/pusimp/blob/main/applications/python3-dolfinx/patches/patch_dolfinx_init.patch), [unit tests](https://github.com/python-pusimp/pusimp/blob/main/applications/python3-dolfinx/tests/unit/test_pusimp.py).
