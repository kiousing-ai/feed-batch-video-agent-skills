#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def read_prompt(args) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    raise SystemExit("Provide --prompt or --prompt-file.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a batch video task through the local video agent.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8321")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9"])
    parser.add_argument("--logo-path", required=True)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()

    form = urllib.parse.urlencode(
        {
            "source_prompt": read_prompt(args),
            "requested_count": str(args.count),
            "aspect_ratio": args.aspect_ratio,
            "logo_path": args.logo_path,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        args.base_url.rstrip("/") + "/batches",
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    opener = urllib.request.build_opener(NoRedirectHandler)
    try:
        opener.open(request, timeout=args.timeout)
    except urllib.error.HTTPError as exc:
        location = exc.headers.get("Location", "")
        if exc.code in {302, 303} and location:
            match = re.search(r"/batches/(\d+)", location)
            payload = {"ok": bool(match), "location": location}
            if match:
                payload["batch_id"] = int(match.group(1))
            print(json.dumps(payload, ensure_ascii=False))
            return 0 if match else 1
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"ok": False, "status": exc.code, "body": body}, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps({"ok": False, "error": "Batch creation did not return a redirect."}, ensure_ascii=False))
    return 1


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


if __name__ == "__main__":
    raise SystemExit(main())
