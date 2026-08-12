# ⚠️ DEPRECATED — Service Case DocType

**وضعیت:** این DocType در حال حذف است.
**تاریخ deprecation:** 2026-08-11
**جایگزین:** Frappe Helpdesk `HD Ticket` (Extended)

## چرا حذف می‌شود

طبق UPSTREAM-REUSE-AUDIT-01، Helpdesk HD Ticket قابلیت‌های زیر را دارد که Service Case ما ندارد:

- ✅ SLA tracking (response_by, resolution_by)
- ✅ Response time metrics
- ✅ Agent/Team assignment (HD Team)
- ✅ Priority management
- ✅ Hold/Suspension tracking
- ✅ Resolution time logging
- ✅ Email integration
- ✅ Customer portal

## Migration path

```text
Atrin Service Case  →  Helpdesk HD Ticket (Extended)
         ↓                        ↓
   case.status          hd_ticket.status
   case.citizen         hd_ticket.custom_citizen
   case.service         hd_ticket.custom_service
   case.office          hd_ticket.custom_office
   case.queue_ticket    hd_ticket.custom_queue_ticket
   case.resolution      hd_ticket.resolution_details
   case.opened_at       hd_ticket.opening_date + opening_time
   case.completed_at    hd_ticket.resolution_date
```

## وضعیت فعلی

- **از این DocType استفاده نکنید.**
- **Feature development روی آن متوقف شده.**
- **Migration script بعد از environment validation نوشته می‌شود.**
- **حذف نهایی: پس از migration موفق و تأیید.**

مستندات کامل: [UPSTREAM-REUSE-AUDIT-01.md](../../../docs/architecture/UPSTREAM-REUSE-AUDIT-01.md)
مستندات migration: [SERVICE-CASE-MIGRATION-PLAN.md](../../../docs/development/SERVICE-CASE-MIGRATION-PLAN.md)
