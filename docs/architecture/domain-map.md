# Atrin Domain Map

## Platform Layer

Frappe provides the technical platform: identity, RBAC, document model, database abstraction, API, workflow, background jobs, realtime, notifications, files, and migrations.

## Atrin Domain Layer

### Identity
Users, roles, operator identity, authorization policies.

### Organization
Company, office/branch, department, counter group, organizational ownership.

### Citizen
Citizen profile, contact data, identifiers, consent and service history references.

### Service Registry
Service definitions, categories, required documents/data, channels, fees, SLA, availability, workflow and government provider mapping.

### Case Management
Service case, ticket, assignment, SLA, communication, status and resolution.

### Queue
Queue ticket, queue policy, priority, calling, waiting, hold, serving and completion.

### Counter
Office counter, counter type, operator station, service capability and availability.

### Appointment
Appointment booking, slots, check-in, confirmation, cancellation and linkage to service/case/queue.

### Document
Required documents, uploaded files, verification and document checklist.

### Asset
Service-center assets and equipment where required.

### Finance
Fees, payment requests, receipts and accounting integration.

### Government Integration
External government systems, adapters, credentials, requests, responses, retries and audit trail.

### Reporting
Operational dashboards, queue metrics, service performance, SLA and management reports.

## Main Flow

Citizen -> Service Registry -> Appointment/Walk-in -> Queue -> Counter/Operator -> Case -> Documents/Payment/Government Integration -> Completion -> Reporting
