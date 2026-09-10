"""Dry-run-aware filesystem mutation layer.

Every write performed by the automation scripts goes through these helpers, so
`--dry-run` is enforced in one place instead of at ~20 call sites, and JSON
registries are always written atomically.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from typing import Any

_DRY_RUN = False


def set_dry_run(value: bool) -> None:
    global _DRY_RUN
    _DRY_RUN = bool(value)


def is_dry_run() -> bool:
    return _DRY_RUN


def _plan(msg: str) -> None:
    """Report a mutation that --dry-run suppressed."""
    print(f"[DRY-RUN] {msg}", file=sys.stderr)


def ensure_dir(path: str) -> None:
    if not path:
        return
    if _DRY_RUN:
        if not os.path.isdir(path):
            _plan(f"Would create directory: {path}")
        return
    os.makedirs(path, exist_ok=True)


def write_text(path: str, content: str) -> None:
    if _DRY_RUN:
        verb = "overwrite" if os.path.exists(path) else "create"
        _plan(f"Would {verb} {path} ({len(content)} bytes)")
        return
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def safe_write_json(target_path: str, data: Any) -> None:
    """Write JSON atomically: a crash mid-write cannot truncate the registry.

    The temp file is created in the destination directory so os.replace stays on
    one filesystem and is therefore atomic.
    """
    if _DRY_RUN:
        verb = "overwrite" if os.path.exists(target_path) else "create"
        size = len(data) if isinstance(data, (list, dict)) else "?"
        _plan(f"Would {verb} {target_path} ({size} records)")
        return
    parent = os.path.dirname(target_path) or "."
    os.makedirs(parent, exist_ok=True)
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", dir=parent, prefix=".tmp-", suffix=".json",
            delete=False, encoding="utf-8",
        ) as tf:
            # Bind the name BEFORE serializing: json.dump raising partway through
            # must still leave a name for the finally block to clean up.
            tmp_name = tf.name
            json.dump(data, tf, ensure_ascii=False, indent=2)
            tf.flush()
            os.fsync(tf.fileno())
        os.replace(tmp_name, target_path)
        tmp_name = None
    finally:
        if tmp_name and os.path.exists(tmp_name):
            os.unlink(tmp_name)


def rename_dir(src: str, dst: str) -> bool:
    """Rename a directory, refusing to clobber an existing target.

    os.rename onto an existing directory either raises or silently replaces
    depending on platform and emptiness. Neither is acceptable for a folder
    holding a solution, so refuse and report instead.
    """
    if os.path.exists(dst):
        print(
            f"[SKIP] target already exists, not renaming: "
            f"{os.path.basename(src)!r} -> {os.path.basename(dst)!r}",
            file=sys.stderr,
        )
        return False
    if _DRY_RUN:
        _plan(f"Would rename: {os.path.basename(src)!r} -> {os.path.basename(dst)!r}")
        return True
    os.rename(src, dst)
    return True
