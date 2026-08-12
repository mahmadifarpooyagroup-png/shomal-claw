import unittest
import json
import os


class TestOfficeDocType(unittest.TestCase):
    """Unit tests for Office DocType."""

    def setUp(self):
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "office")
        with open(os.path.join(base, "office.json")) as f:
            self.doc = json.load(f)

    def test_has_office_code(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("office_code", fields)
        self.assertTrue(fields["office_code"]["reqd"])
        self.assertTrue(fields["office_code"]["unique"])

    def test_links_to_organization(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["organization"]["fieldtype"], "Link")
        self.assertEqual(fields["organization"]["options"], "Organization")

    def test_has_contact_fields(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("phone", fields)
        self.assertIn("address", fields)

    def test_has_counters_table(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["counters"]["fieldtype"], "Table")
        self.assertEqual(fields["counters"]["options"], "Office Counter")

    def test_no_system_manager(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)

    def test_title_field(self):
        self.assertEqual(self.doc.get("title_field"), "office_name")


if __name__ == "__main__":
    unittest.main()
