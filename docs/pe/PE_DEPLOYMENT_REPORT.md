# PE Deployment Report — Nebula Maintenance App

**ACI:** ACI-PE-002  
**Date:** 2026-06-11  
**Branch:** `feature/pe-aws-ec2` (not merged to `deployable`)  
**Deployment Status:** **SUCCESS — PE live on AWS EC2**

---

## Configuration

| Field | Value |
|-------|-------|
| AWS Region | `us-east-1` |
| Docker Image | `taig2k/nebula_maint_app:v0.1` |
| EC2 Instance Type | `t3.micro` |
| AMI | Amazon Linux 2023 |
| Workflow | `.github/workflows/terraform-pe.yml` |

---

## Terraform Resources

| Resource | Purpose |
|----------|---------|
| `aws_vpc` | PE network (`10.0.0.0/16`) |
| `aws_internet_gateway` | Internet access |
| `aws_subnet` | Public subnet (`10.0.1.0/24`) |
| `aws_route_table` | Default route to IGW |
| `aws_route_table_association` | Subnet routing |
| `aws_security_group` | Inbound 22/tcp, 5000/tcp (MVP testing) |
| `aws_instance` | EC2 host running Docker container |

---

## Published Environment

| Field | Value |
|-------|-------|
| EC2 Public IP | `98.82.24.178` |
| App URL | [http://98.82.24.178:5000](http://98.82.24.178:5000) |
| EC2 Tag | `nebula-maint-app-pe-ec2` |

---

## Deployment Attempt #1

| Field | Value |
|-------|-------|
| Workflow Run | [#27315626758](https://github.com/the-ai-guy-2k/nebula_maint_app/actions/runs/27315626758) |
| Commit | `799f20f` |
| Result | **FAILURE** |
| Failed Step | Configure AWS credentials |
| Error | `Input required and not supplied: aws-region` |

**Root cause:** `AWS_REGION` GitHub secret was not configured. Workflow updated to use hardcoded `us-east-1`.

## Deployment Attempt #2

| Field | Value |
|-------|-------|
| Workflow Run | [#27315708846](https://github.com/the-ai-guy-2k/nebula_maint_app/actions/runs/27315708846) |
| Commit | `2fc0ec1` |
| Result | **FAILURE** |
| Failed Step | Verify AWS secrets |
| Error | `AWS_ACCESS_KEY_ID` and/or `AWS_SECRET_ACCESS_KEY` missing or empty |

**Root cause:** AWS IAM credentials were not yet loaded into nebula_maint_app GitHub repository secrets.

## Deployment Attempt #3 (Successful)

| Field | Value |
|-------|-------|
| Workflow Run | [#27316135616](https://github.com/the-ai-guy-2k/nebula_maint_app/actions/runs/27316135616) |
| Commit | `6601f80` |
| Result | **SUCCESS** |
| Terraform init | Passed |
| Terraform fmt -check | Passed |
| Terraform validate | Passed |
| Terraform plan | Passed |
| Terraform apply | Passed (~1 min) |

---

## Validation

| Check | Status | Evidence |
|-------|--------|----------|
| Terraform apply | **Pass** | Workflow run #27316135616 |
| EC2 instance exists | **Pass** | Instance tagged `nebula-maint-app-pe-ec2` in `us-east-1` |
| Public IP output | **Pass** | `98.82.24.178` |
| App HTTP 200 | **Pass** | `GET http://98.82.24.178:5000/` → 200 |
| Dashboard title | **Pass** | "Nebula Maintenance App" present |
| All 7 nodes displayed | **Pass** | OG, OG2, Cyka, Clooney, Clooney2, Clooney3, Spectrum |

---

## Required GitHub Secrets

| Secret | Status |
|--------|--------|
| `AWS_ACCESS_KEY_ID` | Configured |
| `AWS_SECRET_ACCESS_KEY` | Configured |
| `AWS_REGION` | Optional — workflow defaults to `us-east-1` |

---

## Deployment Status Summary

| Check | Status |
|-------|--------|
| Terraform files created | Complete |
| GitHub Actions workflow created | Complete |
| Workflow triggered | Complete |
| Terraform apply | Complete |
| EC2 instance running | Complete |
| App reachable | Complete |

**PA status:** Achieved (prior validation)  
**PE status:** Live — first AWS Published Environment operational

---

## Security Note (MVP)

Security group allows SSH (22) and app traffic (5000) from `0.0.0.0/0` for MVP testing only. Restrict before production use.
