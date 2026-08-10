## Mandatory Atrin Code Reuse Gate

> **ALL AGENTS AND DEVELOPERS MUST COMPLETE THIS GATE BEFORE MERGING ANY FUNCTIONAL CHANGE.**
>
> This is a mandatory project rule, not an optional recommendation.

### Required search order

- [ ] **Frappe** searched first
- [ ] **ERPNext** searched second
- [ ] **Frappe Helpdesk** searched third
- [ ] Existing suitable implementation identified, or searches documented as negative

### Reuse decision

- [ ] Existing implementation is suitable → **Reuse / Extend**
- [ ] No suitable implementation exists → **Atrin-specific code is justified**

### Evidence

**Frappe:**
<!-- Repository path(s), commit(s), or search terms. -->

**ERPNext:**
<!-- Repository path(s), commit(s), or search terms. -->

**Helpdesk:**
<!-- Repository path(s), commit(s), or search terms. -->

**Decision:**
<!-- Explain what is reused/extended, or why custom code is necessary. -->

### Enforcement

A PR that does not complete this section is **not ready for merge**. Reviewers/agents must reject or return it for completion when the required reuse investigation is missing.

See `docs/development/CODE-REUSE-POLICY.md` for the authoritative policy.
