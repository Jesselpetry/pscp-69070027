#!/usr/bin/env python3
"""Local web dashboard for the PSCP tooling.

    python3 .op/scripts/pscp.py web            # opens http://127.0.0.1:8765
    python3 .op/scripts/web_app.py --port 9000 --no-browser

Shows progress from the registries, signs in to iJudge (session cookie, or
username + password used once to mint a cookie and never stored), and runs
the pscp.py commands with live output.

It listens on 127.0.0.1 only. Every POST must carry a per-launch token that is
embedded in the page, and requests whose Host is not this server are refused,
so another website open in the same browser cannot drive it. Submitting to
iJudge is deliberately not exposed here: use `pscp.py submit` in a terminal.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ijudge import code, config, paths  # noqa: E402
from ijudge.auth import AuthError, load_config, login, save_config, validate_cookie  # noqa: E402

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(SCRIPT_DIR, "web", "index.html")
PSCP = os.path.join(SCRIPT_DIR, "pscp.py")
TOKEN = secrets.token_urlsafe(24)
MAX_BODY = 64 * 1024
IDS_RE = re.compile(r"^[0-9][0-9,\- ]*$")

# What the browser may run: command -> {option: kind}. kind is "flag",
# "ids" (an id list such as 3290-3301,3355) or "int". Positional ids use the
# key "ids". Anything not listed here is rejected before a process starts.
RUNNABLE: dict[str, dict[str, str]] = {
    "scrape": {"--fast": "flag", "--dry-run": "flag", "--seed-code": "flag", "--only": "ids"},
    "render": {"--dry-run": "flag", "--check": "flag", "--only": "ids"},
    "status": {"--dry-run": "flag"},
    "test": {"ids": "ids", "--week": "int", "--solutions": "flag"},
    "archive": {"--dry-run": "flag", "--update": "flag", "--ids": "ids",
                "--restore": "ids", "--blank": "ids"},
    "readme": {"--dry-run": "flag", "--check": "flag"},
    "doctor": {"--quiet": "flag"},
}


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------

def _load_json(path: str) -> list[dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def _read(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def _deadline(expire: str | None) -> datetime | None:
    try:
        return datetime.strptime(expire or "", "%d %B %Y, %H:%M")
    except ValueError:
        return None


def _categories(rec: dict[str, Any]) -> list[str]:
    names = {
        "is_learning_log": "learning_log",
        "is_recommended": "recommended",
        "is_midterm": "midterm",
        "is_mini_exam": "mini_exam",
    }
    return [name for flag, name in names.items() if rec.get(flag)]


def collect_problems() -> list[dict[str, Any]]:
    """One row per registry problem, joined with what is on disk."""
    folders = paths.index_problem_dirs()
    rows = []
    for rec in sorted(_load_json(paths.SUMMARY_JSON), key=lambda r: r["id"]):
        pid = rec["id"]
        folder = folders.get(pid)
        main_py = _read(os.path.join(folder, "main.py")) if folder else None
        archived = os.path.isfile(paths.solution_file(pid))
        if main_py is None:
            local = "missing"
        elif code.is_stub(main_py):
            local = "stub"
        else:
            local = "solved"
        is_ll = bool(rec.get("is_learning_log"))
        rows.append({
            "id": pid,
            "title": config.clean_title(rec.get("name")),
            "week": rec.get("week"),
            "status": rec.get("status") or "Not Submit",
            "categories": _categories(rec),
            "local": local,
            "archived": archived,
            "folder": os.path.relpath(folder, paths.MAIN_ROOT) if folder else None,
            "deadline": rec.get("expire_date") or "",
            "passed_count": rec.get("passed_count", 0),
            "attempt_count": rec.get("attempt_count", 0),
            "percentage": rec.get("percentage", 0.0),
            "url": rec.get("url"),
            "has_submission": bool(
                is_ll and folder and os.path.isfile(os.path.join(folder, "submission.md"))
            ),
        })
    return rows


def overview() -> dict[str, Any]:
    rows = collect_problems()
    passed = [r for r in rows if r["status"] == "Passed"]

    weeks: dict[Any, dict[str, Any]] = {}
    for r in rows:
        w = weeks.setdefault(r["week"], {
            "week": r["week"], "label": config.week_label(r["week"]),
            "title": config.week_title(r["week"]),
            "total": 0, "passed": 0, "solved": 0,
        })
        w["total"] += 1
        w["passed"] += r["status"] == "Passed"
        w["solved"] += r["local"] == "solved"

    cats = {}
    for name in ("learning_log", "recommended", "midterm", "mini_exam"):
        members = [r for r in rows if name in r["categories"]]
        cats[name] = {"total": len(members),
                      "passed": sum(r["status"] == "Passed" for r in members)}

    now = datetime.now()
    upcoming = []
    for r in rows:
        due = _deadline(r["deadline"])
        if r["status"] != "Passed" and due and due >= now:
            upcoming.append((due, r))
    upcoming.sort(key=lambda t: (t[0], t[1]["id"]))

    try:
        scraped = datetime.fromtimestamp(os.path.getmtime(paths.SUMMARY_JSON)).isoformat(timespec="minutes")
    except OSError:
        scraped = None

    return {
        "total": len(rows),
        "passed": len(passed),
        "not_passed": sum(r["status"] == "Not Passed" for r in rows),
        "not_submitted": sum(r["status"] not in ("Passed", "Not Passed") for r in rows),
        "solved_local": sum(r["local"] == "solved" for r in rows),
        "stubs": sum(r["local"] == "stub" for r in rows),
        "archived": sum(r["archived"] for r in rows),
        "passed_not_local": [r["id"] for r in passed if r["local"] != "solved"],
        "learning_log_missing": [r["id"] for r in rows
                                 if "learning_log" in r["categories"] and not r["has_submission"]],
        "weeks": sorted(weeks.values(), key=lambda w: (w["week"] is None, w["week"] or 0)),
        "categories": cats,
        "upcoming": [dict(r, due=due.isoformat(timespec="minutes")) for due, r in upcoming[:12]],
        "scraped_at": scraped,
        "main_root": paths.MAIN_ROOT,
    }


def problem_detail(pid: int) -> dict[str, Any] | None:
    folder = paths.find_problem_dir(pid)
    if not folder:
        return None
    return {
        "id": pid,
        "folder": os.path.relpath(folder, paths.MAIN_ROOT),
        "problem_md": _read(os.path.join(folder, "problem.md")) or "",
        "main_py": _read(os.path.join(folder, "main.py")) or "",
    }


# ---------------------------------------------------------------------------
# iJudge session
# ---------------------------------------------------------------------------

def _mask(cookie: str) -> str:
    value = cookie.split("=", 1)[-1]
    return f"{value[:6]}…{value[-4:]}" if len(value) > 12 else "…"


def auth_state(check: bool) -> dict[str, Any]:
    env_cookie = (os.environ.get("IJUDGE_COOKIE") or "").strip()
    saved = (load_config().get("cookie") or "").strip()
    cookie, source = (env_cookie, "env IJUDGE_COOKIE") if env_cookie else (saved, "submit_config.json")
    state: dict[str, Any] = {"has_cookie": bool(cookie), "source": source if cookie else None,
                             "masked": _mask(cookie) if cookie else None}
    if check and cookie:
        info = validate_cookie(cookie)
        state.update(valid=info["valid"], username=info["username"],
                     fullname=info["fullname"], error=info["error"])
    return state


def store_cookie(cookie: str) -> None:
    conf = load_config()
    conf["cookie"] = cookie
    save_config(conf)


def sign_in_with_cookie(cookie: str) -> dict[str, Any]:
    cookie = cookie.strip()
    if not cookie:
        return {"ok": False, "error": "ว่าง — วาง cookie จาก browser"}
    if "=" not in cookie:
        cookie = f"access_token={cookie}"
    info = validate_cookie(cookie)
    if not info["valid"]:
        return {"ok": False, "error": info["error"] or "cookie ใช้ไม่ได้"}
    store_cookie(cookie)
    return {"ok": True, "username": info["username"], "fullname": info["fullname"]}


def sign_in_with_password(username: str, password: str) -> dict[str, Any]:
    if not username or not password:
        return {"ok": False, "error": "กรอก username และ password"}
    try:
        cookie = login(username, password)
    except AuthError as e:
        return {"ok": False, "error": str(e)}
    except Exception as e:  # network, iJudge redeploy (stale sign-in action id)
        return {"ok": False, "error": f"เข้าสู่ระบบไม่สำเร็จ: {e}"}
    if not cookie:
        return {"ok": False, "error": "iJudge ไม่ส่ง access_token กลับมา — username/password ผิด หรือ IJUDGE_SIGNIN_ACTION_ID หมดอายุ"}
    return sign_in_with_cookie(cookie)


def sign_out() -> None:
    store_cookie("")


# ---------------------------------------------------------------------------
# jobs
# ---------------------------------------------------------------------------

class Job:
    def __init__(self, job_id: int, argv: list[str]):
        self.id = job_id
        self.argv = argv
        self.lines: list[str] = []
        self.exit_code: int | None = None
        self.started = time.time()
        self.proc: subprocess.Popen[str] | None = None

    def run(self) -> None:
        env = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONWARNINGS="ignore")
        try:
            self.proc = subprocess.Popen(
                [sys.executable, PSCP, *self.argv], cwd=paths.MAIN_ROOT, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                text=True, encoding="utf-8", errors="replace", bufsize=1,
            )
            assert self.proc.stdout is not None
            for line in self.proc.stdout:
                self.lines.append(line.rstrip("\n"))
            self.exit_code = self.proc.wait()
        except OSError as e:
            self.lines.append(f"[web] could not start: {e}")
            self.exit_code = -1

    def view(self, since: int) -> dict[str, Any]:
        return {"id": self.id, "argv": self.argv, "lines": self.lines[since:],
                "next": len(self.lines), "done": self.exit_code is not None,
                "exit_code": self.exit_code, "elapsed": round(time.time() - self.started, 1)}


JOBS: dict[int, Job] = {}
JOBS_LOCK = threading.Lock()


def build_argv(command: str, options: dict[str, Any]) -> list[str]:
    spec = RUNNABLE.get(command)
    if spec is None:
        raise ValueError(f"command {command!r} is not available here")
    argv = [command]
    for key, value in options.items():
        kind = spec.get(key)
        if kind is None:
            raise ValueError(f"{command}: unknown option {key!r}")
        if kind == "flag":
            if value:
                argv.append(key)
        elif value in (None, ""):
            continue
        elif kind == "int":
            argv += [key, str(int(value))]
        else:
            text = str(value).strip()
            if not IDS_RE.match(text):
                raise ValueError(f"{key}: expected ids like 3290-3301,3355")
            ids = text.replace(" ", "")
            argv += ids.split(",") if key == "ids" else [key, ids]
    return argv


def start_job(command: str, options: dict[str, Any]) -> Job:
    argv = build_argv(command, options)
    with JOBS_LOCK:
        if any(j.exit_code is None for j in JOBS.values()):
            raise RuntimeError("มีคำสั่งกำลังรันอยู่ — รอให้เสร็จก่อน")
        job = Job(len(JOBS) + 1, argv)
        JOBS[job.id] = job
    threading.Thread(target=job.run, daemon=True).start()
    return job


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "pscp-web"

    def log_message(self, fmt: str, *args: Any) -> None:  # keep the terminal quiet
        pass

    def _host_ok(self) -> bool:
        port = self.server.server_address[1]
        return self.headers.get("Host", "") in (f"127.0.0.1:{port}", f"localhost:{port}")

    def _send(self, status: int, body: bytes, ctype: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, payload: Any, status: int = 200) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _error(self, status: int, message: str) -> None:
        self._json({"error": message}, status)

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            raise ValueError("request too large")
        data = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        return data

    def do_GET(self) -> None:
        if not self._host_ok():
            return self._error(HTTPStatus.FORBIDDEN, "bad host")
        url = urlparse(self.path)
        query = parse_qs(url.query)
        route = url.path
        try:
            if route == "/":
                page = (_read(PAGE) or "index.html missing").replace("__PSCP_TOKEN__", TOKEN)
                return self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
            if route == "/api/overview":
                return self._json(overview())
            if route == "/api/problems":
                return self._json(collect_problems())
            if route == "/api/auth":
                return self._json(auth_state(check=query.get("check") == ["1"]))
            m = re.fullmatch(r"/api/problem/(\d+)", route)
            if m:
                detail = problem_detail(int(m.group(1)))
                return self._json(detail) if detail else self._error(404, "no such problem")
            m = re.fullmatch(r"/api/jobs/(\d+)", route)
            if m:
                job = JOBS.get(int(m.group(1)))
                if not job:
                    return self._error(404, "no such job")
                return self._json(job.view(int((query.get("since") or ["0"])[0])))
            if route == "/api/jobs":
                return self._json([j.view(len(j.lines)) for j in JOBS.values()])
            return self._error(404, "not found")
        except Exception as e:
            return self._error(500, f"{type(e).__name__}: {e}")

    def do_POST(self) -> None:
        if not self._host_ok():
            return self._error(HTTPStatus.FORBIDDEN, "bad host")
        if not secrets.compare_digest(self.headers.get("X-PSCP-Token", ""), TOKEN):
            return self._error(HTTPStatus.FORBIDDEN, "missing or stale token — reload the page")
        route = urlparse(self.path).path
        try:
            body = self._body()
            if route == "/api/auth/cookie":
                return self._json(sign_in_with_cookie(str(body.get("cookie", ""))))
            if route == "/api/auth/login":
                return self._json(sign_in_with_password(
                    str(body.get("username", "")).strip(), str(body.get("password", ""))))
            if route == "/api/auth/logout":
                sign_out()
                return self._json({"ok": True})
            if route == "/api/run":
                job = start_job(str(body.get("command", "")), dict(body.get("options") or {}))
                return self._json({"job": job.id, "argv": job.argv})
            m = re.fullmatch(r"/api/jobs/(\d+)/cancel", route)
            if m:
                job = JOBS.get(int(m.group(1)))
                if job and job.proc and job.exit_code is None:
                    job.proc.terminate()
                return self._json({"ok": True})
            return self._error(404, "not found")
        except (ValueError, RuntimeError) as e:
            return self._error(400, str(e))
        except Exception as e:
            return self._error(500, f"{type(e).__name__}: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Local web dashboard for the PSCP tooling.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true", help="do not open a browser tab")
    args = parser.parse_args()

    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as e:
        print(f"[!] cannot listen on 127.0.0.1:{args.port}: {e} (try --port)", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{args.port}/"
    print(f"PSCP dashboard: {url}  (Ctrl+C to stop)")
    print(f"main: {paths.MAIN_ROOT}\nOP:   {paths.OP_ROOT}")
    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        for job in JOBS.values():
            if job.proc and job.exit_code is None:
                job.proc.terminate()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
