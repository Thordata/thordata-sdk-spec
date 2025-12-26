# thordata-sdk-spec

A versioned specification repository used to keep Thordata SDKs (Python, Node.js, Go, Java) consistent.

This repository defines the canonical defaults, parameter conventions, and shared logic for:
- API base URLs and environment variables
- Endpoint paths and authentication methods
- Proxy gateway conventions (hosts, ports, username format)
- SERP parameter normalization
- Error code handling precedence and mappings
- Webhook payload definitions
- Public API and API NEW specifications

Any change to `v1.json` requires bumping the sdk-spec submodule in all SDK repos.

## Structure

### `v1.json` (Canonical artifact)
The single source of truth consumed by SDK parity tests. Generated from the YAML sources in `spec/v1/`.

### `spec/v1/*.yaml` (Human-readable sources)
- `auth.yaml`: Authentication modes (Bearer, Header Token, Sign/ApiKey)
- `endpoints.yaml`: API paths and methods
- `env.yaml`: Environment variable names and defaults
- `errors.yaml`: Error code mappings (300, 4xx, 5xx)
- `proxy.yaml`: Proxy hosts, ports, and username construction rules
- `serp.yaml`: Search engine parameters and mappings
- `tasks.yaml`: Web Scraper API definitions (Builder, Video Builder, List, Status)
- `public_api.yaml`: Public API endpoints (Usage, Users, Whitelist)
- `public_api_new.yaml`: API NEW endpoints (Sign/ApiKey auth)

### `tools/`
Scripts to build (`build_v1_json.py`) and validate (`validate_v1_json.py`) the JSON spec.

## Versioning Policy

- `v1` is considered stable.
- Backward-compatible changes update `v1.json` (and git tag).
- Breaking changes require a new major version (`v2`).

## Change Workflow

1. Update YAML sources in `spec/v1/`.
2. Run `python tools/build_v1_json.py` to regenerate `v1.json`.
3. Verify with `python tools/validate_v1_json.py`.
4. Commit changes.
5. Update submodules in SDK repositories.