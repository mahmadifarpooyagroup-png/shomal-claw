# Shomal / Atrin Architecture

## Decision
Shomal is the foundation for Atrin Smart Service Platform (ASSP).

- Platform: Frappe Framework
- Application: Atrin
- Architecture: Modular Monolith
- Queue engine: Atrin-specific Pishkhan domain module
- ERPNext: installed and reused/extended for capabilities it already provides, especially Appointment and SLA
- Frappe Helpdesk: installed and reused/extended for Ticket/Case lifecycle, activity, assignment and related helpdesk capabilities
- External projects: research/reference only unless explicitly approved; they are not runtime dependencies by default

## Mandatory Reuse Gate

Every functional requirement must follow this order:

**Frappe → ERPNext → Helpdesk → Reuse/Extend → only if unavailable, custom Atrin code.**

A PR is not merge-ready unless it records the upstream search and explains any custom implementation.

## Core Domains

1. Identity
2. Organization
3. Citizen
4. Service Registry
5. Case Management (Helpdesk-backed)
6. Queue (Atrin-specific Pishkhan behavior)
7. Counter (Atrin-specific)
8. Appointment (ERPNext-backed)
9. Document
10. Asset
11. Finance
12. Government Integration
13. Reporting

## Runtime and Offline Principle

Frappe, ERPNext, Helpdesk and Atrin run as applications inside the same Shomal installation. The operational Pishkhan path must work over the local network without requiring Internet connectivity. External government APIs, SMS gateways and cloud services may require Internet access.

Do not create duplicate offline implementations of upstream Appointment, Ticket, SLA, Assignment, Activity, Workflow or Permission domains. An Atrin-specific synchronization layer is permitted only after the same upstream reuse audit proves it is required.

## Principles

- Do not fork Frappe.
- Keep Atrin-specific code inside the Atrin app.
- Prefer Frappe-native capabilities for authentication, permissions, workflow, API, jobs, realtime, documents and migrations.
- Reuse/extend installed ERPNext and Helpdesk capabilities rather than linking to external systems or rebuilding equivalent engines.
- Keep Queue, Counter, Call Next and Pishkhan-specific routing in Atrin where upstream functionality is insufficient.
- Start as a modular monolith; extract services only when operational evidence justifies it.
- Preserve domain boundaries without introducing unnecessary microservices.
- Future ideas belong under `docs/future/` until explicitly selected for implementation.
