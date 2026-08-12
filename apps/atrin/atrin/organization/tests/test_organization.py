import unittest
from unittest.mock import patch, MagicMock


class TestOrganizationDocType(unittest.TestCase):
    """Unit tests for Organization DocType.

    These tests validate field definitions and permission structure
    without requiring a running Frappe bench instance.
    """

    def setUp(self):
        import json, os
        base = os.path.join(os.path.dirname(__file__), "..", "doctype", "organization")
        with open(os.path.join(base, "organization.json")) as f:
            self.doc = json.load(f)

    # --- Field Tests ---

    def test_has_organization_code(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("organization_code", fields)
        self.assertEqual(fields["organization_code"]["fieldtype"], "Data")
        self.assertTrue(fields["organization_code"]["reqd"])
        self.assertTrue(fields["organization_code"]["unique"])

    def test_has_organization_name(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("organization_name", fields)
        self.assertTrue(fields["organization_name"]["reqd"])

    def test_has_contact_fields(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("phone", fields)
        self.assertIn("address", fields)

    def test_has_hierarchy_support(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertIn("is_group", fields)
        self.assertIn("lft", fields)
        self.assertIn("rgt", fields)
        self.assertTrue(self.doc.get("is_tree"))

    def test_active_default_true(self):
        fields = {f["fieldname"]: f for f in self.doc["fields"]}
        self.assertEqual(fields["active"]["default"], "1")

    # --- Permission Tests ---

    def test_no_system_manager_only(self):
        roles = {p["role"] for p in self.doc["permissions"]}
        self.assertNotIn("System Manager", roles)

    def test_org_admin_has_full_access(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertIn("Organization Admin", perms)
        org_admin = perms["Organization Admin"]
        self.assertTrue(org_admin["create"])
        self.assertTrue(org_admin["write"])
        self.assertTrue(org_admin["read"])
        self.assertTrue(org_admin["delete"])

    def test_service_manager_read_only(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertIn("Service Manager", perms)
        sm = perms["Service Manager"]
        self.assertTrue(sm["read"])
        self.assertNotIn("create", sm)

    def test_citizen_viewer_read_only(self):
        perms = {p["role"]: p for p in self.doc["permissions"]}
        self.assertIn("Citizen Viewer", perms)
        cv = perms["Citizen Viewer"]
        self.assertTrue(cv["read"])

    # --- Naming ---

    def test_autoname_by_field(self):
        self.assertEqual(self.doc.get("autoname"), "field:organization_code")

    def test_title_field(self):
        self.assertEqual(self.doc.get("title_field"), "organization_name")


if __name__ == "__main__":
    unittest.main()
