# -*- coding: utf-8 -*-

# Copyright © 2020 labfis.py
# (see LICENSE for details)

__version__ = "1.2.1"

# Local imports
from labfis.uncertainty import labfloat, Infix

u = Infix(lambda x, y: labfloat(x, y))
