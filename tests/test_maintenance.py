import sys
import unittest
from datetime import date
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent / "app"
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance


REFERENCE_DATE = date(2026, 6, 10)


class TestDaysSinceMaintenance(unittest.TestCase):
    def test_returns_days_since_date(self):
        self.assertEqual(
            maintenance.days_since_maintenance("2026-06-08", REFERENCE_DATE), 2
        )

    def test_returns_none_when_date_missing(self):
        self.assertIsNone(maintenance.days_since_maintenance(None, REFERENCE_DATE))


class TestCalculateStatus(unittest.TestCase):
    def test_current_at_zero_days(self):
        self.assertEqual(
            maintenance.calculate_status("2026-06-10", REFERENCE_DATE),
            maintenance.STATUS_CURRENT,
        )

    def test_current_at_six_days(self):
        self.assertEqual(
            maintenance.calculate_status("2026-06-04", REFERENCE_DATE),
            maintenance.STATUS_CURRENT,
        )

    def test_due_at_seven_days(self):
        self.assertEqual(
            maintenance.calculate_status("2026-06-03", REFERENCE_DATE),
            maintenance.STATUS_DUE,
        )

    def test_due_at_thirteen_days(self):
        self.assertEqual(
            maintenance.calculate_status("2026-05-28", REFERENCE_DATE),
            maintenance.STATUS_DUE,
        )

    def test_overdue_at_fourteen_days(self):
        self.assertEqual(
            maintenance.calculate_status("2026-05-27", REFERENCE_DATE),
            maintenance.STATUS_OVERDUE,
        )

    def test_overdue_when_date_missing(self):
        self.assertEqual(
            maintenance.calculate_status(None, REFERENCE_DATE),
            maintenance.STATUS_OVERDUE,
        )


class TestNodeDataValidation(unittest.TestCase):
    def test_seed_nodes_have_expected_statuses(self):
        nodes = maintenance.apply_status_to_nodes(
            maintenance.load_nodes(), REFERENCE_DATE
        )
        statuses = {node["node_name"]: node["status"] for node in nodes}

        self.assertEqual(statuses["OG"], maintenance.STATUS_CURRENT)
        self.assertEqual(statuses["OG2"], maintenance.STATUS_DUE)
        self.assertEqual(statuses["Cyka"], maintenance.STATUS_OVERDUE)

    def test_seed_nodes_have_required_fields(self):
        nodes = maintenance.load_nodes()
        required_fields = {
            "node_name",
            "node_role",
            "last_maintenance_date",
            "status",
        }

        for node in nodes:
            self.assertTrue(required_fields.issubset(node.keys()))

    def test_seed_roles_are_correct(self):
        nodes = maintenance.load_nodes()
        roles = {node["node_name"]: node["node_role"] for node in nodes}

        self.assertEqual(roles["OG"], "Governance")
        self.assertEqual(roles["OG2"], "Governance")
        self.assertEqual(roles["Cyka"], "Band Manager")
        self.assertEqual(roles["Clooney"], "DevOps")
        self.assertEqual(roles["Clooney2"], "DevOps")
        self.assertEqual(roles["Clooney3"], "DevOps")
        self.assertEqual(roles["Spectrum"], "Research")


if __name__ == "__main__":
    unittest.main()
