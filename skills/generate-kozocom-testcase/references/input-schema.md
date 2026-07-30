# Input JSON Schema

This is the contract between the normalized testcase content you write and
`scripts/render_testcase_workbook.py`. Write one JSON file with exactly two
top-level keys: `metadata` and `cases`.

```json
{
  "metadata": {
    "locale": "VN",
    "environment": "STG",
    "browser": "Google Chrome 126",
    "created_by": "Your Name",
    "specs": "https://link-to-spec-or-ticket",
    "url": "https://staging.example.com/feature"
  },
  "cases": [
    {
      "target_item": "Email field - Registration form",
      "type": "Validate",
      "precondition": "User is on the Registration screen",
      "testcase": "Verify validation when Email field is left blank",
      "steps": "1. Go to Registration screen\n2. Leave Email empty\n3. Fill other fields\n4. Click Register",
      "data_test": "",
      "expected": "Error 'Email is required' is shown below the field; form is not submitted"
    }
  ]
}
```

## `metadata` (all optional, but fill what you know)

| Key | Target cell | Notes |
|---|---|---|
| `locale` | `A15:A<last>` | `VN` or `JP`. Defaults to `VN` if omitted. Marks the language convention of the sheet, not necessarily the content language. |
| `environment` | `G2` (merged `G2:H3`) | e.g. `STG`, `PROD`, `DEV`. Defaults to leaving the template's existing value untouched if omitted. |
| `browser` | `J2` (merged `J2:L2`) | Browser/device + version, e.g. `Google Chrome 126`, `iPhone 15 - iOS 17.5`. Leave the template default untouched if omitted. |
| `created_by` | `B9` (merged `B9:D9`) | Tester / author name. |
| `specs` | `B10` (merged `B10:D11`) | Link or short reference to the spec/requirement/ticket used to derive the cases. |
| `url` | `B12` (merged `B12:D12`) | The URL (or app screen/route if not a web URL) under test. |

Only keys that are present overwrite the template's default value; omit a key
to leave the template's pre-filled default in place.

## `cases` (required, array, order = row order)

Each case becomes one row starting at row 15. All 7 fields are required
strings (use `""` for `data_test` when no specific input value applies —
never omit the key).

| Key | Excel column | Constraint |
|---|---|---|
| `target_item` | C | Free text — name the field/screen/button/flow under test |
| `type` | D | **Must** be one of: `Display`, `Default`, `Function`, `Validate`, `Transition`, `Operation` (matches the sheet's dropdown validation). Anything else gets normalized to `Function` by the renderer with a printed warning — fix the source data instead of relying on that fallback. |
| `precondition` | E | Free text, can be empty string if genuinely none |
| `testcase` | F | One-line statement of what is being tested |
| `steps` | G | Numbered steps, `\n`-separated, precise enough to reproduce |
| `data_test` | H | Concrete input value(s), or `""` |
| `expected` | I | Verifiable expected outcome, not a vague statement |

Round-tracking columns `J:X` (Status/BugID/Date/Tester/Memo × 3 rounds) are
never populated by the renderer except with the default `NT` status placed
in `J`, `O`, `T` — those are for testers to fill in after execution, not part
of the design-time payload.
