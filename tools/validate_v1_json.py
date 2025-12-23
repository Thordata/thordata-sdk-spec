from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import validate


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--schema", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))

    validate(instance=spec, schema=schema)

    # Lightweight invariants (keep this minimal and stable)
    rule = spec["errors"]["precedence"]["effectiveCodeRule"]
    if rule != "payload_code_if_present_and_not_200_else_http_status":
        raise SystemExit(f"Unexpected effectiveCodeRule: {rule}")

    ports = spec["proxy"]["products"]
    for k in ("residential", "mobile", "datacenter", "isp"):
        p = ports[k]["port"]
        if not isinstance(p, int):
            raise SystemExit(f"proxy.products.{k}.port must be int, got {type(p).__name__}")

    tbm = spec["serp"]["mappings"]["searchTypeToTbm"]
    if tbm.get("news") != "nws":
        raise SystemExit("serp.mappings.searchTypeToTbm.news must be 'nws'")


if __name__ == "__main__":
    main()