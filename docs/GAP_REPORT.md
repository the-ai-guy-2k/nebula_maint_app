# Gap Report — Nebula Maintenance App

**ACI:** ACI-007  
**Date:** 2026-06-10  
**PA Status:** PA Achieved — **no blocking gaps**

---

## Blocking Gaps

**None identified.**

All required validation scenarios passed (29/29 checks). The application meets the established intent for operator-driven maintenance tracking on Nebula nodes.

---

## Out-of-Scope Limitations (Not Blocking PA)

The following items were explicitly excluded from ACI-001 through ACI-006 and do not prevent PA qualification for the current MVP intent:

| Item | Status | Notes |
|------|--------|-------|
| Authentication | Not implemented | Single-operator local use assumed |
| Record editing | Not implemented | Records are append-only |
| Record deletion | Not implemented | History is preserved |
| Prompt versioning / history | Not implemented | Prompts are current-state only |
| Notes / backup filename entry | Partial | Fields exist on records but default to blank; no form to populate at completion |
| Search / filtering (records) | Not implemented | Full list and per-node views only |
| Database | Not implemented | JSON file storage under `data/` |
| AWS / Terraform deployment | Not implemented | Local Flask dev server only |
| Production WSGI server | Not implemented | `python app.py` uses Flask development server |

---

## Recommended Future Enhancements (Post-PA)

These are improvements beyond current PA scope, not deficiencies:

1. **Notes and backup filename capture** — allow operator to enter values when marking maintenance complete.
2. **Production deployment** — WSGI server, hosting, and infrastructure (AWS/Terraform).
3. **Authentication** — if multi-operator or network-exposed deployment is required.
4. **Record management** — edit/delete if operational correction workflows are needed.

---

## Conclusion

No gap report action is required for PA qualification. The Maintenance App is ready for operator use at the MVP stop point.
