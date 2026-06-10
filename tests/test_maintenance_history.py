import importlib.util
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_APP_DIR = _ROOT / "app"
_DATA_DIR = _ROOT / "data"

if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance

SAMPLE_RECORDS = [
    {
        "date": "2026-06-09",
        "node": "Clooney2",
        "activity_type": "Backup Export",
        "notes": "",
        "backup_filename": "",
    },
    {
        "date": "2026-06-08",
        "node": "OG",
        "activity_type": "Backup Export",
        "notes": "",
        "backup_filename": "",
    },
    {
        "date": "2026-06-05",
        "node": "OG",
        "activity_type": "Backup Export",
        "notes": "",
        "backup_filename": "",
    },
]


def load_app_module():
    spec = importlib.util.spec_from_file_location("app_module", _ROOT / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestMaintenanceHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records_backup = (_DATA_DIR / "maintenance_records.json").read_text(
            encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        (_DATA_DIR / "maintenance_records.json").write_text(
            cls.records_backup, encoding="utf-8"
        )

    def setUp(self):
        maintenance.save_maintenance_records(SAMPLE_RECORDS)

    def test_records_sorted_newest_first(self):
        records = maintenance.get_maintenance_records()
        self.assertEqual([record["date"] for record in records], [
            "2026-06-09",
            "2026-06-08",
            "2026-06-05",
        ])

    def test_node_filter_returns_only_matching_records(self):
        records = maintenance.get_maintenance_records("OG")
        self.assertEqual(len(records), 2)
        self.assertTrue(all(record["node"] == "OG" for record in records))
        self.assertEqual(records[0]["date"], "2026-06-08")

    def test_all_records_page_loads(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/records")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("Maintenance Records", html)
        self.assertIn("2026-06-09", html)
        self.assertIn("Clooney2", html)
        self.assertIn("Backup Export", html)

    def test_node_history_page_loads_and_filters(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/maintenance/OG/history")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("OG Maintenance History", html)
        self.assertIn("2026-06-08", html)
        self.assertIn("2026-06-05", html)
        self.assertNotIn("Clooney2", html)

    def test_empty_state_when_no_records(self):
        maintenance.save_maintenance_records([])
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/records")

        self.assertEqual(resp.status_code, 200)
        self.assertIn(maintenance.NO_RECORDS_MESSAGE, resp.get_data(as_text=True))

    def test_maintenance_page_links_to_view_history(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/maintenance/OG")

        self.assertEqual(resp.status_code, 200)
        self.assertIn("View History", resp.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
