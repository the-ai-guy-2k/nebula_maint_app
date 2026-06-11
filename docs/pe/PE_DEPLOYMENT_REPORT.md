# PE Deployment Report — Nebula Maintenance App

**ACI:** ACI-PE-002  
**Date:** 2026-06-10  
**Branch:** `feature/pe-aws-ec2`  
**Deployment Status:** Pending — awaiting GitHub Actions Terraform apply

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

Populated after successful `terraform apply` via workflow outputs:
- `ec2_public_ip`
- `app_url`

---

## Deployment Status

| Check | Status |
|-------|--------|
| Terraform files created | Complete |
| GitHub Actions workflow created | Complete |
| Workflow triggered | Pending |
| Terraform apply | Pending |
| EC2 instance running | Pending |
| App reachable | Pending |

---

## Validation Steps (Post-Deploy)

1. Confirm GitHub Actions workflow **Terraform PE Deploy** completed successfully
2. Record `ec2_public_ip` and `app_url` from workflow summary
3. Open app URL in browser — dashboard should display Nebula nodes
4. Update this report with workflow run ID and final URLs

---

## Security Note (MVP)

Security group allows SSH (22) and app traffic (5000) from `0.0.0.0/0` for MVP testing only. Restrict before production use.
