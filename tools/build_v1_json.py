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
        ("auth", "auth.yaml"),
        ("env", "env.yaml"),
        ("endpoints", "endpoints.yaml"),
        ("proxy", "proxy.yaml"),
        ("serp", "serp.yaml"),
        ("universal", "universal.yaml"),
        ("tasks", "tasks.yaml"),
        ("publicApi", "public_api.yaml"),        # 新增
        ("publicApiNew", "public_api_new.yaml"), # 新增
        ("errors", "errors.yaml"),
        ("network", "network.yaml"),
        ("locations", "locations.yaml"),
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
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    main()