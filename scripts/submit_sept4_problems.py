#!/usr/bin/env python3
"""
Convenience shortcut to submit September 4th problems using the standardized submit_oj.py runner.
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMIT_OJ = os.path.join(SCRIPT_DIR, "submit_oj.py")

if __name__ == "__main__":
    cmd = [sys.executable, SUBMIT_OJ, "--expire", "4 September 2026"] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))
