# UPSTREAM-REUSE-AUDIT-01 — Frappe Helpdesk & ERPNext

**تاریخ:** 2026-08-11
**منبع:** GitHub source code direct inspection
**نسخه‌های بررسی‌شده:** ERPNext v15, Frappe Helpdesk main

---

## ERPNext Appointment

**مسیر:** `erpnext/crm/doctype/appointment/appointment.json`
**ماهیت:** CRM-oriented — برای مشتری/lead طراحی شده

### فیلدهای موجود

| فیلد | نوع | توضیح |
|------|-----|-------|
| customer_name | Data | نام مشتری |
| customer_phone_number | Data | تلفن |
| customer_skype | Data | Skype |
| customer_email | Data (Email) | ایمیل |
| customer_details | Long Text | جزئیات |
| scheduled_time | Datetime | زمان ملاقات |
| status | Select | Open / Unverified / Closed |
| appointment_with | Link (DocType) | نوع طرف مقابل |
| party | Dynamic Link | ارجاع به طرف |
| calendar_event | Link (Event) | رویداد تقویم |
| created_through_portal | Check | ساخته‌شده از پرتال |
| email_verified | Check | ایمیل تأییدشده |
| verification_token | Data | توکن تأیید |

### قابلیت‌های Python (appointment.py)

- `validate()` — اعتبارسنجی وضعیت، زمان گذشته، تعطیلی، بازه زمانی
- `is_appointment_scheduling_enabled()` — بررسی تنظیمات
- `validate_advanced_booking()` — محدودیت رزرو پیشرفته
- `validate_holiday()` — بررسی تعطیلی
- `validate_slot_timing()` — بررسی بازه زمانی
- `validate_available_time_slot()` — بررسی در دسترس بودن
- `add_assignment()` — ارجاع وظیفه
- `add_docshare()` — اشتراک‌گذاری سند

### شکاف‌ها برای Atrin

| نیاز Atrin | وضعیت | اقدام |
|-----------|--------|-------|
| Citizen (نه CRM Customer) | ❌ ندارد | Extend — اضافه کردن Link به Citizen |
| Service/Office | ❌ ندارد | Extend — اضافه کردن Link به Service, Office |
| Queue Ticket linkage | ❌ ندارد | Atrin integration layer |
| Check-in workflow | ❌ ندارد | Extend یا Atrin workflow |
| Status > 3 حالت | ❌ فقط ۳ حالت | Extend (یا Workflow سفارشی) |
| Multi-service appointment | ❌ ندارد | Extend |
| Walk-in support | ❌ ندارد | Atrin Queue logic |

**تصمیم:** Extend (نه Direct Reuse). نیازمند custom fields + integration layer.

---

## Frappe Helpdesk HD Ticket

**مسیر:** `helpdesk/helpdesk/doctype/hd_ticket/hd_ticket.json`
**ماهیت:** Full ticket management system

### فیلدهای موجود (خلاصه)

#### Core
| فیلد | نوع | توضیح |
|------|-----|-------|
| subject | Data | موضوع |
| raised_by | Data | ایجادکننده (ایمیل) |
| status | Link (HD Ticket Status) | وضعیت |
| priority | Link (Priority) | اولویت |
| ticket_type | Link (Ticket Type) | نوع تیکت |
| agent_group | Link (HD Team) | تیم |
| description | Text Editor | شرح |

#### SLA
| فیلد | نوع | توضیح |
|------|-----|-------|
| sla | Link (SLA) | قرارداد SLA |
| response_by | Datetime | مهلت پاسخ |
| resolution_by | Datetime | مهلت حل |
| agreement_status | Select | وضعیت SLA |
| on_hold_since | Datetime | شروع تعلیق |
| total_hold_time | Duration | کل زمان تعلیق |

#### Response Tracking
| فیلد | نوع | توضیح |
|------|-----|-------|
| first_response_time | Duration | زمان اولین پاسخ |
| first_responded_on | Datetime | تاریخ اولین پاسخ |
| avg_response_time | Duration | میانگین زمان پاسخ |
| last_agent_response | Datetime | آخرین پاسخ اپراتور |
| last_customer_response | Datetime | آخرین پاسخ مشتری |

#### Resolution
| فیلد | نوع | توضیح |
|------|-----|-------|
| resolution_details | Text Editor | شرح حل |
| opening_date | Date | تاریخ باز شدن |
| opening_time | Time | زمان باز شدن |
| resolution_date | Datetime | تاریخ حل |
| resolution_time | Duration | زمان حل |
| user_resolution_time | Duration | زمان حل کاربر |

#### References
| فیلد | نوع | توضیح |
|------|-----|-------|
| contact | Link (Contact) | مخاطب |
| customer | Link (Customer) | مشتری |
| email_account | Link | حساب ایمیل |
| via_customer_portal | Check | از پرتال مشتری |

### قابلیت‌های کلیدی که Atrin Service Case ندارد

| قابلیت | HD Ticket | Atrin Service Case |
|--------|-----------|-------------------|
| SLA tracking | ✅ کامل | ❌ |
| Response time metrics | ✅ کامل | ❌ |
| Agent/Team assignment | ✅ HD Team | ❌ |
| Priority management | ✅ Priority doctype | ❌ |
| Ticket type classification | ✅ Ticket Type | ❌ |
| Hold/Suspension tracking | ✅ | ❌ |
| Email integration | ✅ | ❌ |
| Resolution time logging | ✅ | ❌ |
| Customer portal | ✅ | ❌ |

### شکاف‌ها برای Atrin

| نیاز Atrin | وضعیت | اقدام |
|-----------|--------|-------|
| Citizen (نه CRM Customer) | ❌ از Customer CRM استفاده می‌کند | Extend — Link به Citizen |
| Service/Office | ❌ ندارد | Extend — custom fields |
| Queue Ticket linkage | ❌ ندارد | Atrin integration layer |
| Counter/Operator assignment | ❌ HD Team (generic) | Extend — link به Counter |

**تصمیم:** Extend (Reuse کامل lifecycle + SLA + assignment). جایگزین کامل Atrin Service Case.

---

## Frappe Core — قابلیت‌های Platform

| قابلیت | Frappe | استفاده در Atrin |
|--------|--------|-----------------|
| **Auth / RBAC** | User, Role, Role Profile, User Permission | Direct Reuse ✅ |
| **ORM / DocType** | Document model, DB abstraction, migrations | Direct Reuse ✅ |
| **Workflow** | Workflow, Workflow State, Workflow Action, Transition | Extend برای Case lifecycle ✅ |
| **API** | REST API (auto-generated), Frappe Client | Direct Reuse ✅ |
| **Background Jobs** | Scheduler, Queue, Background workers | Direct Reuse ✅ |
| **Realtime** | Frappe Realtime (Socket.io) | Direct Reuse برای Call Next ✅ |
| **Notifications** | Email, System Notification, Push | Direct Reuse ✅ |
| **Files** | File, Attach, private/public files | Direct Reuse ✅ |
| **Reports** | Report Builder, Query Report, Script Report | Extend برای dashboards ✅ |
| **Permissions** | Role Permission, DocShare, User Permission | Direct Reuse ✅ |
| **Translations** | i18n support | Direct Reuse ✅ |
| **Web Forms** | Web Form Builder | Extend برای self-service ✅ |
| **Print Format** | Print Format Builder | Extend برای ticket print ✅ |
| **Audit / Versioning** | Track Changes, Version history | Direct Reuse ✅ |

---

## نتیجه‌گیری نهایی

### آنچه باید Reuse کنیم

| منبع | قابلیت | نحوه استفاده |
|------|--------|-------------|
| Frappe | Auth, ORM, Workflow, API, Jobs, Realtime | Direct Reuse |
| Frappe | Track Changes (Audit) | Direct Reuse |
| ERPNext | Appointment (Extended) | Reuse + Custom Fields |
| Helpdesk | HD Ticket (Extended) | Reuse + Custom Fields + Integration |
| Helpdesk | SLA engine | Direct Reuse |
| Helpdesk | Assignment engine | Direct Reuse |

### آنچه باید Custom Atrin باشد

| قابلیت | دلیل Custom |
|--------|------------|
| Queue Ticket + numbering | منطق اختصاصی پیشخوان — upstream ندارد |
| Counter + Call Next | منطق اختصاصی — upstream ندارد |
| Citizen (domain master) | متفاوت از CRM Customer |
| Service Registry | خاص Pishkhan — upstream ندارد |
| Government Integration | خاص دولت — upstream ندارد |
| Offline sync layer | نیاز عملیاتی پیشخوان |

### تغییرات لازم در Atrin DocTypeها

| DocType فعلی | اقدام |
|-------------|--------|
| `Service Case` | ❌ حذف — جایگزین با HD Ticket (Extended) |
| `Appointment` (custom) | ❌ حذف — جایگزین با ERPNext Appointment (Extended) |
| `Queue Ticket` | ✅ حفظ — اضافه کردن link به HD Ticket |
| `Counter` | ✅ حفظ |
| `Citizen` | ✅ حفظ |
| `Service` | ✅ حفظ |
| `Organization` | ✅ حفظ |
| `Office` | ✅ حفظ |
