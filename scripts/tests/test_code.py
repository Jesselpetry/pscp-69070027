"""ijudge.code: the main.py template and stub detection."""

from __future__ import annotations

import os
import unittest

from ijudge import code, paths


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class IsStubTest(unittest.TestCase):
    def test_current_template(self):
        stub = code.stub_solution("Left Arrow")
        self.assertIn(code.STUB_MARKER, stub)
        self.assertTrue(code.is_stub(stub))
        compile(stub, "<stub>", "exec")

    def test_old_docstring_only_template(self):
        path = os.path.join(paths.MAIN_ROOT, "oj3036", "main.py")
        if not os.path.isfile(path):
            self.skipTest("oj3036/main.py not present on main")
        src = read(path)
        self.assertNotIn(code.STUB_MARKER, src)
        self.assertTrue(code.is_stub(src))

    def test_real_solution(self):
        folder = paths.find_problem_dir(3290)
        self.assertIsNotNone(folder)
        self.assertFalse(code.is_stub(read(os.path.join(folder, "main.py"))))
        self.assertFalse(code.is_stub('def main():\n    print(input())\n\n\nmain()\n'))

    def test_unparsable_code_counts_as_work(self):
        self.assertFalse(code.is_stub("def main(:\n    print('half done'\n"))

    def test_blank_and_trivial_bodies(self):
        self.assertTrue(code.is_stub(""))
        self.assertTrue(code.is_stub('"""T"""\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n'))
        self.assertFalse(code.is_stub('import sys\n\ndef main():\n    pass\n'))


if __name__ == "__main__":
    unittest.main()
