#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class PromptPreviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.prompts: list[str] = []
        self._in_prompt_textarea = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag.lower() != "textarea":
            return
        attr_map = dict(attrs)
        if attr_map.get("name") == "prompts":
            self._in_prompt_textarea = True
            self._buffer = []

    def handle_data(self, data: str):
        if self._in_prompt_textarea:
            self._buffer.append(data)

    def handle_endtag(self, tag: str):
        if tag.lower() == "textarea" and self._in_prompt_textarea:
            self.prompts.append(html.unescape("".join(self._buffer)).strip())
            self._in_prompt_textarea = False
            self._buffer = []


def read_prompt(args) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    raise SystemExit("Provide --prompt or --prompt-file.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview rewritten prompts from the local video agent.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8321")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9"])
    parser.add_argument("--timeout", type=float, default=360)
    args = parser.parse_args()

    form = urllib.parse.urlencode(
        {
            "source_prompt": read_prompt(args),
            "requested_count": str(args.count),
            "aspect_ratio": args.aspect_ratio,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        args.base_url.rstrip("/") + "/prompt-preview",
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"ok": False, "status": exc.code, "body": body}, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    if "application/json" in content_type:
        print(body)
        return 0

    parser = PromptPreviewParser()
    parser.feed(body)
    print(json.dumps({"ok": True, "count": len(parser.prompts), "prompts": parser.prompts}, ensure_ascii=False, indent=2))
    return 0 if parser.prompts else 1


if __name__ == "__main__":
    raise SystemExit(main())
