"""
Tests for Queue API business logic.
"""
import frappe
import unittest
from unittest.mock import patch, MagicMock


def create_test_citizen():
    """Helper: create a test citizen."""
    if frappe.db.exists("Citizen", "TEST-001"):
        return "TEST-001"
    doc = frappe.get_doc({
        "doctype": "Citizen",
        "citizen_code": "TEST-001",
        "full_name": "Test Citizen",
        "mobile": "09120000000",
        "national_identifier": "0010000001",
        "active": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_test_organization():
    """Helper: create a test organization."""
    if frappe.db.exists("Organization", "ORG-TEST"):
        return "ORG-TEST"
    doc = frappe.get_doc({
        "doctype": "Organization",
        "organization_code": "ORG-TEST",
        "organization_name": "Test Organization",
        "active": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_test_office(org_id):
    """Helper: create a test office."""
    if frappe.db.exists("Office", "OFF-TEST"):
        return "OFF-TEST"
    doc = frappe.get_doc({
        "doctype": "Office",
        "office_code": "OFF-TEST",
        "office_name": "Test Office",
        "organization": org_id,
        "active": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_test_service(office_id):
    """Helper: create a test service."""
    if frappe.db.exists("Service", "SVC-TEST"):
        return "SVC-TEST"
    doc = frappe.get_doc({
        "doctype": "Service",
        "service_code": "SVC-TEST",
        "service_name": "Test Service",
        "office": office_id,
        "active": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_test_counter(office_id):
    """Helper: create a test counter."""
    if frappe.db.exists("Counter", "CNT-TEST"):
        return "CNT-TEST"
    doc = frappe.get_doc({
        "doctype": "Counter",
        "counter_code": "CNT-TEST",
        "counter_name": "Test Counter",
        "office": office_id,
        "active": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def cleanup_test_data():
    """Remove all test data."""
    for dt in ["Queue Ticket", "Counter", "Service", "Office", "Organization", "Citizen"]:
        frappe.db.delete(dt, {"name": ["like", "TEST-%"]})
    frappe.db.commit()


class TestQueueTicketCreation(unittest.TestCase):
    """Test queue ticket creation."""

    def setUp(self):
        self.citizen = create_test_citizen()
        self.org = create_test_organization()
        self.office = create_test_office(self.org)
        self.service = create_test_service(self.office)

    def tearDown(self):
        cleanup_test_data()

    def test_create_ticket_valid(self):
        """A valid ticket should be created with Waiting status."""
        from atrin.queue.api import create_ticket

        ticket = create_ticket(self.citizen, self.service, self.office)
        doc = frappe.get_doc("Queue Ticket", ticket.name)

        self.assertEqual(doc.citizen, self.citizen)
        self.assertEqual(doc.service, self.service)
        self.assertEqual(doc.office, self.office)
        self.assertEqual(doc.status, "Waiting")
        self.assertIsNotNone(doc.ticket_number)

    def test_create_ticket_invalid_citizen(self):
        """Should throw when citizen does not exist."""
        from atrin.queue.api import create_ticket
        with self.assertRaises(frappe.ValidationError):
            create_ticket("NONEXISTENT", self.service, self.office)

    def test_create_ticket_ticket_number_format(self):
        """Ticket number should follow OFF-TEST-NNNN format."""
        from atrin.queue.api import create_ticket
        ticket = create_ticket(self.citizen, self.service, self.office)
        doc = frappe.get_doc("Queue Ticket", ticket.name)
        self.assertRegex(doc.ticket_number, r"OFF-TEST-\d{4}")

    def test_create_ticket_sequential_numbers(self):
        """Ticket numbers should increment."""
        from atrin.queue.api import create_ticket
        t1 = create_ticket(self.citizen, self.service, self.office)
        t2 = create_ticket(self.citizen, self.service, self.office)
        d1 = frappe.get_doc("Queue Ticket", t1.name)
        d2 = frappe.get_doc("Queue Ticket", t2.name)
        # Numbers should be different
        self.assertNotEqual(d1.ticket_number, d2.ticket_number)


class TestCallNext(unittest.TestCase):
    """Test call-next logic."""

    def setUp(self):
        self.citizen = create_test_citizen()
        self.org = create_test_organization()
        self.office = create_test_office(self.org)
        self.service = create_test_service(self.office)
        self.counter = create_test_counter(self.office)

    def tearDown(self):
        cleanup_test_data()

    def test_call_next_empty_queue(self):
        """Should return None when no tickets are waiting."""
        from atrin.queue.api import call_next
        result = call_next(self.counter)
        self.assertIsNone(result)

    def test_call_next_with_ticket(self):
        """Should call the next waiting ticket."""
        from atrin.queue.api import create_ticket, call_next

        ticket = create_ticket(self.citizen, self.service, self.office)
        result = call_next(self.counter)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, ticket.name)
        self.assertEqual(result.status, "Called")

    def test_call_next_updates_counter(self):
        """Counter should reference the called ticket."""
        from atrin.queue.api import create_ticket, call_next

        create_ticket(self.citizen, self.service, self.office)
        call_next(self.counter)

        counter = frappe.get_doc("Counter", self.counter)
        self.assertIsNotNone(counter.current_ticket)

    def test_call_next_inactive_counter(self):
        """Should throw when counter is not active."""
        from atrin.queue.api import call_next
        frappe.db.set_value("Counter", self.counter, "active", 0)
        with self.assertRaises(frappe.ValidationError):
            call_next(self.counter)


class TestTicketLifecycle(unittest.TestCase):
    """Test complete ticket lifecycle."""

    def setUp(self):
        self.citizen = create_test_citizen()
        self.org = create_test_organization()
        self.office = create_test_office(self.org)
        self.service = create_test_service(self.office)
        self.counter = create_test_counter(self.office)

    def tearDown(self):
        cleanup_test_data()

    def test_full_lifecycle(self):
        """Test: Waiting → Called → Serving → Completed."""
        from atrin.queue.api import (
            create_ticket, call_next, mark_serving, complete_ticket
        )

        # Create and call
        ticket = create_ticket(self.citizen, self.service, self.office)
        called = call_next(self.counter)
        self.assertEqual(called.status, "Called")

        # Mark serving
        mark_serving(called.name, self.counter)
        serving = frappe.get_doc("Queue Ticket", called.name)
        self.assertEqual(serving.status, "Serving")

        # Complete
        complete_ticket(called.name)
        completed = frappe.get_doc("Queue Ticket", called.name)
        self.assertEqual(completed.status, "Completed")
        self.assertIsNotNone(completed.completed_at)

        # Counter should be cleared
        counter = frappe.get_doc("Counter", self.counter)
        self.assertIsNone(counter.current_ticket)

    def test_hold_and_recall(self):
        """Test: Called → Hold → Called."""
        from atrin.queue.api import create_ticket, call_next, hold_ticket, recall_ticket

        create_ticket(self.citizen, self.service, self.office)
        called = call_next(self.counter)

        hold_ticket(called.name, "Customer left")
        held = frappe.get_doc("Queue Ticket", called.name)
        self.assertEqual(held.status, "Hold")

        recall_ticket(called.name, self.counter)
        recalled = frappe.get_doc("Queue Ticket", called.name)
        self.assertEqual(recalled.status, "Called")

    def test_cannot_complete_waiting(self):
        """Should not allow completing a Waiting ticket."""
        from atrin.queue.api import create_ticket, complete_ticket
        ticket = create_ticket(self.citizen, self.service, self.office)
        with self.assertRaises(frappe.ValidationError):
            complete_ticket(ticket.name)

    def test_cannot_cancel_serving(self):
        """Should not allow cancelling a Serving ticket."""
        from atrin.queue.api import create_ticket, call_next, mark_serving, cancel_ticket

        create_ticket(self.citizen, self.service, self.office)
        called = call_next(self.counter)
        mark_serving(called.name, self.counter)

        with self.assertRaises(frappe.ValidationError):
            cancel_ticket(called.name)


class TestQueueStatus(unittest.TestCase):
    """Test queue status reporting."""

    def setUp(self):
        self.citizen = create_test_citizen()
        self.org = create_test_organization()
        self.office = create_test_office(self.org)
        self.service = create_test_service(self.office)

    def tearDown(self):
        cleanup_test_data()

    def test_empty_queue_status(self):
        """Empty queue should return zero counts."""
        from atrin.queue.api import get_queue_status
        status = get_queue_status(self.office)
        self.assertEqual(status["office"], self.office)
        self.assertEqual(status["total"], 0)

    def test_queue_status_with_tickets(self):
        """Should return correct counts."""
        from atrin.queue.api import create_ticket, get_queue_status

        create_ticket(self.citizen, self.service, self.office)
        create_ticket(self.citizen, self.service, self.office)

        status = get_queue_status(self.office)
        self.assertEqual(status["total"], 2)
        self.assertEqual(status["statuses"].get("Waiting"), 2)
        self.assertEqual(len(status["next_waiting"]), 2)
