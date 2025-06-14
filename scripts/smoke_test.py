#!/usr/bin/env python

import httpx, json, os, sys


query = sys.argv[1] if len(sys.argv) > 1 else "weekend beach break in july"

resp = httpx.post(
    "http://127.0.0.1:8000/travel-assistant", json={"query": query}, timeout=60
)

print(json.dumps(resp.json(), indent=2))
