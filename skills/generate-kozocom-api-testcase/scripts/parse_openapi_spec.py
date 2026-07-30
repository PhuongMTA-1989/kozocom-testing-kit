#!/usr/bin/env python3
"""
Parse an OpenAPI/Swagger spec (YAML or JSON) into a flat, human-readable JSON
summary of every operation (path + method): parameters, request body schema,
responses, and security requirements. Resolves local `$ref` pointers into
`#/components/...` (OpenAPI 3) or `#/definitions/...` (Swagger 2).

This is a reading aid, not the testcase renderer — use it so large specs
don't have to be manually eyeballed for every field's constraints (required,
type, format, minLength/maxLength, minimum/maximum, enum).

Usage:
    python3 parse_openapi_spec.py --input openapi.yaml --output summary.json
    python3 parse_openapi_spec.py --input swagger.json          # prints to stdout
"""
import argparse
import json
import sys


def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if path.endswith((".yaml", ".yml")):
        import yaml
        return yaml.safe_load(text)
    return json.loads(text)


def resolve_ref(spec, ref):
    if not ref.startswith("#/"):
        return {}
    node = spec
    for part in ref[2:].split("/"):
        node = node.get(part, {}) if isinstance(node, dict) else {}
    return node


def resolve(spec, node, _depth=0):
    """Recursively resolve $ref pointers, with a depth guard against cycles."""
    if _depth > 12 or not isinstance(node, (dict, list)):
        return node
    if isinstance(node, list):
        return [resolve(spec, n, _depth + 1) for n in node]
    if "$ref" in node:
        target = resolve_ref(spec, node["$ref"])
        return resolve(spec, target, _depth + 1)
    return {k: resolve(spec, v, _depth + 1) for k, v in node.items()}


def schema_summary(schema):
    """Reduce a JSON-schema-like object to the fields testcase design needs."""
    if not schema:
        return {}
    out = {"type": schema.get("type")}
    for key in ("format", "enum", "minLength", "maxLength", "minimum", "maximum",
                "pattern", "minItems", "maxItems", "default", "nullable"):
        if key in schema:
            out[key] = schema[key]
    if schema.get("type") == "object" or "properties" in schema:
        required = set(schema.get("required", []))
        props = {}
        for name, prop_schema in (schema.get("properties") or {}).items():
            props[name] = {**schema_summary(prop_schema), "required": name in required}
        out["properties"] = props
    if schema.get("type") == "array" and "items" in schema:
        out["items"] = schema_summary(schema["items"])
    return out


def get_body_schema(spec, operation):
    # OpenAPI 3
    rb = operation.get("requestBody")
    if rb:
        content = rb.get("content", {})
        for media_type in ("application/json", *content.keys()):
            if media_type in content:
                return {
                    "media_type": media_type,
                    "required": rb.get("required", False),
                    "schema": schema_summary(content[media_type].get("schema", {})),
                }
    # Swagger 2 (body parameter is listed under `parameters`)
    for param in operation.get("parameters", []):
        if param.get("in") == "body":
            return {
                "media_type": "application/json",
                "required": param.get("required", False),
                "schema": schema_summary(param.get("schema", {})),
            }
    return None


def get_params(operation, path_item):
    combined = (path_item.get("parameters") or []) + (operation.get("parameters") or [])
    out = []
    for p in combined:
        if p.get("in") == "body":
            continue
        entry = {
            "name": p.get("name"),
            "in": p.get("in"),
            "required": p.get("required", False),
        }
        schema = p.get("schema") or {k: p[k] for k in
                                      ("type", "format", "enum", "minimum", "maximum",
                                       "minLength", "maxLength", "pattern") if k in p}
        entry.update(schema_summary(schema))
        out.append(entry)
    return out


def get_responses(operation):
    out = {}
    for status, resp in (operation.get("responses") or {}).items():
        out[str(status)] = resp.get("description", "")
    return out


def get_security(spec, operation):
    sec = operation.get("security", spec.get("security"))
    if not sec:
        return []
    schemes = []
    defs = (spec.get("components", {}).get("securitySchemes")
            or spec.get("securityDefinitions") or {})
    for entry in sec:
        for name in entry.keys():
            scheme = defs.get(name, {})
            schemes.append({"name": name, "type": scheme.get("type"), "scheme": scheme.get("scheme")})
    return schemes


def summarize(spec):
    spec = resolve(spec, spec)
    operations = []
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            if method not in path_item:
                continue
            operation = path_item[method]
            operations.append({
                "method": method.upper(),
                "path": path,
                "operation_id": operation.get("operationId"),
                "summary": operation.get("summary", ""),
                "tags": operation.get("tags", []),
                "parameters": get_params(operation, path_item),
                "request_body": get_body_schema(spec, operation),
                "responses": get_responses(operation),
                "security": get_security(spec, operation),
            })
    return {
        "title": (spec.get("info") or {}).get("title", ""),
        "version": (spec.get("info") or {}).get("version", ""),
        "servers": [s.get("url") for s in spec.get("servers", [])] or spec.get("host"),
        "operation_count": len(operations),
        "operations": operations,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to the OpenAPI/Swagger file (.yaml/.yml/.json)")
    parser.add_argument("--output", default=None, help="Write JSON summary here instead of stdout")
    args = parser.parse_args()

    spec = load_spec(args.input)
    summary = summarize(spec)

    text = json.dumps(summary, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote summary of {summary['operation_count']} operations to {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
