# Runtime Verification Tasks — Deferred

**وضعیت:** Blocked — نیاز به Frappe Bench running

## M2.1 — Verify ERPNext Appointment در runtime

### acceptance criteria
- `bench --site shomal.local console` باز شود
- `frappe.get_doc('DocType', 'Appointment')` مقدار برگرداند
- Custom fields (citizen_link, service_link, office_link) هنوز اضافه نشده‌اند

### steps when unblocked
1. `bench use shomal.local`
2. `bench console` → `frappe.get_all('DocType', filters={'name': 'Appointment'})`
3. Verify field list matches UPSTREAM-REUSE-AUDIT-01

## M2.2 — Verify Helpdesk HD Ticket در runtime

### acceptance criteria
- `frappe.get_doc('DocType', 'HD Ticket')` مقدار برگرداند
- Custom fields روی HD Ticket قابل ایجاد باشند

### steps when unblocked
1. `bench console` → `frappe.get_all('DocType', filters={'name': 'HD Ticket'})`
2. Verify SLA fields, agent_group, priority exist

## blocker
Frappe Bench نصب نیست. WSL نیاز به:
```bash
sudo apt-get install -y python3-pip python3-venv nodejs npm mariadb-server redis-server
pip3 install frappe-bench
```
