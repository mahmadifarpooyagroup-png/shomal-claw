# Shomal

**Atrin Smart Service Platform (ASSP)**

Shomal is the new development repository for Atrin's smart service platform.

## Architecture

Shomal uses **Frappe Framework** as its platform and builds Atrin as a modular application on top of it.

### Direction

- Frappe Framework → platform
- Atrin → domain application
- ERPNext → selective reusable capabilities/reference
- Frappe Helpdesk → Case/Ticket/SLA reference and selective reuse
- BC Government Queue Management → Queue/Counter/Check-in reference

### Core domains

Identity · Organization · Citizen · Service Registry · Case Management · Queue · Counter · Appointment · Document · Asset · Finance · Government Integration · Reporting

See [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`docs/architecture/domain-map.md`](docs/architecture/domain-map.md).

## Current status

Architecture baseline established. Implementation will proceed from the Frappe-based Atrin application foundation, then Service Registry, Citizen, Case, Queue, Counter, Appointment and Government Integration.
