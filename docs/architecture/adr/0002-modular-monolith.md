# ADR 0002 — Modular Monolith

## Status
Accepted

## Decision
Build Atrin initially as a modular monolith on Frappe Framework.

## Rationale
The domains require strong transactional consistency and rapid iteration. Separate microservices would add deployment, observability, messaging and data-consistency complexity before there is evidence that extraction is necessary.

## Rules
- Keep domain modules separated in code and documentation.
- Avoid direct coupling between unrelated domain internals.
- Expose stable application services/events at domain boundaries.
- Extract a service only after measurable scaling, isolation, or integration requirements justify it.
