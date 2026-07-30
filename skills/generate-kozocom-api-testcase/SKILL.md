---
name: generate-api-testcase-workbook
description: Create a detailed API testcase workbook (.xlsx) — columns Endpoint, No, Type, Precondition, Scenario, Request Headers/Params/Body, Expected Status Code, Expected Response — from an API document, Swagger/OpenAPI spec (.yaml/.yml/.json), or plain API description text. Use when the user asks to "gen API testcase", "tạo testcase cho API", provides a swagger/openapi file or API doc and wants test cases generated, or mentions endpoints/methods/status codes needing coverage. Distinct from generate-kozocom-testcase-workbook (UI/feature testcases) and generate-checklist-workbook (screen checklists) — this one is specifically for HTTP API endpoints.
---

# Generate API Testcase Workbook

Produce very detailed API-level testcases per endpoint: positive path,
validation, boundary values, auth/permission, basic security (injection,
IDOR), error handling, and rate limiting where applicable — rendered as an
`.xlsx` workbook grouped by endpoint.

## Workflow

1. **Load and parse the source.**
   - If given a Swagger/OpenAPI file (`.yaml`, `.yml`, `.json`) or a URL to
     one, run the bundled parser instead of reading the raw spec by eye —
     specs are often too large/nested to reliably scan manually and schema
     constraints (required, format, min/max) are easy to miss that way:
     ```bash
     pip install pyyaml --break-system-packages   # if not already available
     python3 scripts/parse_openapi_spec.py --input /path/to/spec.yaml --output /tmp/api_summary.json
     ```
     Then read `/tmp/api_summary.json` — it lists every operation with its
     resolved parameters, request body schema, response status codes, and
     security requirements ($ref pointers already resolved).
   - If given plain API documentation text (no machine-readable spec),
     extract the same information manually: method, path, parameters,
     request/response schema, auth requirements, documented error codes.
   - If given a Postman collection or other format, read it directly with
     `view`/`bash` and extract the equivalent information.

2. **Extract testable facts before writing cases.**
   Per endpoint, note: required vs optional fields, types/formats,
   min/max constraints, enums, auth scheme, documented status codes and
   what triggers each, and any rate-limit or pagination notes. Flag
   anything genuinely ambiguous (e.g. "spec doesn't say what happens on
   duplicate email — assuming 409") as an assumption rather than guessing
   silently, and ask only if it would materially change scope.

3. **Design cases per endpoint, aiming for thorough coverage.**
   Read [references/input-schema.md](references/input-schema.md) for the
   full coverage checklist (Positive / Validation / Boundary / Auth /
   Permission / Security / ErrorHandling / RateLimit / ContentType /
   Regression) and the exact field meanings. Cover whichever groups
   genuinely apply to each endpoint — don't force irrelevant ones (e.g. no
   rate-limit cases if the spec documents none).

4. **Normalize into JSON** per the same reference doc: an `items` array of
   `{endpoint, type, precondition, scenario, headers, params, body,
   expected_status, expected_response, highlight}`.

5. **Render the workbook.**
   ```bash
   pip install openpyxl --break-system-packages   # if not already available
   python3 scripts/render_api_testcase_workbook.py \
     --input /absolute/path/to/testcases.json \
     --output /mnt/user-data/outputs/API-Testcase-<ServiceName>.xlsx
   ```

6. **Verify**, then present with `present_files`:
   - Each endpoint's `No` restarts at 1 and the Endpoint cell is merged for
     that block.
   - `Type` values match the standard set (see input-schema.md).
   - Every row's `expected_response` is concrete/checkable, not vague.
   - Security/auth cases exist for every endpoint that requires auth.
   - `highlight` is used sparingly (auth/security cases, not everything).

## Output Rules

- Always render via `scripts/render_api_testcase_workbook.py` from
  `assets/api-testcase-template.xlsx` — don't hand-build the sheet.
- Content language: **English**, unless the user asks otherwise.
- Group and order items strictly by endpoint — the renderer's merge/numbering
  logic depends on same-endpoint rows being contiguous.
- Don't invent request/response fields that aren't in the spec or doc; if a
  field's constraints are undocumented, say so as an assumption instead of
  making up a plausible-looking limit.
- If the source is a very large spec (50+ operations), confirm with the user
  whether to cover all endpoints or a specific subset before generating —
  otherwise default to covering everything, noting the total endpoint/case
  count up front.

## Source Handling

- `.yaml`/`.yml`/`.json` OpenAPI/Swagger → `scripts/parse_openapi_spec.py`
  (handles both OpenAPI 3.x `components/schemas` and Swagger 2.0
  `definitions`/body-parameters, with `$ref` resolution).
- Plain-text API docs, Postman collections, or partial specs → read directly
  and extract the same fields by hand.
- If auth uses a scheme the spec references (`securitySchemes` /
  `securityDefinitions`), reflect the actual scheme name/type in
  `precondition`/`headers` (e.g. `Bearer` JWT vs API key in a header vs
  OAuth2) rather than a generic placeholder.

## References

- [references/input-schema.md](references/input-schema.md) — JSON contract
  for the renderer, column meanings, and the full per-endpoint coverage
  checklist.
