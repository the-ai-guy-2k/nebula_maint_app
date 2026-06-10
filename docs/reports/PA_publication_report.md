# PA Publication Report — Nebula Maintenance App

**ACI:** ACI-DEVOPS-002 / ACI-DEVOPS-002R  
**Date:** 2026-06-10  
**Status:** **PA ACHIEVED — Published to Docker Hub**

---

## Publication Summary

| Field | Value |
|-------|-------|
| Docker Repository | `taig2k/nebula_maint_app` |
| Image Tag | `v0.1` |
| Full Image Reference | `docker.io/taig2k/nebula_maint_app:v0.1` |
| GitHub Branch | `deployable` |
| Commit SHA | `707bcdbf3e72568001c4af8abd8a01cc795db092` |
| Workflow Run ID | [27314144449](https://github.com/the-ai-guy-2k/nebula_maint_app/actions/runs/27314144449) |
| Workflow Run URL | https://github.com/the-ai-guy-2k/nebula_maint_app/actions/runs/27314144449 |
| Trigger | Push to `deployable` (re-run publication pipeline) |
| Result | **Success** |
| PA Status | **Achieved** |

---

## Validation Results

| Check | Result |
|-------|--------|
| Workflow started successfully | PASS |
| Docker Hub secret verification | PASS |
| Docker Hub login | PASS |
| Docker image build | PASS |
| Docker image push | PASS |
| Image tag `v0.1` on Docker Hub | PASS |
| Image pullable from Docker Hub | PASS (tag active, last pushed 2026-06-10) |

---

## Docker Hub Evidence

| Field | Value |
|-------|-------|
| Tag | `v0.1` |
| Tag Status | active |
| Architecture | linux/amd64 |
| Image Digest | `sha256:9de4a220aad2f77383bb4ac7aa8f51c7d3aece991bf5ee92a34aaeb4b8573d45` |
| Hub URL | https://hub.docker.com/r/taig2k/nebula_maint_app/tags |

---

## Pull and Run

```bash
docker pull taig2k/nebula_maint_app:v0.1
docker run -d --name nebula_maint_app -p 5000:5000 taig2k/nebula_maint_app:v0.1
```

Open http://127.0.0.1:5000/

---

## Prior Attempts (Resolved)

Earlier runs (#1–#4) failed because `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` were not accessible to GitHub Actions. After repository secrets were confirmed and the pipeline re-run (run #6), authentication and push completed successfully.

---

## Conclusion

The Nebula Maintenance App artifact is published to Docker Hub as `taig2k/nebula_maint_app:v0.1`. **PA publication validated.**
