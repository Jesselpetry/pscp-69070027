"""ijudge.config: titles, categories, weeks and folder names."""

from __future__ import annotations

import json
import os
import unittest
from datetime import date, timedelta

from ijudge import config, paths


def load_summary() -> list[dict]:
    with open(paths.SUMMARY_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


class SplitTitleTest(unittest.TestCase):
    def test_tags_are_separated_and_uppercased(self):
        self.assertEqual(
            config.split_title("[Recommend] [LEARNING LOGS] Temperature"),
            ("Temperature", ["RECOMMEND", "LEARNING LOGS"]),
        )

    def test_padded_tag_and_whitespace_runs(self):
        self.assertEqual(
            config.split_title("[ MINI EXAM ] Count All  Vowel "),
            ("Count All Vowel", ["MINI EXAM"]),
        )

    def test_plain_and_empty(self):
        self.assertEqual(config.split_title("Left Arrow"), ("Left Arrow", []))
        self.assertEqual(config.split_title(None), ("", []))
        self.assertEqual(config.clean_title("[ MIDTERM ] Pizza Time"), "Pizza Time")

    def test_title_that_is_only_tags_keeps_raw_text(self):
        self.assertEqual(config.split_title("[MIDTERM]"), ("[MIDTERM]", ["MIDTERM"]))


class HasCategoryTest(unittest.TestCase):
    def test_tag_prefix_matches(self):
        self.assertTrue(config.has_category("[LEARNING LOGS] Point Sorting", "learning_log"))
        self.assertTrue(config.has_category("[Recommend] Temperature", "recommended"))
        self.assertTrue(config.has_category("[ MIDTERM ] Stats", "midterm"))
        self.assertTrue(config.has_category("[ MINI EXAM ] Longer", "mini_exam"))
        self.assertTrue(config.has_category("[MINI EXAM] Longer", "mini_exam"))

    def test_no_tag_or_other_tag(self):
        self.assertFalse(config.has_category("Learning Log Point Sorting", "learning_log"))
        self.assertFalse(config.has_category("[Recommend] Temperature", "mini_exam"))
        self.assertFalse(config.has_category(None, "midterm"))


class WeekForReleaseTest(unittest.TestCase):
    def setUp(self):
        self.dated = sorted(
            (date.fromisoformat(w["from"]), int(w["week"]))
            for w in config.load_course()["weeks"]
            if w.get("from")
        )

    def test_window_edges(self):
        for (start, week), (next_start, _) in zip(self.dated, self.dated[1:]):
            with self.subTest(week=week):
                self.assertEqual(config.week_for_release(start), week)
                self.assertEqual(config.week_for_release(next_start - timedelta(days=1)), week)
                self.assertNotEqual(config.week_for_release(next_start), week)

    def test_before_first_window(self):
        first = self.dated[0][0]
        self.assertIsNone(config.week_for_release(first - timedelta(days=1)))

    def test_last_window_is_seven_days_then_none(self):
        start, week = self.dated[-1]
        self.assertEqual(config.week_for_release(start + timedelta(days=6)), week)
        self.assertIsNone(config.week_for_release(start + timedelta(days=7)))

    def test_none(self):
        self.assertIsNone(config.week_for_release(None))

    def test_release_date_uses_course_timezone(self):
        # 17:00Z on the day before week 2 is already week 2 at UTC+7.
        self.assertEqual(config.release_date("2026-07-09T17:00:00.000Z"), date(2026, 7, 10))
        self.assertEqual(config.release_date("2026-07-09T16:59:59Z"), date(2026, 7, 9))
        self.assertIsNone(config.release_date("not a date"))


class GetWeekTest(unittest.TestCase):
    def test_matches_stored_week_for_every_summary_record(self):
        records = load_summary()
        self.assertGreater(len(records), 0)
        for p in records:
            with self.subTest(pid=p["id"]):
                self.assertEqual(
                    config.get_week(p["id"], p.get("name"), p.get("released"), fallback=p.get("week")),
                    p["week"],
                )

    def test_override_and_category_win(self):
        self.assertEqual(config.get_week(2981, "สวัสดี: ชื่อ", None), 1)
        self.assertEqual(config.get_week(1, "[MINI EXAM] X", "2026-07-03T05:00:00Z"), 14)

    def test_fallback_when_nothing_matches(self):
        self.assertEqual(config.get_week(1, "X", None, fallback=5), 5)


class FolderNameTest(unittest.TestCase):
    def test_reproduces_existing_oj_folders(self):
        names = {p["id"]: p["name"] for p in load_summary()}
        folders = [d for d in sorted(os.listdir(paths.OJ_DIR)) if paths.problem_id_of(d)]
        self.assertGreater(len(folders), 0)
        for d in folders:
            pid = paths.problem_id_of(d)
            with self.subTest(folder=d):
                self.assertIn(pid, names)
                self.assertEqual(config.folder_name(pid, names[pid]), d.removesuffix(" ✅"))

    def test_slug_and_thai_fallback(self):
        self.assertEqual(config.folder_name(999001, "[MINI EXAM] Longer"), "oj999001-MINI_EXAM_Longer")
        self.assertEqual(config.folder_name(999002, "ปราสาท"), "oj999002")


class MidtermTargetTest(unittest.TestCase):
    def test_map(self):
        self.assertEqual(config.midterm_target(3138), 3276)
        self.assertEqual(config.midterm_target(3148), 3277)
        self.assertIsNone(config.midterm_target(3290))


if __name__ == "__main__":
    unittest.main()
