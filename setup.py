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

version = find_version("labfis", "__init__.py")
long_description = "Adds a new float class type with an float and uncertainty value"

APP_NAME        = "labfis"
APP_DESCRIPTION = "Adds a new float type with uncertainty"
AUTHOR          = "Hendrik Dumith Louzada, João Carlos Rodrigues Júnior"
AUTHOR_EMAIL    = "hendriklouzada@gmail.com, jc.rodrigues1997@usp.br"
URL             = "https://github.com/phisgroup/labfis.py"
THEME_NAME      = "Fusion"
COPYRIGHT       = "Copyright (C) 2020, labfis"


classifiers = [
    'Development Status :: 4 - Beta',
    'Framework :: labfis',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python 2.7 :: Python 3 :: Python 3.8']

python_ver = '>=2.7'

setup(name=APP_NAME,
    version=version,
    description=APP_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    long_description=long_description,
    packages=find_packages(),
    classifiers=classifiers,
    python_requires=python_ver,
)
