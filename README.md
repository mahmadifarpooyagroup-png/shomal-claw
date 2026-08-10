# Shomal

**Atrin Smart Service Platform (ASSP)**

Shomal is the development repository for Atrin's smart service platform.

## Architecture

Shomal is a modular monolith built on **Frappe Framework**. ERPNext and Frappe Helpdesk are installed as internal applications and are reused/extended inside the same Shomal deployment where they provide suitable capabilities.

### Mandatory development direction

**Frappe → ERPNext → Helpdesk → Reuse/Extend → only if unavailable, custom Atrin code.**

This is a mandatory gate for every functional change. A PR must document the upstream search and justify any custom implementation.

### Domain ownership

- Frappe → platform, ORM, permissions, workflow, API, jobs, realtime and migrations
- ERPNext → Appointment and SLA capabilities that fit the requirements
- Helpdesk → Ticket/Case lifecycle, activity, assignment and related helpdesk capabilities
- Atrin → Citizen, Service Registry and Pishkhan-specific Queue, Counter, Call Next and routing where upstream capabilities are insufficient

### Runtime model

Frappe, ERPNext, Helpdesk and Atrin run together inside the same Shomal installation. The core Pishkhan workflow is designed to operate over the local network without Internet access. External government APIs, SMS and cloud services can remain connectivity-dependent.

### Core domains

Identity · Organization · Citizen · Service Registry · Case Management · Queue · Counter · Appointment · Document · Asset · Finance · Government Integration · Reporting

See [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`docs/architecture/domain-map.md`](docs/architecture/domain-map.md).

## Current status

Architecture baseline aligned with the mandatory reuse gate. Next implementation work is the safe migration from parallel Atrin Appointment/Service Case implementations to ERPNext Appointment and Helpdesk HD Ticket, followed by integration with Atrin Queue and Counter.

Future ideas that are not currently selected for implementation are kept under `docs/future/`.
