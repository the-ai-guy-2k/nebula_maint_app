# ACI-PE-003: Destroy AWS EC2 Published Environment

**Project:** Nebula Maintenance App  
**Branch:** `feature/pe-aws-ec2`  
**Date:** 2026-06-11  
**Status:** In progress

---

## Objective

Safely shut down and destroy the Maintenance App AWS Published Environment using Terraform through GitHub Actions.

---

## Current Truth (Pre-Destroy)

- PE exists on AWS EC2 in `us-east-1`
- App reachable at http://98.82.24.178:5000
- EC2 instance: `i-0ca9f5f81a35f9fff`
- Terraform created the environment (ACI-PE-002)
- Docker image `taig2k/nebula_maint_app:v0.1` published and preserved
- PA achieved; GitHub repo preserved

---

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Create `.github/workflows/terraform-destroy-pe.yml` | Complete |
| 2 | Workflow: `workflow_dispatch`, AWS secrets, init, plan -destroy, destroy | Complete |
| 3 | Safety: destroy PE only; preserve Docker Hub, repo, PA | Complete |
| 4 | Create `docs/pe/PE_DESTROY_REPORT.md` | Complete |
| 5 | Save ACI artifact (this file) | Complete |
| 6 | Commit and push: "Add PE destroy workflow" | Pending |
| 7 | Run destroy workflow manually | Pending |
| 8 | Validate destroy and update reports | Pending |

---

## Workflow Design

**File:** `.github/workflows/terraform-destroy-pe.yml`

- Trigger: `workflow_dispatch` only
- Region: `us-east-1` (hardcoded)
- Steps: verify secrets → configure AWS → terraform init → import PE state if empty → plan -destroy → destroy -auto-approve
- State recovery: imports `nebula-maint-app-pe-*` resources when CI state is ephemeral

---

## Safety Rules

- Do not destroy Docker Hub image
- Do not delete GitHub repository
- Do not delete PA artifact
- Do not merge branch to `deployable`
- Do not manually delete AWS resources unless Terraform destroy fails

---

## Stop Point

Maintenance App PE destroyed safely through Terraform with evidence recorded in `docs/pe/PE_DESTROY_REPORT.md`.

---

## References

- Deploy report: `docs/pe/PE_DEPLOYMENT_REPORT.md`
- Destroy report: `docs/pe/PE_DESTROY_REPORT.md`
- Deploy workflow: `.github/workflows/terraform-pe.yml`
- Destroy workflow: `.github/workflows/terraform-destroy-pe.yml`
