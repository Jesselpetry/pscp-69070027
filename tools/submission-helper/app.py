"""
PSCP Submission Helper - local dashboard.

Formats student-provided raw text into the course submission.md /
ai_reflection.md templates. Never invents content: every field below is
copied verbatim from what the student types into the web form.

Run:  python3 tools/submission-helper/app.py
Open: http://localhost:5050
"""

import json
import re
import unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
OJ_DIR = ROOT / "oj"
TEMPLATES_DIR = ROOT / "AI-Guidelines-PSCP" / "templates"
SUBMISSION_TEMPLATE = TEMPLATES_DIR / "SUBMISSION_TEMPLATE.th.md"
REFLECTION_TEMPLATE = TEMPLATES_DIR / "AI_REFLECTION_TEMPLATE.th.md"
STATIC_HTML = Path(__file__).resolve().parent / "index.html"

FOLDER_RE = re.compile(r"^(?:\[LEARNING-LOGS\]-)?oj_(\d{4})-(.+?)(\s*✅)?$")

# Index of every ```text``` block in SUBMISSION_TEMPLATE.th.md, in document
# order. None = informational block, left untouched.
SUBMISSION_BLOCK_FIELDS = [
    "oj_title", "submission_id", "oj_status", "time_spent", None,
    "understanding", "first_plan", "final_approach",
    "t1_why", "t1_input", "t1_expected", "t1_actual", "t1_result",
    "t2_why", "t2_input", "t2_expected", "t2_actual", "t2_result",
    "t3_why", "t3_input", "t3_expected", "t3_actual", "t3_result",
    "used_ai", None,
    "human_help", "who_helped", "what_help", "still_own_work", "copied_code",
]

SUBMISSION_CERT_STATEMENTS = [
    "I wrote this submission in my own words.",
    "I understand my final code.",
    "I recorded the real OJ status.",
    "I did not copy AI-generated text directly into this file.",
    "I did not copy code from another person.",
    "If I received human help, I disclosed it in this file.",
    "I submitted the final code to the OJ by myself.",
]

# Index of every ```text``` block in AI_REFLECTION_TEMPLATE.th.md.
REFLECTION_BLOCK_FIELDS = [
    None, None,
    "ai_tool", "policy_no_explain", "what_asked", "what_noticed",
    "what_checked", "what_learned",
]

REFLECTION_INFO_ROWS = ["OJ problem number/title", "OJ submission ID, if submitted", "OJ status"]

REFLECTION_POLICY_STATEMENTS = [
    "I read the relevant workflow before using AI.",
    "I used `instructions/COURSE_AI_INSTRUCTIONS.md`, `instructions/AGENTS.md`, or manually followed the course AI instructions if the tool did not support custom instructions.",
    "I wrote my own problem understanding before asking AI for help.",
    "I wrote my own first plan before asking AI for help.",
    "I used AI as a coach, reviewer, debugger, or test-case helper, not as a full-answer generator.",
]

REFLECTION_CERT_STATEMENTS = [
    "I wrote this reflection in my own words.",
    "This reflection describes my real AI use.",
    "I checked AI's suggestions before using them.",
    "I can explain my final code.",
    "I did not ask AI to write this reflection for me.",
]

MAIN_PY_TEMPLATE = '''def main():
    pass


if __name__ == "__main__":
    main()
'''


def fill_text_blocks(template_text, field_names, values):
    blocks = list(re.finditer(r"```text\n(.*?)\n```", template_text, re.DOTALL))
    if len(blocks) != len(field_names):
        raise ValueError("template block count changed, refusing to guess")
    out = []
    cursor = 0
    for block, field in zip(blocks, field_names):
        out.append(template_text[cursor:block.start()])
        if field is None:
            out.append(block.group(0))
        else:
            content = values.get(field, "") or ""
            out.append("```text\n" + content + "\n```")
        cursor = block.end()
    out.append(template_text[cursor:])
    return "".join(out)


def fill_two_col_row(text, label, value):
    pattern = re.compile(r"^\|[ \t]*" + re.escape(label) + r"[ \t]*\|[^|\n]*\|[ \t]*$", re.MULTILINE)
    replacement = f"| {label} | {value} |"
    new_text, n = pattern.subn(lambda m: replacement, text, count=1)
    if n == 0:
        raise ValueError(f"row not found: {label}")
    return new_text


def fill_three_col_row(text, label, value, note):
    pattern = re.compile(r"^\|[ \t]*" + re.escape(label) + r"[ \t]*\|[^|\n]*\|[^|\n]*\|[ \t]*$", re.MULTILINE)
    replacement = f"| {label} | {value} | {note} |"
    new_text, n = pattern.subn(lambda m: replacement, text, count=1)
    if n == 0:
        raise ValueError(f"row not found: {label}")
    return new_text


def build_submission_md(fields):
    text = SUBMISSION_TEMPLATE.read_text(encoding="utf-8")
    text = fill_text_blocks(text, SUBMISSION_BLOCK_FIELDS, fields)
    cert = fields.get("certifications", {})
    for statement in SUBMISSION_CERT_STATEMENTS:
        text = fill_two_col_row(text, statement, "Yes" if cert.get(statement) else "")
    return text


def build_reflection_md(fields):
    text = REFLECTION_TEMPLATE.read_text(encoding="utf-8")
    text = fill_text_blocks(text, REFLECTION_BLOCK_FIELDS, fields)
    info = fields.get("info", {})
    for label in REFLECTION_INFO_ROWS:
        text = fill_two_col_row(text, label, info.get(label, ""))
    policy = fields.get("policy", {})
    for statement in REFLECTION_POLICY_STATEMENTS:
        row = policy.get(statement, {})
        text = fill_three_col_row(text, statement, row.get("answer", ""), row.get("note", ""))
    cert = fields.get("certifications", {})
    for statement in REFLECTION_CERT_STATEMENTS:
        text = fill_two_col_row(text, statement, "Yes" if cert.get(statement) else "")
    return text


def slugify_name(name):
    name = unicodedata.normalize("NFKC", name).strip()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w฀-๿-]", "", name)
    return name


def list_problems():
    problems = []
    if not OJ_DIR.exists():
        return problems
    for entry in sorted(OJ_DIR.iterdir()):
        if not entry.is_dir():
            continue
        m = FOLDER_RE.match(entry.name)
        if not m:
            continue
        problem_id, name, passed = m.group(1), m.group(2), bool(m.group(3))
        learning_log = entry.name.startswith("[LEARNING-LOGS]-")
        problems.append({
            "folder": entry.name,
            "id": problem_id,
            "name": name,
            "passed": passed,
            "learning_log": learning_log,
            "has_submission": (entry / "submission.md").exists(),
            "has_reflection": (entry / "ai_reflection.md").exists(),
            "has_main": (entry / "main.py").exists(),
        })
    problems.sort(key=lambda p: p["id"])
    return problems


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def _folder_from_path(self, prefix):
        rest = unquote(self.path[len(prefix):])
        folder = rest.split("/")[0]
        path = OJ_DIR / folder
        if OJ_DIR not in path.resolve().parents and path.resolve() != OJ_DIR:
            raise ValueError("invalid folder")
        if not path.is_dir():
            raise FileNotFoundError(folder)
        return folder, path

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = STATIC_HTML.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/problems":
            self._send_json({"problems": list_problems()})
            return
        self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        try:
            if self.path == "/api/problems":
                self._create_problem()
            elif self.path.startswith("/api/problems/") and self.path.endswith("/toggle-passed"):
                self._toggle_passed()
            elif self.path.startswith("/api/problems/") and self.path.endswith("/submission"):
                self._write_submission()
            elif self.path.startswith("/api/problems/") and self.path.endswith("/reflection"):
                self._write_reflection()
            elif self.path.startswith("/api/problems/") and self.path.endswith("/main-py"):
                self._write_main_py()
            else:
                self._send_json({"error": "not found"}, 404)
        except FileNotFoundError as e:
            self._send_json({"error": f"problem not found: {e}"}, 404)
        except ValueError as e:
            self._send_json({"error": str(e)}, 400)

    def _create_problem(self):
        data = self._read_json()
        problem_id = str(data.get("id", "")).strip()
        name = str(data.get("name", "")).strip()
        learning_log = bool(data.get("learning_log"))
        if not re.fullmatch(r"\d{4}", problem_id):
            raise ValueError("id must be 4 digits")
        if not name:
            raise ValueError("name required")
        slug = slugify_name(name)
        folder_name = f"oj_{problem_id}-{slug}"
        if learning_log:
            folder_name = f"[LEARNING-LOGS]-{folder_name}"
        path = OJ_DIR / folder_name
        if path.exists():
            raise ValueError("problem folder already exists")
        path.mkdir(parents=True)
        if data.get("with_main_py"):
            (path / "main.py").write_text(MAIN_PY_TEMPLATE, encoding="utf-8")
        self._send_json({"folder": folder_name})

    def _toggle_passed(self):
        folder, path = self._folder_from_path("/api/problems/")
        m = FOLDER_RE.match(path.name)
        if not m:
            raise ValueError("unrecognized folder name")
        passed = bool(m.group(3))
        base = path.name[: m.start(3)] if passed else path.name
        new_name = base if passed else f"{base} ✅"
        new_path = OJ_DIR / new_name
        path.rename(new_path)
        self._send_json({"folder": new_name, "passed": not passed})

    def _write_submission(self):
        folder, path = self._folder_from_path("/api/problems/")
        data = self._read_json()
        content = build_submission_md(data)
        (path / "submission.md").write_text(content, encoding="utf-8")
        self._send_json({"ok": True})

    def _write_reflection(self):
        folder, path = self._folder_from_path("/api/problems/")
        data = self._read_json()
        content = build_reflection_md(data)
        (path / "ai_reflection.md").write_text(content, encoding="utf-8")
        self._send_json({"ok": True})

    def _write_main_py(self):
        folder, path = self._folder_from_path("/api/problems/")
        main_py = path / "main.py"
        if not main_py.exists():
            main_py.write_text(MAIN_PY_TEMPLATE, encoding="utf-8")
        self._send_json({"ok": True})


def main():
    server = ThreadingHTTPServer(("localhost", 5050), Handler)
    print("PSCP Submission Helper running at http://localhost:5050")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
