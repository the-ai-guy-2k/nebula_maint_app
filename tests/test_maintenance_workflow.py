import importlib.util
import json
import shutil
import sys
import unittest
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_APP_DIR = _ROOT / "app"
_DATA_DIR = _ROOT / "data"

if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance

REFERENCE_DATE = date(2026, 6, 10)
TEST_NODE = "Spectrum"


def load_app_module():
    spec = importlib.util.spec_from_file_location("app_module", _ROOT / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestMaintenanceWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes_backup = (_DATA_DIR / "nodes.json").read_text(encoding="utf-8")
        cls.records_backup = (_DATA_DIR / "maintenance_records.json").read_text(
            encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        (_DATA_DIR / "nodes.json").write_text(cls.nodes_backup, encoding="utf-8")
        (_DATA_DIR / "maintenance_records.json").write_text(
            cls.records_backup, encoding="utf-8"
        )

    def tearDown(self):
        maintenance.save_maintenance_records([])

    def setUp(self):
        (_DATA_DIR / "nodes.json").write_text(self.nodes_backup, encoding="utf-8")
        maintenance.save_maintenance_records([])

    def test_maintenance_page_loads_with_prompts(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/maintenance/OG")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("OG", html)
        self.assertIn("Governance", html)
        self.assertIn("Export governance configuration backup", html)

    def test_maintenance_page_shows_missing_prompt_message(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/maintenance/OG2")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertEqual(
            html.count(maintenance.NO_PROMPT_MESSAGE), 2
        )

    def test_complete_maintenance_creates_record_and_updates_node(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()

        before_node = maintenance.prepare_node_for_display(
            TEST_NODE, REFERENCE_DATE
        )
        self.assertEqual(before_node["status"], maintenance.STATUS_OVERDUE)

        page_resp = client.get(f"/maintenance/{TEST_NODE}")
        self.assertEqual(page_resp.status_code, 200)
        self.assertIn("Mark Maintenance Complete", page_resp.get_data(as_text=True))

        complete_resp = client.post(f"/maintenance/{TEST_NODE}/complete")
        self.assertEqual(complete_resp.status_code, 302)

        today_str = date.today().strftime("%Y-%m-%d")
        records = maintenance.load_maintenance_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["node"], TEST_NODE)
        self.assertEqual(records[0]["activity_type"], "Backup Export")
        self.assertEqual(records[0]["notes"], "")
        self.assertEqual(records[0]["backup_filename"], "")
        self.assertEqual(records[0]["date"], today_str)

        updated_node = maintenance.prepare_node_for_display(TEST_NODE)
        self.assertEqual(updated_node["last_maintenance_date"], today_str)
        self.assertEqual(updated_node["status"], maintenance.STATUS_CURRENT)

    def test_dashboard_links_to_maintenance_page(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertEqual(html.count("Perform Maintenance"), 7)


if __name__ == "__main__":
    unittest.main()
