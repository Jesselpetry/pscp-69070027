"""HTTP access to iJudge, with retries, backoff and session reuse.

Previously each script opened bare urllib requests with a single attempt and no
status-code discrimination, so one transient blip aborted a full 108-problem
sync and an expired cookie was retried three times unchanged.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

BASE_URL = "https://ijudge.it.kmitl.ac.th"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:153.0) "
    "Gecko/20100101 Firefox/153.0"
)

# Transient conditions worth another attempt. 401/403 are deliberately absent:
# a dead cookie is not fixed by repeating the same request.
RETRY_STATUS = {408, 425, 429, 500, 502, 503, 504}


class HttpError(RuntimeError):
    """Raised when a request fails in a way retrying will not fix."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


class AuthExpired(HttpError):
    """The session cookie was rejected; re-authentication is required."""


def fetch(
    url: str,
    cookie: str,
    rsc: bool = False,
    retries: int = 3,
    timeout: int = 20,
    base_delay: float = 1.0,
) -> str:
    """GET `url`, retrying transient failures with linear backoff.

    Honours Retry-After on 429/503 rather than hammering a university server.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Cookie": cookie,
        "Connection": "close",
    }
    if rsc:
        headers["RSC"] = "1"

    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in (401, 403):
                raise AuthExpired(
                    f"iJudge rejected the session ({e.code}). The cookie is "
                    f"probably expired -- refresh IJUDGE_COOKIE or re-login.",
                    status=e.code,
                ) from e
            if e.code not in RETRY_STATUS or attempt == retries - 1:
                raise HttpError(f"GET {url} failed: HTTP {e.code}", status=e.code) from e
            delay = _retry_after(e) or base_delay * (attempt + 1)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_error = e
            if attempt == retries - 1:
                raise HttpError(f"GET {url} failed: {e}") from e
            time.sleep(base_delay * (attempt + 1))

    # Unreachable: the loop either returns or raises.
    raise HttpError(f"GET {url} failed after {retries} attempts: {last_error}")


def _retry_after(err: urllib.error.HTTPError) -> float | None:
    raw = err.headers.get("Retry-After") if err.headers else None
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except (TypeError, ValueError):
        return None


def extract_balanced(text: str, opener: str = "[", closer: str = "]", start: int = 0) -> str:
    """Return the balanced bracket span beginning at/after `start`."""
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise HttpError("Unbalanced bracket span in RSC stream.")


def fetch_problem_list(cookie: str, course_id: int = 78) -> list[dict[str, Any]]:
    """Fetch the raw problem records for a course from the RSC stream."""
    url = f"{BASE_URL}/courses/{course_id}/problems?page=0"
    rsc = fetch(url, cookie, rsc=True)

    marker = '{"problems":['
    idx = rsc.find(marker)
    if idx == -1:
        raise HttpError(
            f"No problems array in Course {course_id} RSC stream. iJudge's "
            f"frontend may have changed shape, or the session is not valid."
        )
    arr_start = idx + len('{"problems":')
    return json.loads(extract_balanced(rsc, "[", "]", arr_start))
