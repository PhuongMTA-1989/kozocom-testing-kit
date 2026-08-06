---
name: smoke-test-checklist
description: "Generate a smoke test checklist tailored to a specific project, based on project documentation (uploaded PDF, Word, spec, README...) or a project URL (a live website/app, docs site, GitHub repo...). Use this skill whenever the user asks for a 'smoke test checklist', 'smoke test', 'quick pre-release/deploy check', or provides a project document/URL and wants to quickly verify core functionality before release. Do NOT use for detailed test cases, a full test plan, or comprehensive regression testing — this skill focuses only on a quick, core-functionality checklist."
---

# Smoke Test Checklist Generator

This skill produces a smoke test checklist as a Markdown (.md) file, tailored to the ACTUAL functionality of a specific project — not a generic checklist. The checklist must be inferred from evidence gathered from the documentation or URL the user provides.

## Process

### Step 1 — Identify the input
The user may provide one or more of the following:
- **Project documentation**: an uploaded file (PDF, Word, Markdown, technical spec, README, API docs, user stories...). Use the corresponding `file-reading` / `pdf-reading` / `docx` skill to read the content if the file isn't already in context.
- **Project URL**: a live app/website, a docs page, or a repo (GitHub/GitLab...). Use `web_fetch` to retrieve the page content. For a GitHub repo, prioritize fetching the README, and if needed, try reasonable sub-paths (docs/, CONTRIBUTING.md) — only fetch URLs that already appeared in the conversation or in returned results; never invent a path.
- If the user only describes the project verbally (no file/URL), ask one clarifying question to obtain a document or URL before proceeding — a project-specific checklist needs concrete evidence, not guesswork.

If the user provides multiple sources, read all of them before writing the checklist.

### Step 2 — Extract project information
From the documentation/URL, determine:
1. **System type**: web app, mobile app, API, internal system, e-commerce, B2B SaaS...
2. **Core user flows** — e.g. sign up/login, create an order, checkout, search, file upload, submit a report... This is the most important part: list the ACTUAL features present in the documentation/project, never insert a feature with no evidence.
3. **External integrations**, if any: payment gateway, email/SMS, third-party APIs, social login...
4. **User roles / permissions**, if any (admin, user, guest...).
5. **Platform/environment** involved (web, iOS, Android, cross-platform) to determine whether a responsive/cross-platform section is needed.

If the documentation doesn't clearly cover an aspect (e.g. no payment feature), leave that section out of the checklist rather than including an empty or assumed item.

### Step 3 — Draft the checklist
The checklist has 2 parts:

**A. Baseline framework (kept the same for every project)** — infrastructure items that always need checking regardless of the project:
- Build/deploy succeeds, app starts without errors
- Backend/database connection works
- No critical console/log errors
- Basic load time is acceptable, no timeouts on basic actions

**B. Project-specific section (the main focus, the bulk of the checklist)** — generated from Step 2, written as concrete, checkable action items. For each core flow found, write clearly:
- The action to perform (e.g. "Add a product to cart and complete checkout successfully")
- The expected result, if not obvious

Group items by the project's actual feature/module (don't force a generic "Authentication/Navigation/UI..." grouping if the project has a different structure — name groups using the actual terminology/modules found in the documentation).

Keep the checklist SHORT — the goal is 15–30 minutes of manual execution, not exhaustive testing. Prioritize coverage of core flows over item count.

### Step 4 — Create the file
Use `create_file` to create a `.md` file in `/mnt/user-data/outputs/`, named `smoke-test-checklist-<project-name>.md` (using the inferred project name, lowercase, hyphen-separated). Structure the file according to the template below. Then use `present_files` to deliver it to the user — no need for a lengthy explanation after presenting the file.

## Checklist file template

```markdown
# Smoke Test Checklist — <Project Name>

**Project:** <project name>
**Reference source:** <document name or URL used>
**Version/Build:** ___________________________
**Tester:** ___________________________
**Date:** ___________________________
**Environment:** ☐ Dev ☐ Staging ☐ Production

> Smoke test — a quick check of core flows before deeper testing. If a critical item FAILS, you may stop and report immediately.

---

## 1. Infrastructure & Startup
- [ ] Build/deploy succeeds, no installation errors
- [ ] App starts, no crashes
- [ ] Backend/database connection works
- [ ] No critical console/log errors

## 2. <Module/Feature 1 — matching the actual project>
- [ ] <concrete action 1>
- [ ] <concrete action 2>

## 3. <Module/Feature 2>
- [ ] ...

<!-- Add sections for each core feature found in the documentation/URL -->

## N. Basic Performance & Security
- [ ] Basic load/response time is acceptable
- [ ] Permission-restricted features are inaccessible when not logged in / lacking permission

---

## Overall Result
☐ PASS ☐ FAIL

**Issues found:**

| # | Item | Issue description | Severity |
|---|------|--------------------|----------|
|   |      |                    |          |

**Tester signature:** ___________________________
```

## Notes
- Never invent features not present in the documentation/URL — if information about an aspect is unclear (e.g. unsure whether admin permissions exist), skip it rather than guess.
- If the documentation is very large (a long spec, many docs pages), prioritize reading: overview, feature list, user flows, main API endpoints — no need to read every implementation detail.
- If the user later wants a Word (.docx) version instead of Markdown, use the `docx` skill to convert.
