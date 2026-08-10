# Atrin Code Reuse Policy

## Mandatory development rule

Every new Atrin capability MUST follow this decision sequence before custom implementation:

```text
Atrin requirement
      ↓
Search Frappe
      ↓
Search ERPNext
      ↓
Search Frappe Helpdesk
      ↓
Suitable existing implementation?
      │
      ├── Yes → Reuse / Extend
      │
      └── No  → Atrin-specific implementation
```

## Required checks

Before creating a new module, DocType, service, API, workflow, UI behavior, or business rule, the developer/agent must:

1. Search Frappe Framework for an existing implementation or reusable pattern.
2. Search ERPNext for an existing implementation or reusable pattern.
3. Search Frappe Helpdesk for an existing implementation or reusable pattern.
4. Prefer direct reuse when technically appropriate.
5. Prefer extension/composition over copying and rewriting existing functionality.
6. Only implement functionality from scratch when no suitable implementation exists or the existing implementation cannot reasonably support the Atrin requirement.

## Pull Request checklist

Every PR adding functionality should document:

- [ ] Frappe searched
- [ ] ERPNext searched
- [ ] Frappe Helpdesk searched
- [ ] Existing implementation found? If yes, reuse/extension decision documented
- [ ] If custom code was written, the reason existing implementations were insufficient is documented

## Scope

This policy applies to all Atrin/Shomal development work, including backend Python, Frappe DocTypes, APIs, workflows, queue logic, appointments, cases, SLA, notifications, permissions, reports and frontend behavior.

This policy is intentionally independent of licensing decisions. License/compliance review remains a separate release requirement.
