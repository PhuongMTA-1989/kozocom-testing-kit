# Input JSON Schema — API Testcase Workbook

One JSON file: either a top-level array of items, or an object with an
`items` array.

```json
{
  "items": [
    {
      "endpoint": "POST /users",
      "type": "Positive",
      "precondition": "Valid Bearer token for a user with role admin",
      "scenario": "Create a user with all required fields valid",
      "headers": "Authorization: Bearer {valid_token}\nContent-Type: application/json",
      "params": "",
      "body": "{\"email\": \"test@abc.com\", \"password\": \"Abc@12345\", \"name\": \"Test User\"}",
      "expected_status": "201",
      "expected_response": "Response body contains the created user's id, email, and name; password is not echoed back"
    },
    {
      "endpoint": "POST /users",
      "type": "Auth",
      "precondition": "No Authorization header sent",
      "scenario": "Call the endpoint without an auth token",
      "headers": "Content-Type: application/json",
      "params": "",
      "body": "{\"email\": \"test@abc.com\", \"password\": \"Abc@12345\", \"name\": \"Test User\"}",
      "expected_status": "401",
      "expected_response": "Error response indicating missing/invalid authentication; no user is created",
      "highlight": true
    }
  ]
}
```

## Fields (all required except `highlight`)

| Key | Excel column | Notes |
|---|---|---|
| `endpoint` | A — Endpoint | `METHOD /path` (e.g. `GET /orders/{id}`). Consecutive items with the same endpoint are grouped: cell merged vertically, `No` restarts at 1. **Order items endpoint by endpoint** — don't interleave. |
| `type` | C — Type | One of: `Positive`, `Validation`, `Boundary`, `Auth`, `Permission`, `Security`, `ErrorHandling`, `RateLimit`, `ContentType`, `Regression`. |
| `precondition` | D — Precondition | State required before calling (auth token validity/role, existing resource, prior state) |
| `scenario` | E — Scenario | One-line description of what's being tested |
| `headers` | F — Request Headers | Key request headers relevant to the scenario (auth, content-type, custom headers). Use `""` if nothing notable. |
| `params` | G — Request Params | Path and/or query params used, with the specific value under test |
| `body` | H — Request Body | Request payload (can be a JSON string). Use `""` for methods without a body. |
| `expected_status` | I — Expected Status Code | The HTTP status code expected, as a string (e.g. `"200"`, `"400"`, `"429"`) |
| `expected_response` | J — Expected Response / Behavior | Concrete, verifiable expected response body/behavior — not vague |
| `highlight` (optional) | whole row | `true` shades the row light green for extra reviewer attention (e.g. security/auth cases). Use sparingly. |

## Coverage guidance per endpoint (use `parse_openapi_spec.py` output to drive this)

For each endpoint, design cases across as many of these as genuinely apply:

- **Positive** — valid request per schema, typical and edge-of-valid values
- **Validation** — omit each required field one at a time; wrong type (string
  where number expected, etc.); wrong format (invalid email/date/UUID); value
  violating `enum`
- **Boundary** — `minLength`/`maxLength` exact and ±1; `minimum`/`maximum`
  exact and ±1; empty array vs `minItems`/`maxItems`; empty string on
  non-required string field
- **Auth** — missing Authorization header, malformed token, expired token,
  token for wrong audience → expect `401`
- **Permission** — valid token but insufficient role/scope → expect `403`
- **Security** — SQL-injection-style characters (`' OR '1'='1`) and XSS
  payloads (`<script>alert(1)</script>`) in string params/body fields; path
  traversal (`../`) in path params; IDOR-style attempt to access another
  user's resource by changing a path/query id
- **ErrorHandling** — non-existent resource id → `404`; duplicate unique
  field → `409`; unsupported/missing required query filter → documented
  error status
- **RateLimit** — only if the spec documents a rate limit — repeated calls
  exceeding the limit → expect `429`
- **ContentType** — wrong/missing `Content-Type` on a body-carrying request →
  expect `415` or documented behavior
- **Regression** — a small ring around anything a change request modifies on
  this endpoint
