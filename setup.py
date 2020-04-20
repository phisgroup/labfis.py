# -*- coding: utf-8 -*-

# Copyright © 2020 labfis.py
# (see LICENSE for details)
"""Setup module for labfis.py.

Since:
    Sep 19, 2019

Authors:
    - Hendrik Dumith Louzada <hendriklouzada@gmail.com>
    - João Carlos Rodrigues Júnior <jc.rodrigues1997@usp.br>
"""
import codecs
import os
import re
from setuptools import setup, find_packages

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    """Find version in a Python file, searching for the __version__."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as pd:
    long_description = pd.read()

version = find_version("labfis", "__init__.py")

APP_NAME        = "labfis"
APP_DESCRIPTION = "Adds a new float type with uncertainty"
AUTHOR          = "Hendrik Dumith Louzada, João Carlos Rodrigues Júnior"
AUTHOR_EMAIL    = "hendriklouzada@gmail.com, jc.rodrigues1997@usp.br"
URL             = "https://github.com/phisgroup/labfis.py"
DOWNLOAD_URL    = "https://pypi.org/project/labfis/"
THEME_NAME      = "Fusion"
COPYRIGHT       = "Copyright (C) 2020, labfis"
LICENSE         = "MIT"


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8']

python_ver = '>=2.7'

setup(name=APP_NAME,
    version=version,
    description=APP_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=classifiers,
    python_requires=python_ver,
)
