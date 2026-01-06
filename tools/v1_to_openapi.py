# thordata-sdk-spec/tools/v1_to_openapi.py

import json
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True, help="Path to v1.json")
    parser.add_argument("--out", required=True, help="Output path for openapi.json")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    
    openapi = {
        "openapi": "3.0.3",
        "info": {
            "title": "Thordata API",
            "version": "1.0.1",
            "description": "Official documentation for Thordata Proxy, SERP, Universal, and Web Scraper APIs."
        },
        "servers": [
            {"url": "https://scraperapi.thordata.com", "description": "Scraper API (SERP, Builder)"},
            {"url": "https://universalapi.thordata.com", "description": "Universal API"},
            {"url": "https://openapi.thordata.com/api", "description": "Public & Web Scraper API"},
            {"url": "https://api.thordata.com/api", "description": "Proxy API"}
        ],
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "Token"
                },
                "PublicAuth": {
                    "type": "apiKey",
                    "in": "query", # Or header, based on endpoint
                    "name": "token"
                }
            }
        },
        "paths": {}
    }

    # Helper to add path
    def add_path(path, method, summary, tags, parameters=None, request_body=None, responses=None):
        if path not in openapi["paths"]:
            openapi["paths"][path] = {}
        
        op = {
            "summary": summary,
            "tags": tags,
            "responses": responses or {"200": {"description": "Success"}}
        }
        if parameters:
            op["parameters"] = parameters
        if request_body:
            op["requestBody"] = request_body
            
        openapi["paths"][path][method.lower()] = op

    # 1. SERP API
    add_path("/request", "POST", "SERP Search", ["SERP"], 
        request_body={
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "engine": {"type": "string", "default": "google"},
                            "q": {"type": "string"},
                            "num": {"type": "integer"},
                            # ... more fields from spec["serp"]["request"]
                        },
                        "required": ["engine"]
                    }
                }
            }
        }
    )

    # 2. Universal API
    # (Similar mapping logic...)
    
    # 3. Web Scraper API
    # ...

    
    Path(args.out).write_text(json.dumps(openapi, indent=2), encoding="utf-8")
    print(f"Generated OpenAPI spec at {args.out}")

if __name__ == "__main__":
    main()