# Framework Version Pins

## Decision

Use the supported **Frappe/ERPNext Version 15** line for the Shomal prototype.

- Frappe: `version-15-hotfix`
- ERPNext: `version-15-hotfix`
- Frappe Helpdesk: latest compatible with Frappe 15
- Python: 3.12
- Node.js: 18
- MariaDB: 10.6
- Redis: 7

These pins follow the **currently available** Frappe installation requirements. Do NOT install ERPNext from a different major version than Frappe.

## Why Version 15

Version 15 is the current stable and supported line. Version 16 is not yet available as a stable release and must NOT be used as the target. These pins will be updated when Frappe 16 reaches stable release.

## Compatibility note

The previous VERSION-PINS specified Frappe v16 with Python 3.14+ and Node 24 — these versions do not exist. This file corrects that error.
