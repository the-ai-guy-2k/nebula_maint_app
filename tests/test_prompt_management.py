import importlib.util
import json
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_APP_DIR = _ROOT / "app"
_DATA_DIR = _ROOT / "data"

if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance

TEST_NODE = "OG2"
NEW_MAINTENANCE_PROMPT = "Updated governance maintenance checklist."
NEW_RESTORE_PROMPT = "Updated governance restore procedure."


def load_app_module():
    spec = importlib.util.spec_from_file_location("app_module", _ROOT / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPromptManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts_backup = (_DATA_DIR / "prompts.json").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        (_DATA_DIR / "prompts.json").write_text(cls.prompts_backup, encoding="utf-8")

    def setUp(self):
        (_DATA_DIR / "prompts.json").write_text(self.prompts_backup, encoding="utf-8")

    def test_prompt_management_page_loads(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/prompts")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("Prompt Management", html)
        self.assertIn("Edit Prompts", html)
        self.assertEqual(html.count("Edit Prompts"), 7)

    def test_edit_prompt_page_loads(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get("/prompts/OG")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("Maintenance Prompt", html)
        self.assertIn("Restore Prompt", html)
        self.assertIn("Export governance configuration backup", html)

    def test_save_new_prompts_for_node(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()

        resp = client.post(
            f"/prompts/{TEST_NODE}",
            data={
                "maintenance_prompt": NEW_MAINTENANCE_PROMPT,
                "restore_prompt": NEW_RESTORE_PROMPT,
            },
        )
        self.assertEqual(resp.status_code, 302)

        entry = maintenance.get_prompts_for_node(TEST_NODE)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["maintenance_prompt"], NEW_MAINTENANCE_PROMPT)
        self.assertEqual(entry["restore_prompt"], NEW_RESTORE_PROMPT)

    def test_edit_existing_prompts(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()

        updated_maintenance = "Revised OG maintenance steps."
        updated_restore = "Revised OG restore steps."

        resp = client.post(
            "/prompts/OG",
            data={
                "maintenance_prompt": updated_maintenance,
                "restore_prompt": updated_restore,
            },
        )
        self.assertEqual(resp.status_code, 302)

        entry = maintenance.get_prompts_for_node("OG")
        self.assertEqual(entry["maintenance_prompt"], updated_maintenance)
        self.assertEqual(entry["restore_prompt"], updated_restore)

    def test_maintenance_page_displays_saved_prompts(self):
        maintenance.save_prompts_for_node(
            TEST_NODE,
            NEW_MAINTENANCE_PROMPT,
            NEW_RESTORE_PROMPT,
        )

        app_mod = load_app_module()
        client = app_mod.app.test_client()
        resp = client.get(f"/maintenance/{TEST_NODE}")

        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn(NEW_MAINTENANCE_PROMPT, html)
        self.assertIn(NEW_RESTORE_PROMPT, html)

    def test_navigation_includes_prompt_management(self):
        app_mod = load_app_module()
        client = app_mod.app.test_client()

        for path in ["/", "/records", "/maintenance/OG", "/prompts"]:
            resp = client.get(path)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Prompt Management", resp.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
