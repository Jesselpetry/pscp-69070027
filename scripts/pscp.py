#!/usr/bin/env python3
"""Single entry point for the PSCP tooling.

    python3 .op/scripts/pscp.py <command> [args...]
    python3 .op/scripts/pscp.py test 3290-3292 --solutions
    python3 .op/scripts/pscp.py archive --help

Each command is a thin alias for one script in this directory; the remaining
arguments are passed through untouched and its exit code is returned, so
`pscp.py <command> --help` shows that script's own options.
"""

from __future__ import annotations

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# command -> (script, one-line description)
COMMANDS: dict[str, tuple[str, str]] = {
    "scrape": ("scrape_all_oj_problems.py", "fetch problems and status from iJudge into the registries"),
    "render": ("render_problems.py", "write problem.md and seed main.py stubs from the registry"),
    "readme": ("update_readme.py", "regenerate README.md on main"),
    "status": ("sync_oj_status.py", "rename oj/ folders to match iJudge pass status"),
    "doctor": ("check_repo.py", "check registry, folders and archive for inconsistencies"),
    "archive": ("archive_solutions.py", "sync solutions/ with main (--update, --restore, --blank)"),
    "test": ("run_samples.py", "run main.py against the official samples"),
    "submit": ("submit_oj.py", "submit solutions to iJudge"),
    "web": ("web_app.py", "local web dashboard: progress, iJudge login, run commands"),
}


def usage() -> str:
    width = max(map(len, COMMANDS))
    lines = [
        "usage: pscp.py <command> [args...]",
        "",
        "commands:",
        *(f"  {name:<{width}}  {desc}" for name, (_, desc) in COMMANDS.items()),
        "",
        "`pscp.py <command> --help` shows the options of that command.",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(usage())
        return 0
    command, rest = argv[0], argv[1:]
    if command not in COMMANDS:
        print(f"pscp.py: unknown command {command!r}\n", file=sys.stderr)
        print(usage(), file=sys.stderr)
        return 2
    script = os.path.join(SCRIPT_DIR, COMMANDS[command][0])
    if not os.path.isfile(script):
        print(
            f"pscp.py: {command!r} needs {os.path.relpath(script)}, which does not exist",
            file=sys.stderr,
        )
        return 2
    try:
        return subprocess.run([sys.executable, script, *rest]).returncode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
