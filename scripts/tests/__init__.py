"""Unit tests for the OP tooling.

Run from the repo root:

    python3 -m unittest discover -s .op/scripts/tests -t .op/scripts

They read the real data/ registries and main's problem folders, read-only.
"""

import os
import sys

# `-t .op/scripts` already puts the scripts dir on sys.path; this keeps other
# runners (e.g. `python3 -m unittest tests.test_code` from scripts/) working.
_SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
