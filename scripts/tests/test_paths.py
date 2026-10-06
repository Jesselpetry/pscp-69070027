"""ijudge.paths: folder-name parsing and the problem-folder index."""

from __future__ import annotations

import json
import os
import unittest

from ijudge import paths


class ProblemIdOfTest(unittest.TestCase):
    def test_folder_shapes(self):
        self.assertEqual(paths.problem_id_of("oj3381"), 3381)
        self.assertEqual(paths.problem_id_of("oj3290-Left_Arrow"), 3290)
        self.assertEqual(paths.problem_id_of("oj3290-Left_Arrow ✅"), 3290)
        self.assertEqual(paths.problem_id_of("oj3594-1132-Median"), 3594)

    def test_not_problem_folders(self):
        for name in ("README.md", "recommended", "oj", "ojx12", "oj12ab", "xoj3290"):
            with self.subTest(name=name):
                self.assertIsNone(paths.problem_id_of(name))


class IndexProblemDirsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = paths.index_problem_dirs()
        with open(paths.SUMMARY_JSON, "r", encoding="utf-8") as f:
            cls.registry_ids = [p["id"] for p in json.load(f)]

    def test_covers_every_registry_id(self):
        missing = [pid for pid in self.registry_ids if pid not in self.index]
        self.assertEqual(missing, [])

    def test_folders_exist_and_match_their_id(self):
        for pid, folder in self.index.items():
            with self.subTest(pid=pid):
                self.assertTrue(os.path.isdir(folder))
                self.assertEqual(paths.problem_id_of(os.path.basename(folder)), pid)

    def test_learning_logs_resolve_to_root_folders(self):
        roots = [d for d in os.listdir(paths.MAIN_ROOT) if d[:2] == "oj" and d[2:].isdigit()]
        self.assertGreater(len(roots), 0)
        for d in roots:
            with self.subTest(folder=d):
                self.assertEqual(self.index[int(d[2:])], os.path.join(paths.MAIN_ROOT, d))

    def test_find_problem_dir(self):
        self.assertEqual(paths.find_problem_dir(self.registry_ids[0]), self.index[self.registry_ids[0]])
        self.assertIsNone(paths.find_problem_dir(1))


if __name__ == "__main__":
    unittest.main()
