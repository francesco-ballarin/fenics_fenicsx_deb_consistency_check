# pusimp - prevent user-site imports

**pusimp** is a python library to prevent user-site imports of specific dependencies of a package. The typical scenario for using **pusimp** is in combination with a system manager (e.g., `apt` for Debian), to prevent dependencies from being loaded from user-site instead of the location provided by the system manager.

**pusimp** is currently developed and maintained at [Università Cattolica del Sacro Cuore](https://www.unicatt.it/) by [Dr. Francesco Ballarin](https://www.francescoballarin.it), in collaboration with [Prof. Drew Parsons](https://web.unica.it/unica/page/en/drewf_parsons) at [Università degli Studi di Cagliari](https://www.unica.it/).

## The acronym
**pusimp** is an acronym for "**p**revent **u**ser-**s**ite **imp**orts". However, an internet search reveals that PUSIMP is also a slang term that stands for "Put yourself in my position". In agreement with the slang meaning, **pusimp** reports an informative (although, arguably, quite long) error message to guide the user towards solving the conflict in their dependencies.

## Content

The logic of **pusimp** is implemented in [a single python file](https://github.com/python-pusimp/pusimp/blob/main/pusimp/prevent_user_site_imports.py), which exposes the function `pusimp.prevent_user_site_imports`. **pusimp** can be `pip install`ed from [its GitHub repository](https://github.com/python-pusimp/pusimp/) or from [PyPI](https://pypi.org/project/pusimp/).

## Sample usage

Assume to be the maintainer of a package named `my_package`, with website `https://www.my.package`.
`my_package` depends on the auxiliary packages `my_dependency_one`, `my_dependency_two`, `my_dependency_three`, and optionally on `my_dependency_four`.
Furthermore, assume that all five packages are installed by the system manager `my_apt` at the path `/usr/lib/python3.xy/site-packages`, and that the four dependencies are available on `pypi` as `my-dependency-one`, `my-dependency-two`, `my-dependency-three`, and `my-dependency-four`. The corresponding sample usage in this case is:
```
import pusimp
pusimp.prevent_user_site_imports(
    "my_package", "my_apt", "https://www.my.package",
    "/usr/lib/python3.xy/site-packages",
    ["my_dependency_one", "my_dependency_two", "my_dependency_three", "my_dependency_four"],
    ["my-dependency-one", "my-dependency-two", "my-dependency-three", "my_dependency_four"],
    [False, False, False, True],
    [
        "Additional message for my_dependency_one.",
        "",
        "",
        "Maybe inform the user that my_dependency_four is optional."
    ],
    lambda dependency_pypi_name, dependency_actual_path: f"pip uninstall {dependency_pypi_name}"
)
```
Suppose now to have a broken configuration in which `my_dependency_one` is missing, `my_dependency_two` is broken, while `my_dependency_three` and `my_dependency_four` are installed on the user-site location.
A sample error in such case is the following (the terminal will automatically handle line wrapping of long lines):
```
pusimp has detected the following problems with my_package dependencies:
1) Missing dependencies:
* my_dependency_one is missing. Its expected path was /usr/lib/python3.xy/site-packages/my_dependency_one/__init__.py.
2) Broken dependencies:
* my_dependency_two is broken. Error on import was 'purposely broken'.
3) Dependencies imported from a local path rather than from the path provided by my_apt:
* my_dependency_three was imported from a local path: expected in /usr/lib/python3.xy/site-packages/my_dependency_three/__init__.py, but imported from ~/.local/lib/python3.xy/site-packages/my_dependency_three/__init__.py.
* my_dependency_four was imported from a local path: expected in /usr/lib/python3.xy/site-packages/my_dependency_four/__init__.py, but imported from ~/.local/lib/python3.xy/site-packages/my_dependency_four/__init__.py.

pusimp suggests to apply all of the following fixes:
1) To install missing dependencies:
* check how to install my_dependency_one with my_apt.
2) To fix broken dependencies:
* run 'pip show my-dependency-two' in a terminal: if the location field is not /usr/lib/python3.xy/site-packages consider running 'pip uninstall my-dependency-two' in a terminal, because the broken dependency is probably being imported from a local path rather than from the path provided by my_apt.
3) To uninstall local dependencies:
* run 'pip uninstall my-dependency-three' in a terminal, and verify that you are prompted to confirm removal of files in ~/.local/lib/python3.xy/site-packages/my_dependency_three.
* run 'pip uninstall my_dependency_four' in a terminal, and verify that you are prompted to confirm removal of files in ~/.local/lib/python3.xy/site-packages/my_dependency_four. Maybe inform the user that my_dependency_four is optional.

You can disable this check by exporting the MY_PACKAGE_ALLOW_USER_SITE_IMPORTS environment variable. Note, however, that this may break the installation provided by my_apt.
If you believe that this message appears incorrectly, report this at https://www.my.package .
```
