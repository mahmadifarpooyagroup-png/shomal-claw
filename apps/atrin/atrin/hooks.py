"""
Atrin Frappe Application — Hooks Configuration
================================================
Domain modules are intentionally kept separate while sharing one runtime.
Integration hooks to ERPNext/Helpdesk will be activated after environment
validation (see docs/development/ENVIRONMENT-VALIDATION.md).
"""
app_name = "atrin"
app_title = "Atrin Smart Service Platform"
app_publisher = "Atrin"
app_description = "Smart service platform built on Frappe Framework"
app_email = ""
app_license = "License to be determined"

# ---------------------------------------------------------------------------
# Fixtures (auto-loaded on install/migrate)
# ---------------------------------------------------------------------------
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "Counter Agent",
        "Queue Operator",
        "Citizen Viewer",
        "Service Manager",
        "Organization Admin",
        "Integration Agent",
        "Audit Viewer",
    ]]],
    },
]

# ---------------------------------------------------------------------------
# DocType JavaScript/CSS (reserved for future UI work)
# ---------------------------------------------------------------------------
app_include_js = []
app_include_css = []

# ---------------------------------------------------------------------------
# DocType events (document-level hooks)
# ---------------------------------------------------------------------------
doc_events = {
    # Example — activate after environment validation:
    # "Appointment": {
    #     "on_update": "atrin.atrin_integration.erpnext_appointment.on_appointment_update",
    # },
    # "HD Ticket": {
    #     "on_update": "atrin.atrin_integration.helpdesk_ticket.on_ticket_update",
    # },
}

# ---------------------------------------------------------------------------
# Scheduler events (background jobs)
# ---------------------------------------------------------------------------
scheduler_events = {
    # "daily": [
    #     "atrin.atrin_integration.tasks.sync_appointments",
    # ],
}

# ---------------------------------------------------------------------------
# Permissions (app-level role defaults)
# ---------------------------------------------------------------------------
has_permission_for = {}
