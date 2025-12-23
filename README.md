# thordata-sdk-spec

A small, versioned specification repository used to keep Thordata SDKs (Python/JS) consistent.

This repository defines the canonical defaults and parameter conventions for:
- API base URLs and environment variables
- Endpoint paths
- Proxy gateway conventions (hosts, ports, username format)
- SERP parameter normalization (e.g. `searchType -> tbm`)
- Error code handling precedence and mappings
- Network/proxy behavior notes (especially for restricted networks)

Any change to v1.json requires bumping sdk-spec submodule in all SDK repos (or explicitly postponing the bump).

## Files

### `v1.json` (Canonical artifact)
`v1.json` is the canonical, machine-readable spec snapshot consumed by SDK parity tests.

SDK repositories typically include this repo as a git submodule at `sdk-spec/` and read:
- `sdk-spec/v1.json`

### `spec/v1/*.yaml` (Human-readable sources)
The YAML files under `spec/v1/` are the human-readable spec sources.

At this stage, `v1.json` is maintained manually and should remain consistent with the YAML sources.

### `schema/v1.schema.json` (Optional validation)
A JSON Schema for validating `v1.json`. This is optional but recommended.

## Versioning policy

- `v1` is considered stable.
- Backward-compatible changes (additive fields, clarifications) may update `v1` and should bump the git tag (e.g. `v1.0.1`).
- Breaking changes must create a new version (`v2.json` and `spec/v2/...`).

## Change workflow

1. Update YAML sources in `spec/v1/` (and/or `v1.json`).
2. Keep `v1.json` in sync with the YAML sources.
3. Tag a new version (e.g. `v1.0.1`).
4. Bump the `sdk-spec` submodule pointer in both SDK repos.
5. Ensure SDK parity tests pass in both repositories.

## Notes for restricted networks

See `spec/v1/network.yaml` for guidance about environment proxies and tunneling (e.g. TUN mode).