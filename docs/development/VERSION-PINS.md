# Framework Version Pins

## Decision

Use the supported Frappe/ERPNext Version 16 line for the initial Shomal prototype.

- Frappe: `version-16-hotfix`
- ERPNext: `version-16-hotfix`
- Python: 3.14+
- Node.js: 24

These pins follow the current Frappe installation requirements and supported-version guidance. They must be kept aligned; do not install ERPNext from a different major version than Frappe.

## Why Version 16

Version 16 is a supported line with a long planned support window and is the current stable direction for new Frappe/ERPNext installations. Version 17/develop remains bleeding-edge and is not the initial target for Shomal.
