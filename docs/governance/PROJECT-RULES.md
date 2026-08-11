# Atrin Project Rules — Governance

**نسخه:** 1.0
**تاریخ تصویب:** 2026-08-11
**وضعیت:** Active
**مالک:** Architecture

---

## قانون شماره یک — Reuse First (اجباری)

**Frappe → ERPNext → Helpdesk → Reuse/Extend → فقط در صورت نبودن، کد اختصاصی**

برای **هر قابلیت**:

```text
نیاز Atrin
   ↓
Frappe
   ↓
ERPNext
   ↓
Helpdesk
   ↓
کد آماده؟
 ┌───────┴───────┐
بله              خیر
 ↓                ↓
Reuse/Extend   Custom Atrin
```

هیچ Agent یا Developer حق ندارد این مرحله را دور بزند.

---

## ۱. هدف پروژه

ساخت **Atrin Smart Service Platform (ASSP)** — یک پلتفرم حرفه‌ای برای مدیریت و اجرای خدمات پیشخوان، با قابلیت توسعه به یک سیستم سازمانی کامل.

هدف صرفاً یک نرم‌افزار ساده پیشخوان نیست؛ از **بهترین قابلیت‌های نرم‌افزارهای موجود** استفاده می‌کنیم و فقط جاهایی که لازم است خودمان توسعه می‌دهیم.

---

## ۲. نقش AI/Agent در پروژه

AI باید نقش **معمار + مدیر فنی پروژه + ناظر اجرای Agentها** را داشته باشد، نه صرفاً تولیدکننده کد.

یعنی:

- قبل از کدنویسی، نیاز را تحلیل کند
- معماری مصوب را حفظ کند
- کدهای آماده و قابل استفاده را پیدا کند
- از دوباره‌کاری جلوگیری کند
- تغییر معماری خودسرانه ندهد
- هر ایده جدید را قبل از اجرا اعلام کند
- اگر ایده‌ای فعلاً اجرا نشد، آن را در `docs/future/` ثبت کند
- هیچ Dependency یا Frameworkی را بدون دلیل نصب نکند
- کارهای قبلی پروژه را حفظ کند
- وضعیت واقعی GitHub را مبنا قرار دهد، نه حدس یا حافظه ناقص

---

## ۳. فلسفه معماری

**Reuse حداکثری + Custom حداقلی**

نمی‌خواهیم:

- ❌ Workflow خودمان را بی‌دلیل از صفر بسازیم
- ❌ Ticket Engine خودمان را بی‌دلیل بسازیم
- ❌ SLA را دوباره اختراع کنیم
- ❌ Assignment Engine را دوباره بسازیم
- ❌ Notification/Realtime را بدون بررسی دوباره بسازیم
- ❌ Appointment را از صفر بنویسیم

ابتدا باید ببینیم Frappe/ERPNext/Helpdesk چه چیزی آماده دارند و سپس **Reuse یا Extend** کنیم.

---

## ۴. معماری کلان

پروژه به شکل **Modular Monolith** شروع می‌شود، نه Microservices.

لایه‌بندی:

```text
Frappe
   ↓
Platform capabilities

ERPNext
   ↓
Business capabilities

Helpdesk
   ↓
Service/Support capabilities

Atrin
   ↓
Pishkhan-specific capabilities
```

هر چیزی که در Atrin قرار می‌گیرد باید ابتدا از Gate قانون شماره یک عبور کند.

---

## ۵. ویژگی مهم Atrin

Atrin فقط یک Helpdesk نیست — Helpdesk یکی از منابع مهم برای قابلیت‌های Case/Ticket/Agent/SLA است.

Atrin فقط ERPNext نیست — ERPNext نیز یکی از منابع قابلیت‌های آماده مثل Appointment و Issue است.

Frappe نقش بسیار مهمی به‌عنوان **Platform/Foundation** دارد.

---

## ۶. چیزهایی که مخصوص Atrin هستند

اگر بعد از Audit مشخص شود upstream مناسب ندارد، می‌توانیم برای موارد اختصاصی پیشخوان خودمان توسعه دهیم:

- Queue اختصاصی پیشخوان
- Call Next
- Counter-specific routing
- منطق خاص فراخوانی مراجع
- جریان‌های خاص Pishkhan
- نیازهای اختصاصی دولت/خدمات پیشخوان
- Offline-first و Sync (در صورت تأیید معماری)

**ولی حتی اینها هم قبل از Custom شدن باید Audit شوند.**

---

## ۷. Offline / Local Network Operation

یکی از الزامات مهم: سیستم عملیاتی پیشخوان باید بتواند در **شبکه محلی و بدون اینترنت** کار کند.

قطع اینترنت نباید باعث از کار افتادن هسته عملیاتی پیشخوان شود.

سرویس‌های زیر ممکن است به اتصال اینترنت وابسته باشند:
- APIهای دولتی خارجی
- SMS gateway
- سرویس‌های Cloud

---

## ۸. Helpdesk باید داخل سیستم باشد

Helpdesk قرار نیست یک لینک به سایت خارجی باشد. باید به‌صورت یک قابلیت داخلی در معماری Atrin قرار بگیرد، به شکلی که وابستگی عملیاتی به اینترنت نداشته باشد.

اینکه دقیقاً کدام بخش Helpdesk را Reuse و کدام بخش را Extend کنیم، باید بر اساس Audit و compatibility مشخص شود.

---

## ۹. Mobile

ایده‌هایی مثل **Frappe Mobile SDK** را نباید خودسرانه وارد پروژه کنیم.

اگر قابلیت موبایل جدیدی پیشنهاد شود:

1. اعلام به مالک پروژه
2. ذکر مزایا و معایب
3. اگر فعلاً اجرا نشود، ثبت در `docs/future/`

---

## ۱۰. نصب = بعد از تصمیم معماری

**هیچ Framework، Runtime، Application یا Dependency صرفاً به خاطر اینکه «شاید بعداً لازم شود» نصب نشود.**

ترتیب صحیح:

```text
تصمیم معماری → نصب
```

نه:

```text
نصب → تصمیم معماری ❌
```

---

## ۱۱. GitHub مرجع پروژه است

Repository: `mahmadifarpooyagroup-png/shomal-claw`

اطلاعات مهم پروژه باید داخل Repository مستند شود تا وابسته به حافظه یک Agent نباشد.

---

## ۱۲. PR باید قابل بررسی باشد

هر تغییر مهم باید نشان دهد:

```text
Atrin Requirement
        ↓
Frappe Audit
        ↓
ERPNext Audit
        ↓
Helpdesk Audit
        ↓
Reuse / Extend decision
        ↓
Implementation
```

اگر Custom شده، باید **دلیل مستند** داشته باشد.

PR Template اجباری در `.github/pull_request_template.md` تعریف شده است.

---

## ۱۳. قوانین Commit و Push

1. اول بررسی وضعیت (`git status`)
2. بررسی معماری و نیازمندی
3. بررسی قابلیت‌های موجود Frappe/ERPNext/Helpdesk
4. تصمیم معماری
5. پیاده‌سازی کوچک و مرحله‌ای
6. Test / Validation
7. `git diff --check`
8. بررسی تغییرات staged
9. Commit با پیام معنادار
10. Push → GitHub
11. CI / بررسی GitHub
12. مرحله بعد

**قبل از Push:** مالک پروژه از خطرات تغییرات مطلع می‌شود. بدون تأیید مرحله حساس، Push انجام نمی‌شود.

---

## ۱۴. چیزهایی که انجام نمی‌دهیم

- ❌ صرفاً سریع کد نوشتن (بدون تحلیل)
- ❌ هر Framework جدیدی پیشنهاد دادن
- ❌ معماری را هر بار عوض کردن
- ❌ Frappe/ERPNext/Helpdesk را کورکورانه نصب کردن
- ❌ قابلیت موجود را دوباره از صفر نوشتن
- ❌ ایده جدید را بدون اطلاع مالک اجرا کردن
- ❌ اطلاعات و تصمیمات قبلی پروژه را نادیده گرفتن
- ❌ Commitهای بزرگ و غیرقابل ردیابی

---

## ۱۵. وضعیت فعلی پروژه

در حال حاضر در مرحله **Architecture + Upstream Audit** هستیم.

برای ورود به مرحله اجرا، نیازمند:
1. راه‌اندازی Frappe Bench v15 در WSL
2. نصب ERPNext v15 + Helpdesk
3. Verify runtime availability of Appointment (ERPNext) و HD Ticket (Helpdesk)
4. Migration از custom DocTypeها به upstream
5. Integration layer بین Queue/Counter و upstream

---

## ۱۶. خلاصه — اصل راهنمای کل پروژه

> **Atrin باید یک Modular Monolith حرفه‌ای و مستقل باشد که با استفاده حداکثری از قابلیت‌ها و کدهای Frappe، ERPNext و Helpdesk ساخته می‌شود؛ هر قابلیت ابتدا در همین سه منبع بررسی و Reuse/Extend می‌شود و فقط در صورت نبودن راهکار مناسب، کد اختصاصی Atrin نوشته می‌شود؛ با حفظ Offline/Local operation، معماری مصوب، مستندسازی GitHub و کنترل اجباری Agentها.**

---

## Appendices

- [CODE-REUSE-POLICY.md](../development/CODE-REUSE-POLICY.md) — سیاست اجرایی Reuse
- [INTEGRATION-POINTS.md](../development/INTEGRATION-POINTS.md) — نقاط اتصال به upstream
- [ENVIRONMENT-VALIDATION.md](../development/ENVIRONMENT-VALIDATION.md) — Gate اعتبارسنجی محیط
- [SERVICE-CASE-MIGRATION-PLAN.md](../development/SERVICE-CASE-MIGRATION-PLAN.md) — طرح migration
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — سند معماری
