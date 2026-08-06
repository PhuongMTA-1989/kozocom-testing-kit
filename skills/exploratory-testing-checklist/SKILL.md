---
name: exploratory-testing-checklist
description: "Generate an exploratory testing checklist/charter set tailored to a specific project, based on project documentation (uploaded PDF, Word, spec, README...) or a project URL (a live website/app, docs site, GitHub repo...). Use this skill when the user asks for an 'exploratory testing checklist', 'test charter', 'session-based testing', or wants an unscripted testing guide to uncover bugs/edge cases. Do NOT use for a quick pre-release smoke test (use the smoke-test-checklist skill instead) or for detailed/scripted test cases."
---

# Exploratory Testing Checklist Generator

This skill produces an exploratory testing checklist/charter set as a Markdown (.md) file, tailored to the ACTUAL functionality of a specific project. Unlike smoke testing (a quick pass/fail check of core flows), exploratory testing focuses on charter-based, directed exploration to uncover bugs, unexpected behavior, and edge cases — it does not follow a fixed, step-by-step script.

## Process

### Step 1 — Identify the input
The user may provide one or more of the following:
- **Project documentation**: an uploaded file (PDF, Word, Markdown, technical spec, README, API docs, user stories...). Use the corresponding `file-reading` / `pdf-reading` / `docx` skill to read the content if the file isn't already in context.
- **Project URL**: a live app/website, a docs page, or a repo (GitHub/GitLab...). Use `web_fetch` to retrieve the page content. For a GitHub repo, prioritize fetching the README, and if needed, try reasonable sub-paths (docs/, CONTRIBUTING.md) — only fetch URLs that already appeared in the conversation or in returned results; never invent a path.
- If the user only describes the project verbally (no file/URL), ask one clarifying question to obtain a document or URL before proceeding.

If the user provides multiple sources, read all of them before drafting the charters.

### Step 2 — Extract project information
From the documentation/URL, determine:
1. **System type**: web app, mobile app, API, internal system, e-commerce, B2B SaaS...
2. **Core functional areas** to explore — e.g. sign up/login, search, cart, checkout, file upload...
3. **High-risk / complex areas**: places bugs are likely to hide — calculation logic, multi-step flows, large data handling, concurrency, third-party integrations, input validation.
4. **External integrations**, if any: payment gateway, email/SMS, third-party APIs, social login...
5. **User roles / permissions**, if any (admin, user, guest...) — each role is a distinct exploration angle.
6. **Platform/environment** involved (web, iOS, Android, cross-platform, multiple browsers/devices).

If the documentation doesn't clearly cover an aspect, leave it out rather than assuming.

### Step 3 — Draft charters using the Session-Based Test Management (SBTM) model
Each charter describes an exploration GOAL (not a fixed set of steps), using the formula:

> **Explore** <area/functionality>
> **With** <tools, data, or input conditions>
> **To discover** <type of issue to look for>

For each charter, also suggest:
- **Test ideas**: abnormal input, boundary values, off-path actions (back button, mid-flow refresh, double-submit, network loss), concurrent actions across multiple tabs/sessions, empty/oversized/special-character data, cross-role access.
- **Suggested duration**: each session 30–90 minutes, depending on the area's complexity.
- Do not write a charter for an area with no evidence in the documentation/URL.

Group charters by the project's actual area/module (name them using the terminology found in the documentation, not a forced generic framework).

Keep the number of charters focused on covering high-risk areas and core flows — prioritize the quality of exploration questions over quantity.

### Step 4 — Create the file
Use `create_file` to create a `.md` file in `/mnt/user-data/outputs/`, named `exploratory-testing-checklist-<project-name>.md` (using the inferred project name, lowercase, hyphen-separated). Structure the file according to the template below. Then use `present_files` to deliver it to the user — no need for a lengthy explanation after presenting the file.

## Checklist file template

```markdown
# Exploratory Testing Checklist — <Project Name>

**Project:** <project name>
**Reference source:** <document name or URL used>
**Version/Build:** ___________________________
**Tester:** ___________________________
**Date:** ___________________________
**Environment:** ☐ Dev ☐ Staging ☐ Production

> Exploratory testing — directed, charter-based exploration, not a fixed script. Log any unusual behavior even if you're not sure it's a bug.

---

## Charter 1 — <Area/Feature Name>
- **Explore:** <area/functionality>
- **With:** <tools/data/input conditions>
- **To discover:** <type of issue to look for>
- **Suggested duration:** ___ minutes

**Suggested test ideas:**
- [ ] <test idea 1 — e.g. boundary values / special characters>
- [ ] <test idea 2 — e.g. off-path actions, back/refresh mid-flow>
- [ ] <test idea 3>

**Notes/issues found:**
_________________________________________________

## Charter 2 — <Another Area/Feature>
...

<!-- Add a charter for each risk area/core feature found in the documentation/URL -->

---

## Session Summary

| Charter | Actual time | Issues found | Severity |
|---------|-------------|--------------|----------|
|         |             |              |          |

**Overall assessment:** ___________________________
**Tester signature:** ___________________________
```

## Notes
- Never invent areas/features not present in the documentation/URL — if information is missing, skip it rather than guess.
- This is NOT a fixed step-by-step pass/fail checklist like a regular test case — the goal is to direct exploration; the tester is free to follow a lead if they notice something unusual mid-session.
- If the documentation is very large, prioritize reading: overview, feature list, user flows, and areas with complex logic (validation, calculations, integrations).
- If the user needs a quick pre-release pass/fail check instead, use the `smoke-test-checklist` skill instead of this one.
- If the user later wants a Word (.docx) version instead of Markdown, use the `docx` skill to convert.
