---
name: log-bug
description: Create, rewrite, or review Backlog-ready QA bug reports from test notes, failed test cases, screenshots, videos, logs, or user reports. Use when asked to document a reproducible defect, standardize a Backlog issue, assess severity, or distinguish actual results from expected results.
---

# Log QA Bugs for Backlog

Create clear, neutral, and reproducible bug reports that render cleanly in a Backlog issue. This skill uses Backlog-compatible Markdown and remains usable in Codex, Claude, Jira, Notion, or plain Markdown.

## Gather information

Extract the supplied feature or URL, environment, build or version, browser or device, test account or role, preconditions, reproduction steps, actual result, expected result, and evidence.

Do not invent URLs, credentials, expected behavior, or root causes. Mark missing required information as `[Not provided]` and ask a short, purposeful follow-up question.

## Workflow

1. Identify one distinct defect. Split independent defects into separate tickets.
2. Write a concise issue title using: `[Module] Incorrect behavior when Condition`.
3. Keep `Actual Result` and `Expected Result` separate. Base the expected result on the requirement, test case, or confirmed behavior.
4. Write ordered reproduction steps that another person can follow without guessing.
5. Assign severity based on actual impact. If the evidence is insufficient, propose a level and state the assumption.
6. Attach or list evidence: screenshot, video, log, request/response, console error, or test case ID.
7. Redact passwords, tokens, customer data, and other sensitive information from the ticket and evidence.

## Severity guide

- `Blocker`: Core testing or core usage cannot continue and no practical workaround exists.
- `Critical`: Data loss, a serious security defect, or major impact on core business operations.
- `Major`: An important feature behaves incorrectly but has a workaround or limited scope.
- `Minor`: A small functional, validation, UI, or usability defect that does not block the main flow.
- `Trivial`: A very low-impact copy or visual issue.

Severity represents impact. Do not infer priority unless the project rules define it.

## Backlog output rules

- Return `Issue title` separately from `Issue description`; do not repeat the title as a heading in the description.
- Format the description with Backlog Markdown headings (`## `), bullets, and numbered lists.
- Put a blank line before every list and between sections so Backlog renders the layout correctly.
- Use numbered lists for reproduction steps. Do not put steps into a table.
- Use a table only for short, single-line metadata. Use bullets when a value may be long.
- Refer to attached evidence by its filename. Do not claim a file is attached unless it was supplied.

## Required output

Return exactly these two blocks. The second block must be ready to paste into Backlog's **Description** field.

**Issue title**

```text
[Severity] [Module] Concise defect title
```

**Issue description (Backlog Markdown)**

```md
## Test item

- Test case / Requirement: ...
- URL / Screen: ...
- Environment / Build: ...
- Browser / Device: ...
- Test account / Role: ...
- Frequency: Always / Intermittent / Once

## Preconditions

1. ...

## Steps to reproduce

1. ...
2. ...

## Actual result

...

## Expected result

...

## Impact

- Severity: ...
- Impact: ...
- Workaround: ...

## Evidence

- Screenshot / Video / Log: ...
```

Write the title and body in the language requested by the user. If no language is requested, use clear English. Do not assign blame or state an unverified root cause.

## Quality gate

Before delivering, confirm that the title describes one defect, the steps are executable, actual and expected results do not conflict, severity has a rationale, environment and evidence are captured, sensitive data is redacted, unknown information is clearly marked, and the description follows the Backlog output rules.
