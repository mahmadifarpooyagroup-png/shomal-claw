import unittest
import json
import os


class TestServiceDocType(unittest.TestCase):
    """Unit tests for Service DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "service")
        with open(os.path.join(base, "service.json")) as f:
            self.doc = json.load(f)

    def test_has_service_code_required_unique(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertTrue(fields["service_code"]["reqd"])
        self.assertTrue(fields["service_code"]["unique"])

    def test_links_to_office(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["office"]["options"], "Office")

    def test_category_links_to_service_category(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["category"]["options"], "Service Category")

    def test_sla_links_to_service_sla(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["sla"]["options"], "Service SLA")

    def test_has_estimated_duration(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("estimated_duration_minutes", fields)
        self.assertEqual(fields["estimated_duration_minutes"]["default"], "15")

    def test_requires_appointment_field(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("requires_appointment", fields)
        self.assertEqual(fields["requires_appointment"]["default"], "0")

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)

    def test_has_queue_ticket_link(self):
        links = self.doc.get("links", [])
        self.assertTrue(any(l["link_doctype"] == "Queue Ticket" for l in links))


class TestServiceCategoryDocType(unittest.TestCase):
    """Unit tests for Service Category DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "service_category")
        with open(os.path.join(base, "service_category.json")) as f:
            self.doc = json.load(f)

    def test_is_tree(self):
        self.assertTrue(self.doc.get("is_tree"))

    def test_has_parent_category_link(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["parent_category"]["options"], "Service Category")

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)


class TestServiceSLADocType(unittest.TestCase):
    """Unit tests for Service SLA DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "service_sla")
        with open(os.path.join(base, "service_sla.json")) as f:
            self.doc = json.load(f)

    def test_has_response_and_resolution_sla(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("response_minutes", fields)
        self.assertIn("resolution_minutes", fields)

    def test_sla_fields_required(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertTrue(fields["response_minutes"]["reqd"])
        self.assertTrue(fields["resolution_minutes"]["reqd"])

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)


if __name__ == "__main__":
    unittest.main()
