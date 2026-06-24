# Feed Batch Video Agent Skills

Agent skill for running information-feed style batch video production through a local AI video agent service.

Default service URL:

```text
http://127.0.0.1:8321
```

The skill helps an AI agent:

- check whether the local video agent is running
- preview rewritten prompts
- create batch text-to-video tasks
- watch per-video status
- report finished assets one by one
- surface upstream errors in user-readable language

## Repository Structure

```text
skills/
  feed-batch-video-agent/
    SKILL.md
    references/
      api.md
    scripts/
      health_check.py
      preview_prompts.py
      create_batch.py
      watch_batch.py
```

## Install For Codex

Clone this repository:

```bash
git clone https://github.com/kiousing-ai/feed-batch-video-agent-skills.git
```

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\feed-batch-video-agent-skills\skills\feed-batch-video-agent $env:USERPROFILE\.codex\skills\
```

Then ask Codex:

```text
Use feed-batch-video-agent to create 6 short videos from this prompt. Logo path is D:\assets\logo.png.
```

## Install For Claude Code / Other Skill-Compatible Agents

Use the folder:

```text
skills/feed-batch-video-agent
```

Any agent that understands `SKILL.md` style skills can read the instructions and run the bundled scripts.

For agents that do not have native skill support, point them at:

```text
skills/feed-batch-video-agent/SKILL.md
```

and tell them to follow the workflow.

## Required Local Service

This skill does not include the video-generation backend. Users must run a compatible local service first.

Expected endpoints:

- `GET /healthz`
- `POST /prompt-preview`
- `POST /batches`
- `POST /batches/from-prompts`
- `GET /api/batches/{batch_id}`
- `GET /result/{task_id}`
- `GET /raw/{task_id}`

See `skills/feed-batch-video-agent/references/api.md`.

## Can An Agent Complete Tasks Automatically?

Yes, within the limits of the local service and the user's permissions.

The skill gives the calling agent:

- a repeatable workflow
- endpoint documentation
- executable scripts

So an agent such as Codex, Claude Code, OpenClaw, Hermes, or another tool-using agent can:

1. run the health check
2. preview prompts
3. create a batch
4. poll task status
5. report result URLs or local paths

The agent still needs user-provided inputs such as the prompt, count, logo path, and API key configuration in the local service.

## Quick Script Examples

```bash
python skills/feed-batch-video-agent/scripts/health_check.py
```

```bash
python skills/feed-batch-video-agent/scripts/preview_prompts.py --prompt-file prompt.txt --count 6 --aspect-ratio 9:16
```

```bash
python skills/feed-batch-video-agent/scripts/create_batch.py --prompt-file prompt.txt --count 6 --aspect-ratio 9:16 --logo-path "D:\assets\logo.png"
```

```bash
python skills/feed-batch-video-agent/scripts/watch_batch.py --batch-id 123 --max-wait 600
```

