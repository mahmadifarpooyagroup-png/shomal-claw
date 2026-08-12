import unittest
import json
import os


class TestQueueTicketDocType(unittest.TestCase):
    """Unit tests for Queue Ticket DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "queue_ticket")
        with open(os.path.join(base, "queue_ticket.json")) as f:
            self.doc = json.load(f)

    def test_has_hd_ticket_link(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("hd_ticket", fields)
        self.assertEqual(fields["hd_ticket"]["options"], "HD Ticket")

    def test_has_counter_link(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("counter", fields)
        self.assertEqual(fields["counter"]["options"], "Counter")

    def test_has_timing_fields(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("created_at", fields)
        self.assertIn("called_at", fields)
        self.assertIn("serving_started_at", fields)
        self.assertIn("completed_at", fields)

    def test_status_options(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        status = fields["status"]["options"]
        self.assertIn("Waiting", status)
        self.assertIn("Called", status)
        self.assertIn("Serving", status)
        self.assertIn("Hold", status)
        self.assertIn("Completed", status)
        self.assertIn("Cancelled", status)

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)

    def test_citizen_viewer_can_create(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertTrue(perms["Citizen Viewer"]["create"])


if __name__ == "__main__":
    unittest.main()
