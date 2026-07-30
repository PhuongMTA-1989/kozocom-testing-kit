---
name: generate-checklist-workbook
description: Create a screen-by-screen verification checklist workbook (.xlsx) in English — columns Screen/Process, No, Check Point, Pattern, Expected Result — from a requirement, spec, or reference checklist (including one shown as an image/screenshot). Use when the user asks for a "checklist", "confirmation point list", "画面確認チェックリスト"-style deliverable, or wants to translate/rebuild an existing Japanese checklist into English, as distinct from the full Kozocom testcase workbook (which has Precondition/Steps/Data-test columns and round-tracking). Trigger on "tạo checklist", "gen checklist", "checklist tiếng Anh", or a screenshot of a Screen/確認ポイント/パターン/期待結果-style table.
---

# Generate Checklist Workbook

Produce a lightweight verification checklist — one row per check, grouped by
screen/process — as an `.xlsx` file in English. This is a simpler, flatter
sibling of the Kozocom testcase workbook: no Precondition/Steps/Data-test/
round-tracking columns, just **Check Point → Pattern → Expected Result**,
organized under a Screen/Process heading.

## When to use this vs. the testcase workbook skill

- Use **this skill** when the deliverable is a compact confirmation/checklist
  matrix (what the source image showed): screen name, a check-point category,
  a specific pattern, and the expected result — no step-by-step reproduction
  instructions and no execution/round tracking.
- Use `generate-kozocom-testcase-workbook` when the user needs the full
  Kozocom testcase format with Precondition, Steps to perform, Data test, and
  Round 1/2/3 execution tracking.
If unclear which one fits, default to this simpler checklist skill — it's
easy to say "actually I need step-by-step testcases too" afterward.

## Workflow

1. **Read the source.**
   Accept a requirement/spec description, an existing checklist (in any
   language, including a screenshot/image of one), or a mix. If it's an
   image, read it directly (the check points, patterns, and expected results
   are usually visible as table cells) — don't ask the user to re-type it.

2. **Group by screen/process.**
   Identify each distinct screen, batch job, or process block first (e.g.
   "Coupon Issuance", "Bulk Coupon Assignment", "EC→Core Campaign Master
   Sync batch"). All checklist rows for one block must be written together
   and in one pass — the renderer restarts numbering and merges cells based
   on this grouping, so don't interleave two screens' rows.

3. **Within each screen, break down check points.**
   Typical check-point categories (use whichever genuinely apply, translate
   to English, don't force categories that don't exist in the source):
   `Initial Display`, `Input`, `Search`, `Register/Update`, `Delete`,
   `Row selection`, `Column header click / sort`, `Navigation`, `Validation`,
   `Permission`. For each check point, list every distinct pattern (specific
   condition/case) with its own concrete, verifiable expected result — avoid
   vague expected results like "works correctly."

4. **Translate faithfully, don't paraphrase away specifics.**
   When rebuilding from a Japanese (or other language) source, keep exact
   technical details: field names, character limits (`maxLength=250`),
   colors/highlighting rules, screen names, button labels, batch script
   names. These are load-bearing details for a QA reader — don't summarize
   them into vaguer English.

5. **Normalize into JSON** per
   [references/input-schema.md](references/input-schema.md): an `items`
   array of `{screen, check_point, pattern, expected_result, highlight}`.

6. **Render the workbook.**
   ```bash
   pip install openpyxl --break-system-packages   # if not already available
   python3 scripts/render_checklist_workbook.py \
     --input /absolute/path/to/checklist.json \
     --output /mnt/user-data/outputs/Checklist-<FeatureName>.xlsx
   ```

7. **Verify**, then present the file with `present_files`:
   - Each screen's `No` column restarts at 1.
   - Screen/Check Point cells are merged for consecutive identical values,
     not repeated on every row.
   - No `highlight: true` overuse — it should mark a handful of
     attention-worthy rows, not most of the sheet.
   - All content is in English.

## Output Rules

- Always render from `assets/checklist-template.xlsx` via the script — don't
  hand-build the sheet cell by cell.
- Content language: **English**, always, regardless of the source language.
- Keep `pattern` and `expected_result` specific and testable — one concrete
  condition and one concrete, checkable outcome per row, not a bundled list
  of several checks in one cell.
- Don't add columns beyond the five in the template unless the user
  explicitly asks for more (e.g. adding back a Steps or Precondition column —
  in that case, consider whether `generate-kozocom-testcase-workbook` is a
  better fit instead).

## References

- [references/input-schema.md](references/input-schema.md) — the JSON
  contract passed to the renderer, with a worked example.
