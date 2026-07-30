# Kozocom Template — Cell & Column Mapping

Reference for `assets/kozocom-testcase-template.xlsx`, sheet name `Template`.
Do not rename the sheet or restructure rows 1-14; every formula below depends
on the existing row/column positions.

## Header metadata block (rows 1-12)

| Cell(s) | Label | Meaning |
|---|---|---|
| `F2` (label) / `G2:H3` (value) | 環境 / Test environment | e.g. `STG`, `PROD` |
| `I2` (label) / `J2:L2` (value) | ブラウザ / Browser | Browser or device + version |
| `A9` (label) / `B9:D9` (value) | CREATED BY | Author/tester name |
| `A10` (label) / `B10:D11` (value) | SPECS | Link/reference to the source spec or ticket |
| `A12` (label) / `B12:D12` (value) | URL | URL or screen/route under test |

## Summary formulas (rows 4-11, columns F:L)

Pre-built `COUNTA`/`COUNTIF` formulas over `$B$15:$B$5358` and
`$J/O/T$15:$J/O/T$5307` compute Total / Passed / Failed / Confirmed /
N/A / NT / remaining / progress-rate per round. **Never overwrite these
formulas.** They automatically reflect however many rows actually contain
data — which is exactly why empty tail rows must not carry a leftover
numbering formula (see "Tail row cleanup" below).

## Header row (13:14, merged two-row header)

| Column | Field (JP/EN) |
|---|---|
| A | JP or VN |
| B | No (row-number formula, see below) |
| C | 対象項目名 / Target Item |
| D | タイプ / Type |
| E | 前提条件 / Pre-condition |
| F | 何をテストするのか / Testcase |
| G | 実施手順 / Steps to perform |
| H | データテスト / Data test |
| I | 予測される挙動 / Expected behavior |
| J:N | Round 1 — Status / BugID / Date / Tester / Memo |
| O:S | Round 2 — Status / BugID / Date / Tester / Memo |
| T:X | Round 3 — Status / BugID / Date / Tester / Memo |

## Data rows (15+)

- First data row is **15**. Column `B` uses the formula
  `=(ROW()-(ROW($B$14)))` so the visible "No" always equals `row - 14`,
  regardless of how many rows exist.
- Data validation (dropdown lists) is pre-attached to `D15:D40` (Type) and
  `J15:J40` / `O15:O40` / `T15:T40` (Status: `Passed, Failed, N/A, NT,
  Confirmed`). If you render more than 26 cases (rows go past 40), extend
  these `DataValidation` ranges — don't just leave rows 41+ without a
  dropdown.
- Status columns `J`, `O`, `T` default to `NT` (Not test) for every newly
  rendered case — this matches the sheet's own summary formulas, which treat
  `NT` as "not executed yet."

## Tail row cleanup (important, template quirk)

The blank template ships with the `No` formula **pre-filled in column B for
every row from 15 through 40**, even though those rows have no other
content. If you render, say, 5 cases (rows 15-19) and leave rows 20-40
untouched, `COUNTA($B$15:$B$5358)` still counts all of them as "populated"
rows, silently inflating the Total-testcase stat.

**Rule:** after writing your `N` cases (rows `15..14+N`), clear column `B`
(and any other columns) for every row from `15+N` up to at least `40`
(whichever is greater between the template's original last pre-filled row
and your last written row). Clearing means setting the cell value to `None`,
not deleting the row or its formatting.

## Type dropdown values (column D)

`Display`, `Default`, `Function`, `Validate`, `Transition`, `Operation` —
these are the only six values in the pre-attached data validation list.
Using anything else won't break the file, but will fail validation the
moment someone clicks the cell's dropdown in Excel.
