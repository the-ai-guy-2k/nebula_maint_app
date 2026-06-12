# PE Destroy Report — Nebula Maintenance App

**ACI:** ACI-PE-003  
**Date/Time:** 2026-06-11 (pending destroy run)  
**Branch:** `feature/pe-aws-ec2` (not merged to `deployable`)  
**Destroy Status:** **PENDING — workflow not yet executed**

---

## Pre-Destroy State

| Field | Value |
|-------|-------|
| AWS Region | `us-east-1` |
| EC2 Public IP | `98.82.24.178` |
| App URL | http://98.82.24.178:5000 |
| EC2 Instance ID | `i-0ca9f5f81a35f9fff` |
| Docker Image | `taig2k/nebula_maint_app:v0.1` (preserved) |
| Workflow | `.github/workflows/terraform-destroy-pe.yml` |

---

## Terraform Resources (Expected Destroy Targets)

| Resource | Identifier |
|----------|------------|
| `aws_instance.app` | `nebula-maint-app-pe-ec2` |
| `aws_security_group.app` | `nebula-maint-app-pe-sg` |
| `aws_route_table_association.public` | Public subnet association |
| `aws_route_table.public` | `nebula-maint-app-pe-public-rt` |
| `aws_subnet.public` | `nebula-maint-app-pe-public-subnet` |
| `aws_internet_gateway.main` | `nebula-maint-app-pe-igw` |
| `aws_vpc.main` | `nebula-maint-app-pe-vpc` |

---

## Destroy Workflow Run

| Field | Value |
|-------|-------|
| Workflow Run | Pending |
| Commit | Pending |
| Terraform destroy result | Pending |

---

## Final Validation

| Check | Status |
|-------|--------|
| Terraform destroy succeeds | Pending |
| EC2 instance removed | Pending |
| App URL no longer responds | Pending |
| PE AWS resources gone | Pending |
| Docker Hub image preserved | Expected — no workflow touches Docker Hub |
| GitHub repo preserved | Expected — no workflow touches repository |
| PA preserved | Expected — artifact unchanged |

---

## Errors / Manual Follow-Up

None yet.

---

## Safety Notes

- Destroy workflow is `workflow_dispatch` only.
- Only Terraform-managed PE resources (`nebula-maint-app-pe-*`) are targeted.
- State recovery imports existing AWS resources when CI state is empty.
- Manual AWS deletion is not required unless Terraform destroy fails.
