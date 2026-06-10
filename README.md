# Nebula Maintenance App

Flask MVP for tracking maintenance across Nebula nodes.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser.

## Project Structure

```
app/
  templates/    # HTML templates
  static/       # CSS, JS, images
data/
  nodes.json                  # Node definitions
  maintenance_records.json    # Maintenance history
  prompts.json                # Prompt templates
docs/                         # Documentation
app.py                        # Flask entry point
```

## Data Storage

Data is stored in JSON files under `data/`. No database is used in this MVP.
