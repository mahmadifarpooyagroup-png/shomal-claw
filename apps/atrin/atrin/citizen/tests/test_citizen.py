import unittest
import json
import os


class TestCitizenDocType(unittest.TestCase):
    """Unit tests for Citizen DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "citizen")
        with open(os.path.join(base, "citizen.json")) as f:
            self.doc = json.load(f)

    def test_has_citizen_code_required_unique(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertTrue(fields["citizen_code"]["reqd"])
        self.assertTrue(fields["citizen_code"]["unique"])

    def test_has_full_name_required(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertTrue(fields["full_name"]["reqd"])

    def test_has_contact_fields(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("mobile", fields)
        self.assertIn("phone", fields)
        self.assertIn("email", fields)

    def test_has_personal_details(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("date_of_birth", fields)
        self.assertIn("gender", fields)

    def test_national_identifier_unique(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertTrue(fields["national_identifier"]["unique"])

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)

    def test_citizen_viewer_can_create(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertTrue(perms["Citizen Viewer"]["create"])
        self.assertFalse(perms["Citizen Viewer"].get("write", 0))

    def test_counter_agent_can_create(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertTrue(perms["Counter Agent"]["create"])
        self.assertTrue(perms["Counter Agent"]["write"])

    def test_title_field(self):
        self.assertEqual(self.doc.get("title_field"), "full_name")

    def test_has_queue_ticket_link(self):
        links = self.doc.get("links", [])
        self.assertTrue(any(l["link_doctype"] == "Queue Ticket" for l in links))


if __name__ == "__main__":
    unittest.main()
