# ADR 0001 — Platform Choice

## Status
Accepted

## Decision
Use Frappe Framework as the technical platform for Shomal/Atrin.

## Context
The project needs a mature application platform with authentication, permissions, document modeling, workflow, APIs, realtime communication, background jobs, migrations and reporting. Building these foundations from scratch would add unnecessary risk and delay.

## Consequences
- Atrin-specific business logic stays in the Atrin app.
- Frappe core is not forked.
- ERPNext and Frappe Helpdesk are treated as reusable/reference sources rather than the application base.
- Queue and government-service behavior remain Atrin-owned domains.
- The first implementation is a modular monolith.
