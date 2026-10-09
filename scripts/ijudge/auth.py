"""iJudge credential resolution, sign-in and session-cookie caching.

Credentials come from the environment only. There are deliberately no built-in
defaults: a hardcoded password previously reached a public GitHub repository.
"""

from __future__ import annotations

import http.cookiejar
import json
import os
import re
import sys
import urllib.request
from typing import Any

from . import config as course_config
from .client import BASE_URL, USER_AGENT, AuthExpired
from .paths import CONFIG_FILE

# Prefer a browser session cookie; the password path exists only to mint one.
IJUDGE_USERNAME = os.environ.get("IJUDGE_USER")
IJUDGE_PASSWORD = os.environ.get("IJUDGE_PASS")

# Next.js server-action id for the sign-in endpoint. Not a secret, but pinned to
# a specific iJudge build -- re-copy from a browser network capture if sign-in
# starts failing after they redeploy.
SIGNIN_ACTION_ID = os.environ.get(
    "IJUDGE_SIGNIN_ACTION_ID", "7f151777b5ab2e8348f2efaa6a76d5128cb6e64a71"
)

DEFAULT_CONFIG: dict[str, Any] = {
    "exclude_learning_logs": True,
    "poll_interval": 2.0,
    "poll_timeout": 20.0,
    "cookie": "",
}


class AuthError(RuntimeError):
    """Credentials are missing or sign-in failed."""


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_303(self, req, fp, code, msg, headers):
        return fp


def load_config(path: str = CONFIG_FILE) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG, course_id=course_config.course_id())
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except (OSError, ValueError) as e:
            print(f"[!] Warning: failed to parse {path}: {e}", file=sys.stderr)
    return config


def save_config(config: dict[str, Any], path: str = CONFIG_FILE) -> None:
    """Persist config. Session state, not repo data -- written even in dry-run."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"[!] Warning: could not save {path}: {e}", file=sys.stderr)


def login(username: str | None = None, password: str | None = None) -> str | None:
    """Sign in and return an `access_token=...` cookie string."""
    username = username or IJUDGE_USERNAME
    password = password or IJUDGE_PASSWORD
    if not username or not password:
        raise AuthError(
            "iJudge credentials missing. Set IJUDGE_USER and IJUDGE_PASS in the "
            "environment, or set IJUDGE_COOKIE to reuse a browser session. "
            "See .env.example."
        )

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar), _NoRedirectHandler
    )
    payload = json.dumps([username, password, "/"]).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/signin",
        data=payload,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/x-component",
            "Content-Type": "text/plain;charset=UTF-8",
            "Next-Action": SIGNIN_ACTION_ID,
            "Origin": BASE_URL,
            "Referer": f"{BASE_URL}/signin",
            "Connection": "close",
        },
    )
    opener.open(req)
    for cookie in jar:
        if cookie.name == "access_token":
            return f"access_token={cookie.value}"
    return None


def validate_cookie(cookie: str) -> dict[str, Any]:
    """Check a cookie against /submissions/me and return the profile it names."""
    if not cookie or not cookie.strip():
        return {"valid": False, "username": None, "fullname": None, "error": "Empty cookie"}

    try:
        import requests
        resp = requests.get(
            f"{BASE_URL}/submissions/me/overview",
            headers={"User-Agent": USER_AGENT, "Cookie": cookie, "RSC": "1"},
            timeout=10,
        )
        body = resp.content.decode("utf-8")
    except Exception:
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/submissions/me/overview",
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "*/*",
                    "rsc": "1",
                    "Cookie": cookie,
                },
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")
        except Exception as e:
            return {"valid": False, "username": None, "fullname": None, "error": str(e)}

    m_user = re.search(r"\"username\":\"([^\"]+)\"", body)
    m_name = re.search(r"\"fullname\":\"([^\"]+)\"", body)
    if m_user:
        return {
            "valid": True,
            "username": m_user.group(1),
            "fullname": m_name.group(1) if m_name else "",
            "error": None,
        }
    return {
        "valid": False, "username": None, "fullname": None,
        "error": "Not authenticated (invalid session)",
    }


def is_cookie_expired(cookie: str | None) -> bool:
    """Check whether an access_token cookie has passed expiration."""
    if not cookie:
        return True
    try:
        import base64
        import time
        token = cookie.split("access_token=")[-1].split(";")[0].strip()
        parts = token.split(".")
        if len(parts) >= 2:
            padding = "=" * (4 - len(parts[1]) % 4)
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + padding))
            exp = payload.get("exp")
            if exp and time.time() >= exp:
                return True
            return False
    except Exception:
        pass
    return False


def find_browser_cookie() -> str | None:
    """Extract an active iJudge cookie from browser profiles (Zen/Firefox)."""
    import glob
    import shutil
    import sqlite3

    zen_dirs = glob.glob(
        os.path.expanduser(
            "~/Library/Application Support/zen/Profiles/*.Default*"
        )
    )
    for d in zen_dirs:
        db_path = os.path.join(d, "cookies.sqlite")
        if os.path.isfile(db_path):
            temp_db = f"/tmp/ijudge_cookie_{os.getpid()}.sqlite"
            try:
                shutil.copy2(db_path, temp_db)
                conn = sqlite3.connect(temp_db)
                cur = conn.cursor()
                query = (
                    "SELECT value FROM moz_cookies "
                    "WHERE host LIKE '%ijudge%' AND name='access_token'"
                )
                cur.execute(query)
                row = cur.fetchone()
                conn.close()
                if row and row[0]:
                    candidate = f"access_token={row[0]}"
                    if not is_cookie_expired(candidate):
                        return candidate
            except Exception:
                pass
            finally:
                if os.path.exists(temp_db):
                    try:
                        os.remove(temp_db)
                    except OSError:
                        pass
    return None


def resolve_cookie(config_file: str = CONFIG_FILE, quiet: bool = False) -> str:
    """Find a usable session cookie, minting a fresh one as a last resort.

    Order: IJUDGE_COOKIE env -> cached config -> browser profile -> sign-in.
    """
    env_cookie = os.environ.get("IJUDGE_COOKIE")
    if env_cookie and env_cookie.strip():
        if not is_cookie_expired(env_cookie):
            return env_cookie.strip()

    cached = ""
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                cached = (json.load(f).get("cookie") or "").strip()
            if cached and not is_cookie_expired(cached):
                return cached
        except (OSError, ValueError) as e:
            print(f"[!] Warning: could not read {config_file}: {e}",
                  file=sys.stderr)

    # Auto-extract from browser profile if cached cookie is expired or missing
    browser_cookie = find_browser_cookie()
    if browser_cookie:
        if not quiet:
            print("[*] Automatically refreshed iJudge session cookie "
                  "from browser profile.")
        config = load_config(config_file)
        config["cookie"] = browser_cookie
        save_config(config, config_file)
        return browser_cookie

    if cached:
        return cached

    if not IJUDGE_USERNAME or not IJUDGE_PASSWORD:
        raise AuthError(
            "No iJudge session available. Set IJUDGE_COOKIE, or set IJUDGE_USER "
            "and IJUDGE_PASS so a fresh session can be created. See .env.example."
        )

    if not quiet:
        print(f"[*] Logging in to iJudge as {IJUDGE_USERNAME}...")
    token_cookie = login()
    if not token_cookie:
        raise AuthError(
            "Failed to log in to iJudge. Check the credentials, or supply a "
            "valid IJUDGE_COOKIE."
        )
    if not quiet:
        print("    Authentication successful.")

    # Cache the token. This is session state rather than repo data, so it is
    # written even under --dry-run to avoid forcing a second login.
    config = load_config(config_file)
    config["cookie"] = token_cookie
    save_config(config, config_file)
    return token_cookie
