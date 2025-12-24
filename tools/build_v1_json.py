from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return None
    data = yaml.safe_load(text)
    if data is None:
        return None
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping at top-level.")
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="v1.generated.json")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    v1_dir = root / "spec" / "v1"

    meta = load_yaml(v1_dir / "meta.yaml") or {}
    version = int(meta.get("version", 1))

    out: dict = {"version": version}

    for key, filename in [
        ("auth", "auth.yaml"),  # Auth rules across API families (token/key/Authorization)
        ("env", "env.yaml"),
        ("endpoints", "endpoints.yaml"),
        ("proxy", "proxy.yaml"),
        ("serp", "serp.yaml"),
        ("tasks", "tasks.yaml"),
        ("errors", "errors.yaml"),
        ("network", "network.yaml"),
    ]:
        data = load_yaml(v1_dir / filename)
        if data is None:
            continue
        out[key] = data

    out_path = root / args.out
    out_path.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()