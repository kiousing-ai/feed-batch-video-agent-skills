#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import urllib.request


TERMINAL = {"done", "error", "partial_error"}


def fetch_json(url: str, timeout: float):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def summarize(payload):
    batch = payload["batch"]
    tasks = payload["tasks"]
    return {
        "batch_id": batch["id"],
        "status": batch["status"],
        "total": len(tasks),
        "done": sum(1 for task in tasks if task["status"] == "done"),
        "running": sum(1 for task in tasks if task["status"] == "running"),
        "queued": sum(1 for task in tasks if task["status"] == "queued"),
        "error": sum(1 for task in tasks if task["status"] == "error"),
        "results": [
            {
                "task_id": task["id"],
                "index": task["prompt_index"],
                "status": task["status"],
                "result_url": f"/result/{task['id']}" if task.get("result_path") else None,
                "raw_url": f"/raw/{task['id']}" if task.get("raw_result_path") else None,
                "error": task.get("error_message") or task.get("postprocess_error"),
            }
            for task in tasks
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch a local video-agent batch.")
    parser.add_argument("--base-url", default="https://vskills.kio-api.win")
    parser.add_argument("--batch-id", type=int, required=True)
    parser.add_argument("--interval", type=float, default=8)
    parser.add_argument("--max-wait", type=float, default=0, help="Seconds. 0 means one-shot status.")
    parser.add_argument("--timeout", type=float, default=20)
    args = parser.parse_args()

    url = args.base_url.rstrip("/") + f"/api/batches/{args.batch_id}"
    deadline = time.time() + args.max_wait if args.max_wait > 0 else None
    while True:
        payload = fetch_json(url, args.timeout)
        summary = summarize(payload)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        if summary["status"] in TERMINAL or not deadline:
            return 0 if summary["status"] != "error" else 1
        if time.time() >= deadline:
            return 2
        time.sleep(max(1, args.interval))


if __name__ == "__main__":
    raise SystemExit(main())

