"""
Queue API — Business Logic Layer
=================================
Pishkhan-specific queue operations that have no upstream equivalent
in Frappe, ERPNext, or Helpdesk.

Operations:
  - create_ticket: Create a new queue ticket for a citizen/service/office
  - call_next: Call the next waiting ticket to a counter
  - hold_ticket: Put a ticket on hold
  - recall_ticket: Recall a held ticket
  - complete_ticket: Mark a ticket as completed
  - cancel_ticket: Cancel a waiting ticket
  - get_queue_status: Get current queue state for an office
"""
import frappe
from frappe import _
from frappe.utils import now_datetime, get_datetime


def create_ticket(citizen_id, service_id, office_id, appointment_id=None, priority=0):
    """Create a new queue ticket.

    Args:
        citizen_id: Citizen document name
        service_id: Service document name
        office_id: Office document name
        appointment_id: Optional linked Appointment
        priority: Integer priority (0 = normal)

    Returns:
        dict: Created Queue Ticket document
    """
    # Validate
    if not frappe.db.exists("Citizen", citizen_id):
        frappe.throw(_("Citizen not found: {0}").format(citizen_id))
    if not frappe.db.exists("Service", service_id):
        frappe.throw(_("Service not found: {0}").format(service_id))
    if not frappe.db.exists("Office", office_id):
        frappe.throw(_("Office not found: {0}").format(office_id))

    ticket = frappe.get_doc({
        "doctype": "Queue Ticket",
        "citizen": citizen_id,
        "service": service_id,
        "office": office_id,
        "appointment": appointment_id,
        "priority": priority,
        "status": "Waiting",
        "ticket_number": _generate_ticket_number(office_id),
    })

    frappe.get_doc(ticket)

    # TODO: After migration — create linked Helpdesk HD Ticket
    # _create_or_link_case(ticket)

    return ticket


def call_next(counter_id):
    """Call the next waiting ticket to the given counter.

    Args:
        counter_id: Counter document name

    Returns:
        dict: Called Queue Ticket or None if queue is empty
    """
    counter = frappe.get_doc("Counter", counter_id)

    if not counter.active:
        frappe.throw(_("Counter {0} is not active").format(counter.counter_name))

    # Find next waiting ticket for this counter's office
    next_ticket = frappe.get_list(
        "Queue Ticket",
        filters={
            "office": counter.office,
            "status": "Waiting",
        },
        order_by="priority desc, creation asc",
        limit_page_length=1,
    )

    if not next_ticket:
        return None

    ticket = frappe.get_doc("Queue Ticket", next_ticket[0].name)
    ticket.status = "Called"
    ticket.called_at = now_datetime()
    ticket.save()

    # Update counter with current ticket
    counter.current_ticket = ticket.name
    counter.save()

    frappe.db.commit()
    return ticket


def mark_serving(ticket_id, counter_id):
    """Mark a called ticket as now being served.

    Args:
        ticket_id: Queue Ticket document name
        counter_id: Counter document name
    """
    ticket = frappe.get_doc("Queue Ticket", ticket_id)

    if ticket.status != "Called":
        frappe.throw(_("Ticket {0} is not in Called status").format(ticket.name))

    ticket.status = "Serving"
    ticket.save()

    # TODO: After migration — update Helpdesk HD Ticket status
    frappe.db.commit()


def hold_ticket(ticket_id, reason=None):
    """Put a ticket on hold.

    Args:
        ticket_id: Queue Ticket document name
        reason: Optional reason for hold
    """
    ticket = frappe.get_doc("Queue Ticket", ticket_id)

    if ticket.status not in ("Called", "Serving"):
        frappe.throw(_("Only Called or Serving tickets can be put on hold"))

    ticket.status = "Hold"
    ticket.save()

    frappe.db.commit()


def recall_ticket(ticket_id, counter_id):
    """Recall a held ticket.

    Args:
        ticket_id: Queue Ticket document name
        counter_id: Counter document name
    """
    ticket = frappe.get_doc("Queue Ticket", ticket_id)

    if ticket.status != "Hold":
        frappe.throw(_("Ticket {0} is not on Hold").format(ticket.name))

    ticket.status = "Called"
    ticket.called_at = now_datetime()
    ticket.save()

    counter = frappe.get_doc("Counter", counter_id)
    counter.current_ticket = ticket.name
    counter.save()

    frappe.db.commit()


def complete_ticket(ticket_id):
    """Mark a ticket as completed.

    Args:
        ticket_id: Queue Ticket document name
    """
    ticket = frappe.get_doc("Queue Ticket", ticket_id)

    if ticket.status not in ("Serving", "Called"):
        frappe.throw(_("Only Serving or Called tickets can be completed"))

    ticket.status = "Completed"
    ticket.completed_at = now_datetime()
    ticket.save()

    # Clear counter
    counter_name = frappe.db.get_value(
        "Counter",
        {"current_ticket": ticket_id},
        "name",
    )
    if counter_name:
        counter = frappe.get_doc("Counter", counter_name)
        counter.current_ticket = None
        counter.save()

    # TODO: After migration — complete Helpdesk HD Ticket
    frappe.db.commit()


def cancel_ticket(ticket_id):
    """Cancel a waiting ticket.

    Args:
        ticket_id: Queue Ticket document name
    """
    ticket = frappe.get_doc("Queue Ticket", ticket_id)

    if ticket.status != "Waiting":
        frappe.throw(_("Only Waiting tickets can be cancelled"))

    ticket.status = "Cancelled"
    ticket.completed_at = now_datetime()
    ticket.save()

    frappe.db.commit()


def get_queue_status(office_id):
    """Get current queue status for an office.

    Args:
        office_id: Office document name

    Returns:
        dict: Queue status summary
    """
    statuses = frappe.db.sql("""
        SELECT status, COUNT(*) as count
        FROM `tabQueue Ticket`
        WHERE office = %s
            AND DATE(creation) = CURDATE()
        GROUP BY status
    """, (office_id,), as_dict=True)

    total = sum(s["count"] for s in statuses)

    # Current serving
    serving = frappe.db.sql("""
        SELECT qt.name, qt.ticket_number, qt.citizen, qt.service,
               c.counter_name
        FROM `tabQueue Ticket` qt
        LEFT JOIN `tabCounter` c ON c.current_ticket = qt.name
        WHERE qt.office = %s
            AND qt.status = 'Serving'
            AND DATE(qt.creation) = CURDATE()
    """, (office_id,), as_dict=True)

    waiting = frappe.db.get_list(
        "Queue Ticket",
        filters={"office": office_id, "status": "Waiting"},
        order_by="priority desc, creation asc",
        limit_page_length=10,
        fields=["name", "ticket_number", "citizen", "service", "priority"],
    )

    return {
        "office": office_id,
        "total": total,
        "statuses": {s["status"]: s["count"] for s in statuses},
        "currently_serving": serving,
        "next_waiting": waiting,
    }


def _generate_ticket_number(office_id):
    """Generate a sequential ticket number for the given office.

    Format: {office_code}-{sequential_number}

    Args:
        office_id: Office document name

    Returns:
        str: Ticket number
    """
    office_code = frappe.db.get_value("Office", office_id, "office_code") or "XX"

    # Get today's last ticket number for this office
    last = frappe.db.sql("""
        SELECT ticket_number
        FROM `tabQueue Ticket`
        WHERE office = %s
            AND DATE(creation) = CURDATE()
        ORDER BY creation DESC
        LIMIT 1
    """, (office_id,), as_dict=True)

    if last and last[0].ticket_number:
        # Extract number and increment
        try:
            parts = last[0].ticket_number.rsplit("-", 1)
            seq = int(parts[-1]) + 1
        except (ValueError, IndexError):
            seq = 1
    else:
        seq = 1

    return f"{office_code}-{seq:04d}"
