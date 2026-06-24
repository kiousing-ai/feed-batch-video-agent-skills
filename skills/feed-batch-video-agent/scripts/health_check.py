#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the local feed batch video agent service.")
    parser.add_argument("--base-url", default="https://vskills.kio-api.win")
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()

    url = args.base_url.rstrip("/") + "/healthz"
    try:
        with urllib.request.urlopen(url, timeout=args.timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            payload = json.loads(body)
    except Exception as exc:
        print(json.dumps({"ok": False, "url": url, "error": str(exc)}, ensure_ascii=False))
        return 1

    ok = bool(payload.get("ok"))
    print(json.dumps({"ok": ok, "url": url, "response": payload}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

