"""ACI-007 PA validation — runs all scenario checks and prints a summary."""

import importlib.util
import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_APP_DIR = _ROOT / "app"
_DATA_DIR = _ROOT / "data"

if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance

PROMPTS_BACKUP = (_DATA_DIR / "prompts.json").read_text(encoding="utf-8")
RECORDS_BACKUP = (_DATA_DIR / "maintenance_records.json").read_text(encoding="utf-8")
NODES_BACKUP = (_DATA_DIR / "nodes.json").read_text(encoding="utf-8")

RESULTS = []


def record(scenario, check, passed):
    RESULTS.append({"scenario": scenario, "check": check, "passed": passed})
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {check}")


def load_app():
    spec = importlib.util.spec_from_file_location("app_module", _ROOT / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app.test_client()


def restore_data():
    (_DATA_DIR / "prompts.json").write_text(PROMPTS_BACKUP, encoding="utf-8")
    (_DATA_DIR / "maintenance_records.json").write_text(RECORDS_BACKUP, encoding="utf-8")
    (_DATA_DIR / "nodes.json").write_text(NODES_BACKUP, encoding="utf-8")


try:
    maintenance.save_maintenance_records([])
    client = load_app()

    print("Scenario 1: Node Visibility")
    dash = client.get("/")
    html = dash.get_data(as_text=True)
    nodes = maintenance.prepare_nodes_for_display()
    record("1", "Dashboard loads", dash.status_code == 200)
    record("1", "All 7 nodes visible", html.count("<tr>") == 8)
    record("1", "Node roles displayed", all(n["node_role"] in html for n in nodes))
    record("1", "Maintenance status displayed", "status-current" in html or "status-due" in html or "status-overdue" in html)
    record("1", "Days since maintenance displayed", all(str(n["days_since"]) in html for n in nodes if n["days_since"] is not None))

    print("\nScenario 2: Maintenance Execution")
    maint = client.get("/maintenance/OG")
    maint_html = maint.get_data(as_text=True)
    record("2", "Node selectable via Perform Maintenance", "Perform Maintenance" in client.get("/").get_data(as_text=True))
    record("2", "Maintenance page loads", maint.status_code == 200)
    record("2", "Maintenance prompt displayed", "Maintenance Prompt" in maint_html)
    record("2", "Restore prompt displayed", "Restore Prompt" in maint_html)
    record("2", "Complete maintenance action available", "Mark Maintenance Complete" in maint_html)

    print("\nScenario 3: Maintenance Recording")
    before = maintenance.prepare_node_for_display("Spectrum")
    complete = client.post("/maintenance/Spectrum/complete")
    after = maintenance.prepare_node_for_display("Spectrum")
    records = maintenance.load_maintenance_records()
    today = date.today().strftime("%Y-%m-%d")
    record("3", "Maintenance completion succeeds", complete.status_code == 302)
    record("3", "Maintenance record created", len(records) >= 1 and records[-1]["node"] == "Spectrum")
    record("3", "Record has required fields", all(k in records[-1] for k in ["date", "node", "activity_type", "notes", "backup_filename"]))
    record("3", "Node maintenance date updated", after["last_maintenance_date"] == today)
    record("3", "Status recalculated", after["status"] == maintenance.STATUS_CURRENT)

    print("\nScenario 4: Maintenance History")
    maintenance.save_maintenance_records([
        {"date": "2026-06-09", "node": "OG", "activity_type": "Backup Export", "notes": "", "backup_filename": ""},
        {"date": "2026-06-05", "node": "Clooney", "activity_type": "Backup Export", "notes": "", "backup_filename": ""},
    ])
    all_rec = client.get("/records")
    node_rec = client.get("/maintenance/OG/history")
    record("4", "All records page loads", all_rec.status_code == 200)
    record("4", "All records displayed", "OG" in all_rec.get_data(as_text=True) and "Clooney" in all_rec.get_data(as_text=True))
    record("4", "Node-specific history loads", node_rec.status_code == 200)
    record("4", "Node filter works", "OG" in node_rec.get_data(as_text=True) and "Clooney" not in node_rec.get_data(as_text=True))

    print("\nScenario 5: Prompt Management")
    prompts_page = client.get("/prompts")
    edit_page = client.get("/prompts/OG2")
    save = client.post("/prompts/OG2", data={
        "maintenance_prompt": "PA validation maintenance prompt.",
        "restore_prompt": "PA validation restore prompt.",
    })
    saved = maintenance.get_prompts_for_node("OG2")
    maint_after = client.get("/maintenance/OG2")
    maint_after_html = maint_after.get_data(as_text=True)
    record("5", "Prompt management page loads", prompts_page.status_code == 200)
    record("5", "Create maintenance prompt", saved and saved.get("maintenance_prompt") == "PA validation maintenance prompt.")
    record("5", "Create restore prompt", saved and saved.get("restore_prompt") == "PA validation restore prompt.")
    record("5", "Edit prompt page loads", edit_page.status_code == 200)
    edit_save = client.post("/prompts/OG", data={
        "maintenance_prompt": "Edited maintenance prompt.",
        "restore_prompt": "Edited restore prompt.",
    })
    edited = maintenance.get_prompts_for_node("OG")
    record("5", "Edit maintenance prompt", edited["maintenance_prompt"] == "Edited maintenance prompt.")
    record("5", "Edit restore prompt", edited["restore_prompt"] == "Edited restore prompt.")
    record("5", "Maintenance page shows saved prompts", "PA validation maintenance prompt." in maint_after_html)

    print("\nScenario 6: Restart Validation")
    spec = importlib.util.spec_from_file_location("app_restart", _ROOT / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    record("6", "Application module loads", mod.app is not None)
    record("6", "Startup node data loaded", len(mod.nodes) == 7)
    record("6", "Home route responds after reload", mod.app.test_client().get("/").status_code == 200)

finally:
    restore_data()

print("\n" + "=" * 50)
passed = sum(1 for r in RESULTS if r["passed"])
failed = sum(1 for r in RESULTS if not r["passed"])
print(f"TOTAL: {passed} passed, {failed} failed out of {len(RESULTS)} checks")
print("PA INTENT: YES" if failed == 0 else "PA INTENT: NO")
sys.exit(0 if failed == 0 else 1)
