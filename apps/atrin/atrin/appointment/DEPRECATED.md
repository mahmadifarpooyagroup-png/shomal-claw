# ⚠️ DEPRECATED — Appointment DocType

**وضعیت:** این DocType در حال حذف است.
**تاریخ deprecation:** 2026-08-11
**جایگزین:** ERPNext `Appointment` (Extended)

## چرا حذف می‌شود

طبق UPSTREAM-REUSE-AUDIT-01، ERPNext Appointment قابلیت‌های زیر را دارد:

- ✅ Slot timing validation
- ✅ Holiday checking
- ✅ Advanced booking limits
- ✅ Calendar event integration
- ✅ Email verification
- ✅ Portal creation
- ✅ Assignment

Atrin Appointment فعلی فقط ۶ فیلد ساده دارد بدون هیچ business logic.

## Migration path

```text
Atrin Appointment  →  ERPNext Appointment (Extended)
         ↓                        ↓
   apt.citizen           apt.party (Dynamic Link → Citizen)
   apt.service           apt.custom_service
   apt.office            apt.custom_office
   apt.appointment_date  apt.scheduled_time
   apt.status            apt.status (Extended: add "Checked In", "No Show")
```

## وضعیت فعلی

- **از این DocType استفاده نکنید.**
- **Feature development روی آن متوقف شده.**
- **Migration script بعد از environment validation نوشته می‌شود.**
- **حذف نهایی: پس از migration موفق و تأیید.**

مستندات کامل: [UPSTREAM-REUSE-AUDIT-01.md](../../../docs/architecture/UPSTREAM-REUSE-AUDIT-01.md)
