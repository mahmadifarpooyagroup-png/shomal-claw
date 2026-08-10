# Environment Validation Gate

## Mandatory reuse rule

**Frappe → ERPNext → Helpdesk → Reuse/Extend → only if unavailable, custom Atrin code.**

## Purpose

Before writing runtime integration code, validate the actual Shomal installation. GitHub source alone is not sufficient to assume which ERPNext/Helpdesk versions are installed or which hooks are available at runtime.

## Required checks

Run these checks in the actual Shomal/Frappe bench environment:

```bash
bench version
bench --site <site> list-apps
bench --site <site> list-apps --format json
```

Confirm:

- Frappe version
- ERPNext version
- Helpdesk version
- Atrin version/branch
- Site name
- Database engine/version

## Integration validation

After versions are known, verify the installed runtime for:

1. ERPNext Appointment DocType and its fields/workflow.
2. ERPNext booking APIs/settings used by the selected version.
3. Helpdesk HD Ticket DocType and its status/activity/assignment model.
4. Frappe hooks supported by the installed version.
5. Existing Atrin DocTypes and references that must be migrated.

## Gate

No `hooks.py` integration, migration script, or runtime adapter should be added until these checks are available and recorded in the implementation PR.

If an upstream feature exists, use or extend it. If the installed version differs from repository assumptions, adapt to the installed upstream implementation rather than creating a parallel Atrin engine.

## Current status

Architecture and migration plans are ready. Runtime integration is intentionally blocked pending environment/version validation.
