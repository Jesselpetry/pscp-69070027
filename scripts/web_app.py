#!/usr/bin/env python3
"""Local web dashboard for the PSCP tooling.

    python3 .op/scripts/pscp.py web            # opens http://127.0.0.1:8765
    python3 .op/scripts/web_app.py --port 9000 --no-browser

Sign in to iJudge (session cookie, or username + password used once to mint a
cookie and never stored), then see your progress, browse problems, submit
code to iJudge with a live per-problem result, and run the pscp.py commands.

It listens on 127.0.0.1 only. Every POST must carry a per-launch token that is
embedded in the page, and requests whose Host is not this server are refused,
so another website open in the same browser cannot drive it.
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
SUBMIT_GAP_SEC = 1.0  # same pause submit_oj.py leaves between problems

# What the browser may run: command -> {option: kind}. kind is "flag",
# "ids" (an id list such as 3290-3301,3355) or "int". Positional ids use the
# key "ids". Anything not listed here is rejected before a process starts.
# Submitting has its own endpoint (/api/submit) with a preview step.
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


def registry() -> dict[int, dict[str, Any]]:
    return {r["id"]: r for r in _load_json(paths.SUMMARY_JSON)}


def collect_problems() -> list[dict[str, Any]]:
    """One row per registry problem, joined with what is on disk."""
    folders = paths.index_problem_dirs()
    rows = []
    for pid, rec in sorted(registry().items()):
        folder = folders.get(pid)
        main_py = _read(os.path.join(folder, "main.py")) if folder else None
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
            "archived": os.path.isfile(paths.solution_file(pid)),
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
        "ready_to_submit": sum(r["local"] == "solved" and r["status"] != "Passed" for r in rows),
        "passed_not_local": [r["id"] for r in passed if r["local"] != "solved"],
        "learning_log_missing": [r["id"] for r in rows
                                 if "learning_log" in r["categories"] and not r["has_submission"]],
        "weeks": sorted(weeks.values(), key=lambda w: (w["week"] is None, w["week"] or 0)),
        "categories": cats,
        "upcoming": [dict(r, due=due.isoformat(timespec="minutes")) for due, r in upcoming[:8]],
        "scraped_at": scraped,
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

def current_cookie() -> tuple[str, str | None]:
    env_cookie = (os.environ.get("IJUDGE_COOKIE") or "").strip()
    if env_cookie:
        return env_cookie, "env IJUDGE_COOKIE"
    saved = (load_config().get("cookie") or "").strip()
    return saved, ("submit_config.json" if saved else None)


def auth_state(check: bool) -> dict[str, Any]:
    cookie, source = current_cookie()
    state: dict[str, Any] = {"has_cookie": bool(cookie), "source": source}
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
        return {"ok": False, "error": "วาง access token หรือ cookie ก่อน"}
    if "=" not in cookie:
        cookie = f"access_token={cookie}"
    info = validate_cookie(cookie)
    if not info["valid"]:
        return {"ok": False, "error": "token ใช้ไม่ได้หรือหมดอายุ — ลองคัดลอกใหม่จาก browser"}
    store_cookie(cookie)
    return {"ok": True, "username": info["username"], "fullname": info["fullname"]}


def sign_in_with_password(username: str, password: str) -> dict[str, Any]:
    if not username or not password:
        return {"ok": False, "error": "กรอก username และ password ให้ครบ"}
    try:
        cookie = login(username, password)
    except AuthError as e:
        return {"ok": False, "error": str(e)}
    except Exception as e:  # network, or iJudge redeployed (stale sign-in action id)
        return {"ok": False, "error": f"เข้าสู่ระบบไม่สำเร็จ: {e}"}
    if not cookie:
        return {"ok": False, "error": "username หรือ password ไม่ถูกต้อง (หรือ iJudge เปลี่ยนระบบ login — ใช้ access token แทน)"}
    return sign_in_with_cookie(cookie)


def sign_out() -> None:
    store_cookie("")


# ---------------------------------------------------------------------------
# jobs
# ---------------------------------------------------------------------------

class Job:
    """A pscp.py command running in a subprocess, output kept line by line."""

    kind = "command"

    def __init__(self, job_id: int, argv: list[str]):
        self.id = job_id
        self.argv = argv
        self.lines: list[str] = []
        self.exit_code: int | None = None
        self.started = time.time()
        self.proc: subprocess.Popen | None = None

    @property
    def done(self) -> bool:
        return self.exit_code is not None

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

    def cancel(self) -> None:
        if self.proc and not self.done:
            self.proc.terminate()

    def view(self, since: int) -> dict[str, Any]:
        return {"id": self.id, "kind": self.kind, "argv": self.argv,
                "lines": self.lines[since:], "next": len(self.lines), "done": self.done,
                "exit_code": self.exit_code, "elapsed": round(time.time() - self.started, 1)}


class SubmitJob(Job):
    """Submit main.py files one by one, recording each verdict as it lands."""

    kind = "submit"

    def __init__(self, job_id: int, items: list[dict[str, Any]], cookie: str):
        super().__init__(job_id, ["submit", ",".join(str(i["id"]) for i in items)])
        self.items = items
        self.cookie = cookie
        self.cancelled = False

    def run(self) -> None:
        import submit_oj  # the CLI's own submit/poll code, so both paths stay identical

        conf = load_config()
        course = config.course_id()
        try:
            for n, item in enumerate(self.items):
                if self.cancelled:
                    item["state"] = "cancelled"
                    continue
                if n:
                    time.sleep(SUBMIT_GAP_SEC)
                self._submit_one(submit_oj, item, course, conf)
            self.exit_code = 0 if all(i["state"] == "done" for i in self.items) else 1
        except Exception as e:
            self.lines.append(f"[web] submit stopped: {type(e).__name__}: {e}")
            self.exit_code = -1

    def _submit_one(self, submit_oj: Any, item: dict[str, Any], course: int, conf: dict[str, Any]) -> None:
        pid = item["id"]
        source = _read(item["path"]) or ""
        if code.is_stub(source):
            item.update(state="skipped", error="ยังเป็น stub")
            return
        item["state"] = "submitting"
        try:
            sub_id = submit_oj.submit_problem(pid, source, self.cookie, course_id=course)
        except Exception as e:
            item.update(state="failed", error=str(e))
            self.lines.append(f"OJ {pid}: error {e}")
            return
        if not sub_id:
            item.update(state="failed", error="iJudge ไม่รับ (session หมดอายุ?)")
            self.lines.append(f"OJ {pid}: rejected")
            return
        item.update(state="judging", submission_id=sub_id)
        info = submit_oj.poll_submission_status(
            sub_id, self.cookie,
            poll_timeout=float(conf.get("poll_timeout", 20.0)),
            poll_interval=float(conf.get("poll_interval", 2.0)),
        )
        result = info.get("result") or ""
        all_pass = bool(result) and set(result) == {"P"}
        item.update(
            state="done" if info.get("ready") else "timeout",
            result=result, score=info.get("score", 0.0), pep8=info.get("pep8", 0.0),
            passed=all_pass, perfect=all_pass and info.get("score") == 1000.0,
        )
        self.lines.append(f"OJ {pid}: #{sub_id} {result} score {info.get('score')} pep8 {info.get('pep8')}")

    def cancel(self) -> None:
        self.cancelled = True

    def view(self, since: int) -> dict[str, Any]:
        out = super().view(since)
        out["items"] = [{k: v for k, v in i.items() if k != "path"} for i in self.items]
        return out


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
                raise ValueError(f"{key}: ใส่ id แบบ 3290-3301,3355")
            ids = text.replace(" ", "")
            argv += ids.split(",") if key == "ids" else [key, ids]
    return argv


def _launch(make) -> Job:
    with JOBS_LOCK:
        if any(not j.done for j in JOBS.values()):
            raise RuntimeError("มีงานกำลังรันอยู่ — รอให้เสร็จก่อน")
        job = make(len(JOBS) + 1)
        JOBS[job.id] = job
    threading.Thread(target=job.run, daemon=True).start()
    return job


def start_job(command: str, options: dict[str, Any]) -> Job:
    argv = build_argv(command, options)
    return _launch(lambda job_id: Job(job_id, argv))


# ---------------------------------------------------------------------------
# submission planning
# ---------------------------------------------------------------------------

def _ids_of(value: Any) -> list[int]:
    if not isinstance(value, list):
        raise ValueError("ids must be a list")
    return sorted({int(v) for v in value})


def submit_preview(ids: list[int], skip_passed: bool, include_ll: bool) -> dict[str, Any]:
    """Which of `ids` would be submitted, and why the others would not."""
    import submit_oj

    reg = registry()
    rows = []
    for pid in ids:
        rec = reg.get(pid)
        if rec is None:
            continue
        path = submit_oj.find_solution_file(pid)
        source = _read(path) if path else None
        reason = None
        if source is None:
            reason = "ไม่มี main.py"
        elif code.is_stub(source):
            reason = "ยังเป็น stub"
        elif skip_passed and rec.get("status") == "Passed":
            reason = "ผ่านแล้ว"
        elif rec.get("is_learning_log") and not include_ll:
            reason = "Learning Log"
        rows.append({
            "id": pid,
            "title": config.clean_title(rec.get("name")),
            "week": rec.get("week"),
            "status": rec.get("status"),
            "file": os.path.relpath(path, paths.MAIN_ROOT) if path else None,
            "lines": len(source.splitlines()) if source else 0,
            "warnings": submit_oj.lint_check_code(source) if source and not reason else [],
            "skip": reason,
        })
    return {"rows": rows, "ready": [r["id"] for r in rows if not r["skip"]]}


def start_submit(ids: list[int]) -> Job:
    cookie, _ = current_cookie()
    if not cookie:
        raise RuntimeError("ยังไม่ได้ login iJudge")
    plan = submit_preview(ids, skip_passed=False, include_ll=True)
    items = [
        {"id": r["id"], "title": r["title"], "state": "queued",
         "path": os.path.join(paths.MAIN_ROOT, r["file"])}
        for r in plan["rows"] if not r["skip"]
    ]
    if not items:
        raise RuntimeError("ไม่มีข้อที่ส่งได้ (ต้องมี main.py ที่ไม่ใช่ stub)")
    return _launch(lambda job_id: SubmitJob(job_id, items, cookie))


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
            if route == "/api/weeks":
                return self._json([{"week": w, "label": config.week_label(w),
                                    "title": config.week_title(w)} for w in config.known_weeks()])
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
            if route == "/api/submit/preview":
                return self._json(submit_preview(
                    _ids_of(body.get("ids")), bool(body.get("skip_passed", True)),
                    bool(body.get("include_ll", False))))
            if route == "/api/submit":
                job = start_submit(_ids_of(body.get("ids")))
                return self._json({"job": job.id})
            m = re.fullmatch(r"/api/jobs/(\d+)/cancel", route)
            if m:
                job = JOBS.get(int(m.group(1)))
                if job:
                    job.cancel()
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
            job.cancel()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
