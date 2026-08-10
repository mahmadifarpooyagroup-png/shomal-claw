# Service Case → Helpdesk Migration Plan

## Mandatory reuse gate

**Frappe → ERPNext → Helpdesk → Reuse/Extend → only if unavailable, custom Atrin code.**

## Decision

The current Atrin `Service Case` must not become a second case/ticket engine. Frappe Helpdesk `HD Ticket` is the target operational case record.

## Current mapping

| Atrin Service Case | Helpdesk target | Decision |
|---|---|---|
| citizen | HD Ticket customer/contact reference; Atrin Citizen remains domain master | Integrate/Extend |
| service | custom/link metadata on ticket where needed | Extend |
| office | ticket metadata / routing context | Extend |
| queue_ticket | Atrin Queue Ticket reference | Keep Atrin-specific |
| status | HD Ticket status | Reuse Helpdesk |
| opened_at | Helpdesk ticket creation timestamp | Reuse Helpdesk |
| completed_at | Helpdesk completion/close lifecycle | Reuse Helpdesk |
| resolution | Helpdesk resolution/description fields where applicable | Reuse/Extend |

## Target flow

```text
Appointment / Walk-in
        ↓
ERPNext Appointment (when applicable)
        ↓
Helpdesk HD Ticket
        ↓
Atrin Queue Ticket
        ↓
Counter / Call Next
        ↓
Service execution
        ↓
HD Ticket completion/closure
```

## Migration safety

1. Do not delete the legacy `Service Case` DocType yet.
2. Freeze feature development on the legacy case engine.
3. Inventory existing Service Case records and references.
4. Verify the exact installed Helpdesk `HD Ticket` fields/workflow before writing migration code.
5. Build a migration script only after that verification.
6. Migrate records in a test environment first.
7. Verify Queue Ticket references and Citizen/Service/Office relationships.
8. Verify status, resolution and timestamps.
9. Run end-to-end tests.
10. Deprecate the legacy DocType only after successful validation.

## Non-goals

Do not create an Atrin replacement for Helpdesk ticket status, assignment, activity, SLA, notifications, permissions or ticket lifecycle.

## Custom-code boundary

Atrin-specific code is allowed only for genuine Pishkhan requirements, especially queue numbering, counter assignment, call-next behavior and routing that cannot reasonably be expressed through upstream configuration/extension.

## Required PR evidence

Before implementation, the PR must record concrete evidence from Frappe, ERPNext and Helpdesk and explain every custom field or method that remains after migration.
