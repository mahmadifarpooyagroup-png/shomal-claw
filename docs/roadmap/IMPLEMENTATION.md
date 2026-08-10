# Shomal Implementation Roadmap

## Phase 0 — Foundation
- Frappe development environment
- Atrin application scaffold
- CI baseline
- coding conventions
- environment documentation

## Phase 1 — Core Domain
- Organization
- Office/Branch
- Citizen
- User/Operator
- Service Registry
- Service Category

## Phase 2 — Service Execution
- Service Case
- Required Documents
- Workflow
- Assignment
- SLA
- Appointment

## Phase 3 — Queue Operations
- Queue Ticket
- Queue Policy
- Priority
- Counter
- Operator Station
- Calling
- Hold/Recall
- Serving/Completion
- Check-in
- Digital signage API

## Phase 4 — Transactions
- Fees
- Payment Request
- Receipt
- Government transaction
- Retry/idempotency
- Audit trail

## Phase 5 — Operations
- dashboards
- reporting
- monitoring
- permissions hardening
- backups
- deployment

## Phase 6 — Advanced
- offline-first workflows where justified
- synchronization/outbox
- external integrations
- performance optimization
- selective service extraction if required

## First MVP
The first executable slice should be intentionally small:

Organization -> Service -> Citizen -> Appointment/Walk-in -> Queue Ticket -> Counter -> Case -> Completion

This vertical slice will validate the platform and domain architecture before broad module expansion.
