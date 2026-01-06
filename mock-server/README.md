# Thordata Mock Server

A lightweight mock server for Thordata APIs, useful for local development and integration testing without consuming credits.

## Usage

```bash
# Run with Docker
docker run -p 8080:8080 ghcr.io/thordata/mock-server:latest
```

## Endpoints

- `POST /request`: SERP / Universal
- `POST /builder`: Create Task
- `GET /account/usage-statistics`: Usage
...