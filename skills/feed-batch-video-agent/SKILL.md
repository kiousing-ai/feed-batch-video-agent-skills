---
name: feed-batch-video-agent
description: Use when the user wants to run information-feed style batch video tasks through a local AI video agent service. Supports checking the local service, previewing rewritten prompts, creating batch text-to-video jobs, tracking per-video status, and reporting finished assets from http://127.0.0.1:8321 or another configured base URL.
---

# Feed Batch Video Agent

Use the local batch video agent service to turn agent-rewritten prompts into multiple short-video assets with text-to-video generation, subtitles, and logo overlay.

Default service URL: `http://127.0.0.1:8321`

## Workflow

1. Check the service:
   `python scripts/health_check.py --base-url http://127.0.0.1:8321`
2. If the user only asks whether the workflow can run, stop after the health check and explain the service state.
3. For a new batch, collect:
   - core prompt
   - requested count
   - aspect ratio, usually `9:16` or `16:9`
   - logo local path
   - the user's KVideo API key for this batch, unless the service already has one configured
4. Rewrite prompts as the calling agent. Preserve only:
   - storyboard structure / scene count
   - product names, slogans, and core dialogue
   - pacing rhythm
   Change everything else in a product-appropriate way. Avoid repeating the same setting or creative angle across items.
5. Save rewritten prompts as either a JSON array or newline-delimited text.
6. If the user approves the prompts, create a batch:
   `python scripts/create_batch.py --prompt-file prompt.txt --prompts-file rewritten_prompts.json --count 6 --aspect-ratio 9:16 --logo-path "D:\logo.png" --api-key "<USER_KVIDEO_KEY>"`
7. For a no-cost integration test, add `--dry-run`.
8. Watch the batch:
   `python scripts/watch_batch.py --batch-id 123`
9. Report results progressively. Finished tasks expose `/result/{task_id}`. Raw upstream videos expose `/raw/{task_id}`.

## Behavior Rules

- Do not ask the user to upload local logo/material files when the service runs on the same machine. Use the local path.
- Explain that completed videos appear one by one; a batch does not need to finish completely before individual results are downloadable.
- In skill mode, do not call the backend prompt-preview endpoint unless the user explicitly wants the backend LLM to rewrite. The calling agent should rewrite prompts.
- Never invent a fixed genre/theme bank. Choose creative differences from the user's product/category and brief.
- If video generation fails with upstream errors, report the user-readable error and the affected prompt index.
- Use `--api-key` for scheme A: each user supplies their own KVideo key per batch.

## Useful Scripts

- `scripts/health_check.py`: verify `/healthz`
- `scripts/preview_prompts.py`: optional backend LLM preview path; do not use by default in skill mode
- `scripts/create_batch.py`: create a batch through `/batches/from-prompts` when `--prompts-file` is provided
- `scripts/watch_batch.py`: poll `/api/batches/{batch_id}` and summarize task states

Read `references/api.md` when endpoint details or script behavior are needed.
