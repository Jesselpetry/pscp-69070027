"""The main.py template, and telling an untouched stub from real code.

Every script that creates, archives or reports on main.py files uses these,
so "is this solved?" has exactly one answer across the toolchain.
"""

from __future__ import annotations

import ast

STUB_MARKER = "# solution code here"


def stub_solution(title: str) -> str:
    """Fresh main.py for a problem nobody has started yet."""
    return "\n".join([
        f'""" {title} """',
        "",
        "",
        "def main():",
        f'    """{title}"""',
        f"    {STUB_MARKER}",
        "",
        "",
        'if __name__ == "__main__":',
        "    main()",
        "",
    ])


def _is_docstring(node: ast.stmt) -> bool:
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _is_trivial(node: ast.stmt) -> bool:
    if isinstance(node, ast.Pass) or _is_docstring(node):
        return True
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis
    )


def _is_main_guard(node: ast.stmt) -> bool:
    test = getattr(node, "test", None)
    return (
        isinstance(node, ast.If)
        and isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
    )


def is_stub(code: str) -> bool:
    """True if `code` is an untouched template, safe to overwrite or skip.

    Judged on the AST, so STUB_MARKER (a comment) is irrelevant: the current
    template and the older docstring-only one both qualify, while code written
    under a leftover marker does not. Anything that does not parse counts as
    real work: a half-written solution must never be treated as empty.
    """
    if not code.strip():
        return True
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for node in tree.body:
        if _is_docstring(node) or _is_main_guard(node):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            if all(_is_trivial(stmt) for stmt in node.body):
                continue
        return False
    return True
