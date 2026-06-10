import json
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
NODES_FILE = DATA_DIR / "nodes.json"
RECORDS_FILE = DATA_DIR / "maintenance_records.json"
PROMPTS_FILE = DATA_DIR / "prompts.json"

DEFAULT_ACTIVITY_TYPE = "Backup Export"
NO_PROMPT_MESSAGE = "No maintenance prompt configured."
NO_RECORDS_MESSAGE = "No maintenance records found."

STATUS_CURRENT = "Current"
STATUS_DUE = "Due"
STATUS_OVERDUE = "Overdue"


def load_nodes():
    with open(NODES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_nodes(nodes):
    with open(NODES_FILE, "w", encoding="utf-8") as f:
        json.dump(nodes, f, indent=2)
        f.write("\n")


def days_since_maintenance(last_maintenance_date, reference_date=None):
    if not last_maintenance_date:
        return None

    if isinstance(last_maintenance_date, str):
        last_date = datetime.strptime(last_maintenance_date, "%Y-%m-%d").date()
    else:
        last_date = last_maintenance_date

    today = reference_date or date.today()
    return (today - last_date).days


def calculate_status(last_maintenance_date, reference_date=None):
    days = days_since_maintenance(last_maintenance_date, reference_date)

    if days is None:
        return STATUS_OVERDUE
    if days <= 6:
        return STATUS_CURRENT
    if days <= 13:
        return STATUS_DUE
    return STATUS_OVERDUE


def apply_status_to_nodes(nodes, reference_date=None):
    for node in nodes:
        node["status"] = calculate_status(
            node.get("last_maintenance_date"), reference_date
        )
    return nodes


def prepare_nodes_for_display(nodes=None, reference_date=None):
    if nodes is None:
        nodes = load_nodes()
    nodes = apply_status_to_nodes(nodes, reference_date)
    for node in nodes:
        node["days_since"] = days_since_maintenance(
            node.get("last_maintenance_date"), reference_date
        )
    return nodes


def load_maintenance_records():
    with open(RECORDS_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_maintenance_records(node_name=None):
    records = load_maintenance_records()
    if node_name:
        records = [record for record in records if record.get("node") == node_name]
    return sorted(records, key=lambda record: record.get("date", ""), reverse=True)


def save_maintenance_records(records):
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
        f.write("\n")


def load_prompts():
    with open(PROMPTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_prompts(prompts):
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2)
        f.write("\n")


def save_prompts_for_node(node_name, maintenance_prompt, restore_prompt):
    prompts = load_prompts()
    entry = None
    for prompt in prompts:
        if prompt.get("node_name") == node_name:
            entry = prompt
            break

    if entry is None:
        entry = {"node_name": node_name}
        prompts.append(entry)

    entry["maintenance_prompt"] = maintenance_prompt.strip()
    entry["restore_prompt"] = restore_prompt.strip()
    save_prompts(prompts)
    return entry


def get_node_by_name(node_name):
    for node in load_nodes():
        if node["node_name"] == node_name:
            return dict(node)
    return None


def get_prompts_for_node(node_name):
    for prompt in load_prompts():
        if prompt.get("node_name") == node_name:
            return prompt
    return None


def get_prompt_text(prompt_entry, field_name):
    if not prompt_entry:
        return NO_PROMPT_MESSAGE
    value = prompt_entry.get(field_name)
    if not value:
        return NO_PROMPT_MESSAGE
    return value


def prepare_node_for_display(node_name, reference_date=None):
    node = get_node_by_name(node_name)
    if node is None:
        return None

    node["status"] = calculate_status(
        node.get("last_maintenance_date"), reference_date
    )
    node["days_since"] = days_since_maintenance(
        node.get("last_maintenance_date"), reference_date
    )
    return node


def complete_maintenance(node_name, reference_date=None):
    node = get_node_by_name(node_name)
    if node is None:
        return None

    today = reference_date or date.today()
    today_str = today.strftime("%Y-%m-%d")

    record = {
        "date": today_str,
        "node": node_name,
        "activity_type": DEFAULT_ACTIVITY_TYPE,
        "notes": "",
        "backup_filename": "",
    }

    records = load_maintenance_records()
    records.append(record)
    save_maintenance_records(records)

    nodes = load_nodes()
    for stored_node in nodes:
        if stored_node["node_name"] == node_name:
            stored_node["last_maintenance_date"] = today_str
            break
    save_nodes(nodes)

    return record
