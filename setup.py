from distutils import util
from typing import Dict

import setuptools

version: Dict[str, str] = {}
path = util.convert_path("src/refacto/version.py")
with open(path) as version_file:
    exec(version_file.read(), version)  # noqa: S102 DUO105, WPS421

setuptools.setup(version=version["__version__"])
