# Local Video Agent API

Default base URL: `http://127.0.0.1:8321`

## Endpoints

`GET /healthz`

Returns JSON like:

```json
{"ok": true}
```

`POST /prompt-preview`

Form fields:

- `source_prompt`: core prompt
- `requested_count`: number of rewritten prompts
- `aspect_ratio`: `9:16` or `16:9`

Returns an HTML preview page with editable `<textarea name="prompts">` entries. On failure, FastAPI may return JSON with `detail`.

`POST /batches`

Creates a batch and lets the service rewrite prompts internally.

Form fields:

- `source_prompt`
- `requested_count`
- `aspect_ratio`
- `logo_path`
- optional `overlay_position`
- optional `overlay_width`
- optional `overlay_margin_x`
- optional `overlay_margin_y`

Returns a redirect to `/batches/{batch_id}`.

`POST /batches/from-prompts`

Creates a batch from already previewed/edited prompts.

Form fields:

- `source_prompt`
- `aspect_ratio`
- repeated `prompts`
- `logo_path`
- optional logo overlay controls

Returns a redirect to `/batches/{batch_id}`.

`GET /api/batches/{batch_id}`

Returns:

```json
{
  "batch": {"id": 1, "status": "running"},
  "tasks": [
    {
      "id": 1,
      "prompt_index": 1,
      "status": "done",
      "result_path": "...",
      "raw_result_path": "...",
      "error_message": null
    }
  ]
}
```

`GET /result/{task_id}`

Downloads the final postprocessed video.

`GET /raw/{task_id}`

Downloads the raw upstream video.
