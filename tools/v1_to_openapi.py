# thordata-sdk-spec/tools/v1_to_openapi.py

import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    
    openapi = {
        "openapi": "3.0.3",
        "info": {
            "title": "Thordata API Reference",
            "version": "1.0.0",
            "description": (
                "Official API documentation for Thordata services.\n\n"
                "**Authentication**:\n"
                "- SERP/Universal: Bearer Token (`scraperToken`)\n"
                "- Public/Tasks: Query/Header params (`publicToken` + `publicKey`)"
            )
        },
        "servers": [
            {"url": "https://scraperapi.thordata.com", "description": "Scraper API (SERP, Builder)"},
            {"url": "https://universalapi.thordata.com", "description": "Universal API"},
            {"url": "https://openapi.thordata.com/api", "description": "Public & Web Scraper API"},
            {"url": "https://api.thordata.com/api", "description": "Proxy API"}
        ],
        "components": {
            "securitySchemes": {
                "ScraperAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "Token",
                    "description": "Use `scraperToken` from Dashboard -> Account Settings."
                },
                "PublicAuth": {
                    "type": "apiKey",
                    "in": "query",
                    "name": "token",
                    "description": "Use `publicToken` + `key` query param."
                }
            },
            "schemas": {}
        },
        "paths": {}
    }

    # --- Helper: Map Spec Fields to OpenAPI Schema ---
    def map_fields(fields_dict):
        props = {}
        required = []
        for name, meta in fields_dict.items():
            schema = {"type": meta.get("type", "string")}
            
            # Map types
            if schema["type"] == "integer": schema["type"] = "integer"
            elif schema["type"] == "number": schema["type"] = "number"
            elif schema["type"] == "boolean": schema["type"] = "boolean"
            elif schema["type"] == "array": schema["type"] = "array"
            else: schema["type"] = "string"

            # Enums
            if "enum" in meta:
                schema["enum"] = meta["enum"]
            
            # Description
            if "description" in meta:
                schema["description"] = meta["description"]
            elif "meaning" in meta:
                schema["description"] = meta["meaning"]

            # Required
            if meta.get("required") is True:
                required.append(name)
            
            props[name] = schema
        
        return {"type": "object", "properties": props, "required": required}

    # --- 1. SERP API ---
    if "serp" in spec and "request" in spec["serp"]:
        serp_schema = map_fields(spec["serp"]["request"]["fields"])
        openapi["paths"]["/request"] = {
            "post": {
                "summary": "Real-time Search (SERP)",
                "description": "Execute a search on Google, Bing, Yandex, etc.",
                "tags": ["Scraper API"],
                "security": [{"ScraperAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": serp_schema
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful search results (JSON or HTML)",
                        "content": {
                            "application/json": {},
                            "text/html": {}
                        }
                    }
                }
            }
        }

    # --- 2. Universal API ---
    # (Assuming we extract fields from universal.yaml -> spec['universal']['request'])
    # Currently v1.json universal might be empty, let's hardcode a basic one if missing
    uni_fields = {
        "url": {"type": "string", "required": True},
        "js_render": {"type": "string", "enum": ["True", "False"]},
        "type": {"type": "string", "enum": ["html", "png"]},
        "country": {"type": "string"},
        "wait": {"type": "integer"}
    }
    openapi["paths"]["/request"] = { # Note: Path collision in same file, but different servers?
                                     # OpenAPI supports server override per path
        "post": {
            "summary": "Universal Scraper (Web Unlocker)",
            "description": "Scrape any URL with antibot bypass.",
            "tags": ["Universal API"],
            "servers": [{"url": "https://universalapi.thordata.com"}],
            "security": [{"ScraperAuth": []}],
            "requestBody": {
                "content": {
                    "application/x-www-form-urlencoded": {
                        "schema": map_fields(uni_fields)
                    }
                }
            },
            "responses": {"200": {"description": "HTML or PNG data"}}
        }
    }

    # --- 3. Web Scraper Tasks ---
    if "tasks" in spec:
        # Builder
        if "builder" in spec["tasks"]:
            openapi["paths"]["/builder"] = {
                "post": {
                    "summary": "Create Scraper Task",
                    "tags": ["Web Scraper API"],
                    "security": [{"ScraperAuth": []}], # Needs both, simplifies to one for docs
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "file_name": {"type": "string"},
                                        "spider_name": {"type": "string"},
                                        "spider_id": {"type": "string"},
                                        "spider_parameters": {"type": "string", "description": "JSON string of params"}
                                    },
                                    "required": ["spider_id", "spider_name"]
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Task Created", "content": {"application/json": {"example": {"code": 200, "data": {"task_id": "123"}}}}}}
                }
            }

        # Status
        openapi["paths"]["/tasks-status"] = {
            "post": {
                "summary": "Get Task Status",
                "tags": ["Web Scraper API"],
                "security": [{"PublicAuth": []}], # Uses Public Token
                "parameters": [
                    {"name": "token", "in": "query", "schema": {"type": "string"}},
                    {"name": "key", "in": "query", "schema": {"type": "string"}}
                ],
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {"type": "object", "properties": {"tasks_ids": {"type": "string"}}}
                        }
                    }
                },
                "responses": {"200": {"description": "Task Status"}}
            }
        }

    # --- 4. Public API (Usage, Users) ---
    if "publicApi" in spec:
        # Usage
        if "usageStatistics" in spec["publicApi"]:
            meta = spec["publicApi"]["usageStatistics"]
            openapi["paths"]["/account/usage-statistics"] = {
                "get": {
                    "summary": "Get Usage Statistics",
                    "tags": ["Public API"],
                    "security": [{"PublicAuth": []}],
                    "parameters": [
                        {"name": "token", "in": "query", "required": True, "schema": {"type": "string"}},
                        {"name": "key", "in": "query", "required": True, "schema": {"type": "string"}},
                        {"name": "from_date", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}},
                        {"name": "to_date", "in": "query", "required": True, "schema": {"type": "string", "format": "date"}}
                    ],
                    "responses": {"200": {"description": "Usage Data"}}
                }
            }

    Path(args.out).write_text(json.dumps(openapi, indent=2), encoding="utf-8")
    print(f"Generated OpenAPI spec at {args.out}")

if __name__ == "__main__":
    main()