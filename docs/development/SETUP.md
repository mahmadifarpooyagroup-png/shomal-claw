# Development Setup

## Recommended environment

Use WSL2 + Ubuntu on Windows for the Frappe development environment. Keep the Git repository on GitHub and use the local WSL workspace for Bench execution.

## Important

The exact Frappe version should be pinned after the target supported release is selected. Do not mix arbitrary Frappe, ERPNext and Python versions.

## Development flow

1. Install/verify WSL2 Ubuntu.
2. Install Git, Python, MariaDB/PostgreSQL as required by the selected Frappe release, Redis and Node dependencies.
3. Install Frappe Bench.
4. Initialize a Bench.
5. Create a local site.
6. Clone/install the Shomal/Atrin app.
7. Run migrations.
8. Start the development stack.
9. Create the first DocTypes and tests.

## Repository rule

GitHub `shomal` is the source of truth. Generated Bench files, site data, logs, private files and runtime assets must not be committed.

## First executable slice

Organization -> Service -> Citizen -> Appointment/Walk-in -> Queue Ticket -> Counter -> Case -> Completion
