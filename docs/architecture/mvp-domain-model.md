# MVP Domain Model

## Organization
Represents a service organization and its offices/branches.

Key concepts: Organization, Office, Department, Counter.

## Service
Represents a service offered by an office or channel.

Key concepts: Service, Service Category, Service Channel, Required Document, SLA, Fee.

## Citizen
Represents the person requesting a service.

Key concepts: Citizen, Contact, Identifier, Consent.

## Appointment
Represents a scheduled service interaction.

Key concepts: Appointment, Slot, Check-in, Cancellation.

## Queue Ticket
Represents a walk-in or checked-in waiting interaction.

Key concepts: Queue Ticket, Queue, Priority, Position, Calling, Hold, Recall.

## Counter
Represents a physical or logical service station.

Key concepts: Counter, Counter Type, Operator Station, Availability.

## Service Case
Represents the operational case created for a service interaction.

Key concepts: Case, Assignment, Workflow, SLA, Resolution, Completion.

## MVP relationships

Organization 1..* Office
Office 1..* Service
Office 1..* Counter
Citizen 1..* Appointment
Citizen 1..* Queue Ticket
Service 1..* Appointment
Service 1..* Queue Ticket
Appointment 0..1 Queue Ticket
Queue Ticket 0..1 Counter
Queue Ticket 0..1 Service Case
Service Case 1..1 Service
Service Case 1..1 Citizen
