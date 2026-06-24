---
name: feed-batch-video-agent
description: Use when the user wants to run information-feed style batch video tasks through a local AI video agent service. Supports checking the local service, previewing rewritten prompts, creating batch text-to-video jobs, tracking per-video status, and reporting finished assets from http://127.0.0.1:8321 or another configured base URL.
---

# Feed Batch Video Agent

Use the local batch video agent service to turn one core prompt into multiple short-video assets with prompt rewriting, text-to-video generation, subtitles, and logo overlay.

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
4. Preview rewritten prompts before creating videos when the user wants review/editing:
   `python scripts/preview_prompts.py --prompt-file prompt.txt --count 6 --aspect-ratio 9:16`
5. If the user approves the prompts, create a batch:
   `python scripts/create_batch.py --prompt-file prompt.txt --count 6 --aspect-ratio 9:16 --logo-path "D:\logo.png"`
6. Watch the batch:
   `python scripts/watch_batch.py --batch-id 123`
7. Report results progressively. Finished tasks expose `/result/{task_id}`. Raw upstream videos expose `/raw/{task_id}`.

## Behavior Rules

- Do not ask the user to upload local logo/material files when the service runs on the same machine. Use the local path.
- Explain that completed videos appear one by one; a batch does not need to finish completely before individual results are downloadable.
- If prompt rewriting fails with `524`, explain that the upstream LLM gateway timed out or queued too long. Suggest retrying or reducing the count.
- Preserve user product names, slogans, and core dialogue when asking the service to rewrite prompts.
- For large counts, expect the service to split prompt rewriting into smaller upstream requests.

## Useful Scripts

- `scripts/health_check.py`: verify `/healthz`
- `scripts/preview_prompts.py`: call `/prompt-preview` and print rewritten prompts extracted from the preview HTML
- `scripts/create_batch.py`: create a batch through `/batches`
- `scripts/watch_batch.py`: poll `/api/batches/{batch_id}` and summarize task states

Read `references/api.md` when endpoint details or script behavior are needed.
