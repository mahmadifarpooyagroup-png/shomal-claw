import frappe
from frappe.model.document import Document


class Organization(Document):
    def validate(self):
        if self.organization_code:
            self.organization_code = self.organization_code.strip().upper()
        if self.organization_name:
            self.organization_name = self.organization_name.strip()

    def on_update(self):
        frappe.clear_cache(doctype=self.doctype)
