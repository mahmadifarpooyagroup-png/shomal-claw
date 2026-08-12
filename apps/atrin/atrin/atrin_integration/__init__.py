"""
Atrin Integration Layer
========================
Connects Atrin-specific domains (Queue, Counter, Citizen) to upstream
Frappe/ERPNext/Helpdesk capabilities.

Architecture:
  Atrin Queue Ticket → Helpdesk HD Ticket → ERPNext Appointment → Counter

Activation:
  Integration hooks and adapters are activated ONLY after environment
  validation confirms ERPNext and Helpdesk are installed and their
  exact DocType versions are known.

  See: docs/development/ENVIRONMENT-VALIDATION.md

WARNING:
  Do NOT import or activate these modules until the runtime environment
  has been verified. GitHub source inspection is sufficient for design
  decisions but NOT for runtime integration.
"""

# ---------------------------------------------------------------------------
# ERPNext Appointment Integration
# ---------------------------------------------------------------------------
# Maps Atrin Citizen/Service/Office to ERPNext Appointment (CRM-based).
# ERPNext Appointment uses "customer" and "party" fields which must be
# mapped to Atrin Citizen via a custom field extension.
#
# def on_appointment_update(doc, method):
#     """Hook: ERPNext Appointment updated → sync to Atrin Queue/Case."""
#     pass


# ---------------------------------------------------------------------------
# Helpdesk HD Ticket Integration
# ---------------------------------------------------------------------------
# Maps Atrin Queue Ticket to Helpdesk HD Ticket.
# HD Ticket provides SLA, assignment, response tracking, and resolution
# that Atrin Service Case lacks. Custom fields on HD Ticket link back to
# Atrin Citizen, Service, Office, and Queue Ticket.
#
# def on_ticket_update(doc, method):
#     """Hook: HD Ticket updated → sync Atrin Queue/Counter status."""
#     pass


# ---------------------------------------------------------------------------
# Queue → Case → Counter Bridge
# ---------------------------------------------------------------------------
# When a Queue Ticket is created (walk-in or from appointment check-in),
# a linked HD Ticket is created/updated. The Counter calls the next ticket
# via Atrin queue.api, and the ticket's HD Ticket status reflects the
# counter interaction.
#
# def create_case_from_queue(queue_ticket):
#     """Create HD Ticket from Queue Ticket."""
#     pass


# ---------------------------------------------------------------------------
# Version Compatibility
# ---------------------------------------------------------------------------
# These adapters must be verified against the ACTUAL installed versions:
#   - ERPNext version-15 Appointment doctype
#   - Helpdesk main HD Ticket doctype
#
# The UPSTREAM-REUSE-AUDIT-01.md documents the expected field names
# and capabilities based on GitHub source inspection.
