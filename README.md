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

## Docker

**Docker Hub target:** `taig2k/nebula_maint_app`

Image tag: `taig2k/nebula_maint_app:v0.1`

### GitHub Actions Build

Docker images are built by GitHub Actions — not locally. The workflow is defined in `.github/workflows/docker-build.yml`.

**Triggers:**
- Push to the `deployable` branch
- Manual `workflow_dispatch`

**Build steps:** checkout → Docker Buildx → build image → tag `taig2k/nebula_maint_app:v0.1`

### Required Secrets

Configure these repository secrets in GitHub (**Settings → Secrets and variables → Actions**) to enable push to Docker Hub:

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Docker Hub username (`taig2k`) |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

If secrets are not configured, the workflow still builds the image but does not push.

### Run from Docker Hub

Once pushed:

```bash
docker pull taig2k/nebula_maint_app:v0.1
docker run -d --name nebula_maint_app -p 5000:5000 taig2k/nebula_maint_app:v0.1
```

Open http://127.0.0.1:5000/

### PA Condition

PA is achieved when the image exists in Docker Hub and can be pulled and run successfully.
