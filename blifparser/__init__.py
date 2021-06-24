#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imports modules and packages for the developer.
"""

from ._version import __version__

try:
    from . import keywords
    from . import utils
    from . import blifparser

except ImportError:
    from .blifparser import keywords
    from .blifparser import utils
    from .blifparser import blifparser

if __name__ == "__main__":
    blifparser.main()
