# Upstream Integration Points

## Mandatory gate

**Frappe → ERPNext → Helpdesk → Reuse/Extend → only if unavailable, custom Atrin code.**

## Verified repository baseline

The current `main` tree contains the Atrin app and its current parallel Appointment and Service Case DocTypes. These are frozen for feature expansion while migration is designed. fileciteturn179file0

Atrin `hooks.py` currently contains no ERPNext/Helpdesk event hooks, so no integration behavior is active yet. fileciteturn178file0

## Integration boundary

```text
ERPNext Appointment
        │
        │ approved extension/integration point
        ▼
Atrin integration layer
        │
        ▼
Helpdesk HD Ticket
        │
        │ reference
        ▼
Atrin Queue Ticket
        │
        ▼
Counter / Call Next
```

## Rules

- Do not create an Atrin Appointment scheduler.
- Do not create an Atrin Ticket/Case lifecycle.
- Do not fork ERPNext or Helpdesk.
- Do not add hooks until the exact upstream event and installed-app dependency are verified in the target runtime.
- Queue, Counter, Call Next and Pishkhan-specific routing remain Atrin-owned only where upstream capabilities do not cover them.

## Next implementation gate

Before adding integration code, verify in the actual Shomal bench/container:

1. ERPNext is installed and its Appointment DocType is available.
2. Helpdesk is installed and `HD Ticket` is available.
3. The exact Appointment lifecycle/event used by the installed ERPNext version.
4. The exact Helpdesk ticket creation/update API available in the installed version.
5. Required fields for linking Citizen, Service, Office and Queue Ticket.

Only after these checks should `hooks.py` or an integration module be changed.

## Why no code yet

GitHub source inspection is sufficient to establish the reuse direction, but it cannot prove which versions are installed in the user's runtime. Writing hooks against an unverified version would violate the reuse-first rule by introducing speculative custom code.
