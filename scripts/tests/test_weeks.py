"""ijudge.weeks: date formatting and registry week lookup."""

from __future__ import annotations

import unittest

from ijudge import weeks


class FormatExpireDateTest(unittest.TestCase):
    def test_iso_timestamp(self):
        self.assertEqual(weeks.format_expire_date("2026-09-04T23:59:00.000Z"), "4 September 2026, 23:59")
        self.assertEqual(weeks.format_expire_date("2027-10-24T23:59:59Z"), "24 October 2027, 23:59")
        self.assertEqual(weeks.format_expire_date("2026-07-31T00:00"), "31 July 2026, 00:00")

    def test_empty_and_unparsable(self):
        self.assertEqual(weeks.format_expire_date(""), "")
        self.assertEqual(weeks.format_expire_date(None), "")
        self.assertEqual(weeks.format_expire_date("soon"), "soon")


class RegistryWeekTest(unittest.TestCase):
    def test_release_of_both_shapes(self):
        self.assertEqual(weeks.release_of({"released": "a"}), "a")
        self.assertEqual(weeks.release_of({"courseProblem": {"cp_release_time": "b"}}), "b")
        self.assertIsNone(weeks.release_of({}))

    def test_get_week_keeps_stored_week_without_release(self):
        self.assertEqual(weeks.get_week({"id": 1, "name": "X", "week": 9}), 9)


if __name__ == "__main__":
    unittest.main()
