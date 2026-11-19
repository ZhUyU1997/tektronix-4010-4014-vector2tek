#!/usr/bin/env python3
"""Run dxf2tek.py with a fixed random seed (ezdxf hatch-pattern jiggle)."""
import os
import random
import runpy
import sys

seed = int(sys.argv.pop(1))
random.seed(seed)
here = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(here, "dxf2tek.py"), run_name="__main__")
