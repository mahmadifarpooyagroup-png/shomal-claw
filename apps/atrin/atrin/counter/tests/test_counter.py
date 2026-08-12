import unittest
import json
import os


class TestCounterDocType(unittest.TestCase):
    """Unit tests for Counter DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "counter")
        with open(os.path.join(base, "counter.json")) as f:
            self.doc = json.load(f)

    def test_has_status_field(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("status", fields)
        self.assertEqual(fields["status"]["fieldtype"], "Select")
        self.assertIn("Online", fields["status"]["options"])
        self.assertIn("Offline", fields["status"]["options"])
        self.assertIn("Break", fields["status"]["options"])

    def test_default_status_offline(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["status"]["default"], "Offline")

    def test_has_current_ticket(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["current_ticket"]["options"], "Queue Ticket")
        self.assertTrue(fields["current_ticket"]["read_only"])

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)

    def test_counter_agent_can_read_write(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertTrue(perms["Counter Agent"]["read"])
        self.assertTrue(perms["Counter Agent"]["write"])


if __name__ == "__main__":
    unittest.main()
