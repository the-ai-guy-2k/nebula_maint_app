# PE Deployment Report — Nebula Maintenance App

**ACI:** ACI-PE-002  
**Date:** 2026-06-11  
**Branch:** `feature/pe-aws-ec2`  
**Deployment Status:** **BLOCKED — awaiting AWS GitHub secrets**

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

## Expected App URL

```
http://<ec2-public-ip>:5000
```

---

## Deployment Attempt #1

| Field | Value |
|-------|-------|
| Workflow Run | [#27315626758](https://github.com/the-ai-guy-2k/nebula_maint_app/actions/runs/27315626758) |
| Commit | `799f20f` |
| Result | **FAILURE** |
| Failed Step | Configure AWS credentials |
| Error | `Input required and not supplied: aws-region` |

**Root cause:** `AWS_REGION` GitHub secret was not configured. Workflow updated to use hardcoded `us-east-1`. `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` must also be present in repository secrets.

---

## Required GitHub Secrets

| Secret | Status |
|--------|--------|
| `AWS_ACCESS_KEY_ID` | Required — verify in repo settings |
| `AWS_SECRET_ACCESS_KEY` | Required — verify in repo settings |
| `AWS_REGION` | Optional — workflow defaults to `us-east-1` |

---

## Deployment Status

| Check | Status |
|-------|--------|
| Terraform files created | Complete |
| GitHub Actions workflow created | Complete |
| Workflow triggered | Complete (run #1 failed) |
| Terraform apply | Pending |
| EC2 instance running | Pending |
| App reachable | Pending |

---

## Next Steps

1. Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to nebula_maint_app repository secrets
2. Re-run **Terraform PE Deploy** workflow on `feature/pe-aws-ec2`
3. Record `ec2_public_ip` and `app_url` from workflow summary
4. Validate app at `http://<public-ip>:5000`

---

## Security Note (MVP)

Security group allows SSH (22) and app traffic (5000) from `0.0.0.0/0` for MVP testing only. Restrict before production use.
