import sys
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

_APP_DIR = Path(__file__).resolve().parent / "app"
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import maintenance

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

nodes = maintenance.prepare_nodes_for_display()


@app.route("/")
def home():
    dashboard_nodes = maintenance.prepare_nodes_for_display()
    return render_template("home.html", nodes=dashboard_nodes)


@app.route("/maintenance/<node_name>")
def maintenance_page(node_name):
    node = maintenance.prepare_node_for_display(node_name)
    if node is None:
        abort(404)

    prompt_entry = maintenance.get_prompts_for_node(node_name)
    return render_template(
        "maintenance.html",
        node=node,
        maintenance_prompt=maintenance.get_prompt_text(
            prompt_entry, "maintenance_prompt"
        ),
        restore_prompt=maintenance.get_prompt_text(prompt_entry, "restore_prompt"),
    )


@app.route("/maintenance/<node_name>/complete", methods=["POST"])
def complete_maintenance(node_name):
    if maintenance.get_node_by_name(node_name) is None:
        abort(404)

    maintenance.complete_maintenance(node_name)
    return redirect(url_for("home"))


@app.route("/records")
def maintenance_records():
    records = maintenance.get_maintenance_records()
    return render_template("records.html", records=records, node_name=None)


@app.route("/maintenance/<node_name>/history")
def node_maintenance_history(node_name):
    if maintenance.get_node_by_name(node_name) is None:
        abort(404)

    records = maintenance.get_maintenance_records(node_name)
    return render_template("records.html", records=records, node_name=node_name)


@app.route("/prompts")
def prompt_management():
    nodes = maintenance.load_nodes()
    return render_template("prompts.html", nodes=nodes)


@app.route("/prompts/<node_name>", methods=["GET", "POST"])
def edit_prompts(node_name):
    node = maintenance.get_node_by_name(node_name)
    if node is None:
        abort(404)

    if request.method == "POST":
        maintenance.save_prompts_for_node(
            node_name,
            request.form.get("maintenance_prompt", ""),
            request.form.get("restore_prompt", ""),
        )
        return redirect(url_for("prompt_management"))

    prompt_entry = maintenance.get_prompts_for_node(node_name) or {}
    return render_template(
        "edit_prompt.html", node=node, prompt_entry=prompt_entry
    )


if __name__ == "__main__":
    app.run(debug=True)
