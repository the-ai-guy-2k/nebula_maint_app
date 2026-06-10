import importlib.util
import sys
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent / "app"
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance

spec = importlib.util.spec_from_file_location(
    "app_module", Path(__file__).resolve().parent.parent / "app.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

client = mod.app.test_client()
resp = client.get("/")
assert resp.status_code == 200
html = resp.get_data(as_text=True)

expected = {n["node_name"]: n for n in maintenance.prepare_nodes_for_display()}
node_names = ["OG", "OG2", "Cyka", "Clooney", "Clooney2", "Clooney3", "Spectrum"]

for name in node_names:
    assert name in html, f"Missing node: {name}"
    node = expected[name]
    assert node["status"] in html
    assert f"status-{node['status'].lower()}" in html
    assert str(node["days_since"]) in html
    assert node["last_maintenance_date"] in html

assert "Dashboard" in html
assert "Maintenance Records" in html
assert html.count("<tr>") == 8

print("Dashboard loads: OK")
print("All 7 nodes display: OK")
print("Statuses match calculated values:")
for name in node_names:
    n = expected[name]
    print(f"  {name}: {n['status']} ({n['days_since']} days)")
print("No startup errors: OK")
