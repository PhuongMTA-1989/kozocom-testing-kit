---
name: generate-kozocom-testcase-workbook
description: Create a Kozocom-format testcase workbook (.xlsx) from source documents or spec descriptions. Use when the user needs to turn requirement notes, BRD/SRS excerpts, user stories, UI flows, API specs, bug tickets, or change requests into a filled Excel testcase file that matches the Kozocom template, instead of returning plain-text testcases. Trigger on "gen testcase", "viết testcase", "tạo test case", "làm test case cho chức năng X", "Kozocom testcase template", or any request to turn a requirement into a testcase Excel file.
---

# Generate Kozocom Testcase Workbook

Use the bundled Excel template and renderer script to produce a workbook that
keeps the Kozocom layout, formulas, merged cells, validations, and header
structure intact. Design the testcase content first, then render the
spreadsheet from a normalized JSON payload instead of editing cells ad hoc.

## Workflow

1. **Read the source artifact.**
   Accept raw spec text, requirement notes, `.docx`, `.pdf`, screenshots, bug
   tickets, or change descriptions. Use the `docx`/`pdf`/`pdf-reading` skills
   if the source needs deep extraction; use `view` directly for images.

2. **Extract testable statements before writing cases.**
   Separate `explicit requirements`, `assumptions`, `open questions`, and
   `out-of-scope items`. If ambiguity would materially change testcase scope
   (e.g. an unstated field length limit you'd otherwise have to invent), ask
   one blocking question before proceeding — otherwise proceed with stated
   assumptions and note them at the end.

3. **Design testcases per target item, aiming for thorough coverage.**
   For each field/screen/button/flow, cover as many of the following groups
   as genuinely apply (skip groups that don't apply — don't force them):
   - **Happy path** — valid input/typical flow
   - **Validation** — required-field empty, wrong format (email, phone,
     date...), wrong data type
   - **Boundary value** — exact min, exact max, min-1, max+1, zero/negative
     for numbers, empty string, string at the exact length limit and limit+1
   - **Business edge case** — double-submit, refresh mid-flow, dependent
     data deleted/changed elsewhere, network drop mid-action
   - **Basic security** — SQL injection characters (`' OR '1'='1`), XSS
     (`<script>alert(1)</script>`), unauthorized access when not logged in
     or under-privileged, tampering with URL/API params to reach another
     user's data
   - **Permission/regression** — role-based access differences, and a small
     regression ring around anything the change modifies

4. **Normalize the testcase rows into JSON.**
   Read [references/input-schema.md](references/input-schema.md) for the
   exact `metadata` + `cases` contract and
   [references/template-mapping.md](references/template-mapping.md) for what
   every cell/column means. Write the payload to e.g. `/tmp/testcases.json`.

5. **Render the workbook from the template.**
   ```bash
   pip install openpyxl --break-system-packages   # if not already available
   python3 scripts/render_testcase_workbook.py \
     --input /absolute/path/to/testcases.json \
     --output /mnt/user-data/outputs/Testcase-<FeatureName>.xlsx
   ```

6. **Verify the workbook** (see Verification Checklist below), then present
   the file to the user with `present_files`.

## Output Rules

- Always generate the final deliverable as `.xlsx`.
- Always render from `assets/kozocom-testcase-template.xlsx` — never hand-build
  the layout from scratch, and never reuse a template the user uploaded in an
  earlier turn (this bundled copy is the canonical one).
- Fill testcase design columns first: `A:I`. Leave execution columns `J:X`
  blank/default (`NT` status) unless the user explicitly supplies round
  status, bug IDs, dates, testers, or memos.
- Content language: write all testcase content (Target Item, Precondition,
  Testcase, Steps, Data test, Expected) in **English** by default. If the
  user's requirement/spec is in Vietnamese or Japanese and they haven't
  specified otherwise, ask once; don't silently guess between languages.
- Use `VN` as the default locale marker in column `A` (this is just the
  sheet's language-convention flag, independent of the content language)
  unless the source clearly requires `JP`.
- If the source does not provide `Type`, pick the closest of: `Display`,
  `Default`, `Function`, `Validate`, `Transition`, `Operation` — these are
  the only values the sheet's dropdown accepts.

## Source Handling

- For `.docx`, use the `docx` skill (or `python-docx` directly) to extract
  text when a plain read isn't enough.
- For `.pdf`, use the `pdf-reading` skill (or `pypdf`) to extract text.
- For screenshots or UI mockups, infer only visible behaviors and explicitly
  label non-visible business rules as assumptions rather than inventing them.
- For bug tickets or change requests, focus on delta coverage first, then add
  the smallest credible regression ring around what changed.

## Verification Checklist

Before presenting the file, confirm:
- `G2`, `J2`, `B9`, `B10`, `B12` reflect the provided metadata when present,
  and are left at their template defaults when not provided.
- Rows `13:14` (headers) are untouched.
- Data starts at row `15`, one row per case, in the order designed.
- Column `B` is numbered by formula (`=(ROW()-(ROW($B$14)))`) only for
  populated testcase rows.
- Rows after the last populated case (up to at least row 40, or further if
  more than 26 cases were rendered) have their leftover `No`-formula cleared
  — otherwise the sheet's summary stats overcount total testcases (see
  "Tail row cleanup" in [references/template-mapping.md](references/template-mapping.md)).
- Column `D` values are all one of the six valid dropdown options.
- The generated workbook opens without an Excel repair prompt.

## References

- [references/input-schema.md](references/input-schema.md) — the JSON
  contract passed to the renderer (`metadata` + `cases`).
- [references/template-mapping.md](references/template-mapping.md) — Kozocom
  column semantics, header cell mapping, and the tail-row cleanup quirk.
