#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imports modules and packages for the user that executes:

python -m blifparser <input_path>
"""

from ._version import __version__

try:
    from . import keywords
    from . import utils
    from . import blifparser

except ImportError:
    from .blifparser import keywords    # type: ignore
    from .blifparser import utils       # type: ignore
    from .blifparser import blifparser  # type: ignore

if __name__ == "__main__":
    blifparser.main()
