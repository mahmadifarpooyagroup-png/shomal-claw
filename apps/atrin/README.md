# Atrin Application

This directory is reserved for the Atrin Frappe application source.

The application will be implemented as a modular monolith on Frappe Framework. Domain modules will remain internally separated while sharing the Frappe runtime and platform services.

## Planned modules

- identity
- organization
- citizen
- service_registry
- case_management
- queue
- counter
- appointment
- document
- asset
- finance
- integration
- reporting

The actual Frappe app scaffold will be introduced only when the repository is connected to a Frappe Bench/development environment, so generated framework metadata is not fabricated manually in this repository.
