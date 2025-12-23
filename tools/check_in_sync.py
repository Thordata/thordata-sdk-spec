from __future__ import annotations

import argparse
import json
from pathlib import Path


def canonical_json(path: Path) -> str:
    obj = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--generated", required=True)
    ap.add_argument("--canonical", required=True)
    args = ap.parse_args()

    gen = canonical_json(Path(args.generated))
    can = canonical_json(Path(args.canonical))

    if gen != can:
        raise SystemExit(
            "Spec is out of sync.\n"
            "Run: python tools/build_v1_json.py --out v1.generated.json\n"
            "Then update v1.json to match v1.generated.json.\n"
        )


if __name__ == "__main__":
    main()