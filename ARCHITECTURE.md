# Shomal / Atrin Architecture

## Decision
Shomal is the new foundation for Atrin Smart Service Platform (ASSP).

- Platform: Frappe Framework
- Application: Atrin
- Architecture: Modular Monolith
- Queue engine: native Atrin domain module
- ERPNext: selective reuse/reference
- Frappe Helpdesk: selective reuse/reference for Case/Ticket/SLA
- BC Government Queue Management: reference for queue/counter/check-in flows

## Core Domains

1. Identity
2. Organization
3. Citizen
4. Service Registry
5. Case Management
6. Queue
7. Counter
8. Appointment
9. Document
10. Asset
11. Finance
12. Government Integration
13. Reporting

## Principles

- Do not fork Frappe.
- Keep Atrin-specific code inside the Atrin app.
- Prefer Frappe-native capabilities for authentication, permissions, workflow, API, jobs, realtime, documents, and migrations.
- Reuse ERPNext/Helpdesk concepts only where they fit Atrin's domain model.
- Build Queue as an Atrin-native domain, not as an external dependency.
- Start as a modular monolith; extract services only when operational evidence justifies it.
- Preserve domain boundaries without introducing unnecessary microservices.
