# Workspace Management

## Root

Do not store research artifacts in the skill directory.

Do not default research artifacts to the C drive.

The user must choose a workspace root before the first run. Store that choice in a small config file:

```text
<CODEX_HOME>\\pigeonyang-cover-style-distiller\config.json
```

The config stores only the chosen `workspace_root`; heavy assets live in the user-selected workspace.

Recommended workspace shape:

```text
<user-selected-workspace>\pigeonyang-cover-style-distiller\research
```

Example after the user chooses a J drive workspace:

```text
<USER_RESEARCH_WORKSPACE>
```

Run directory:

```text
<root>\<creator-id>\<YYYYMMDD-HHMMSS>\
```

Example:

```text
<USER_RESEARCH_WORKSPACE>\mrbeast\20260524-174500\
```

## Directory Layout

```text
<run>\
  manifest.json
  covers\
    001-title-slug.jpg
    002-title-slug.jpg
  sources\
    articles\
    transcripts\
    pages\
  distillation\
    research.md
  prompts\
  generated\
```

## Required Commands

First-time setup. Ask the user for the workspace path, then persist it:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py set-root `
  --workspace-root <USER_RESEARCH_WORKSPACE>
```

Check remembered workspace:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py show-config
```

Initialize a run:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py init `
  --creator-id mrbeast `
  --creator-name "MrBeast"
```

If no workspace root has been configured, `init` and `cleanup` must fail instead of writing to a default C drive location.

Archive a downloaded cover and update `manifest.json` in one operation:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py add-cover `
  --run-dir <run-dir> `
  --file <downloaded-file> `
  --video-title "I Spent 50 Hours Buried Alive" `
  --video-url "https://www.youtube.com/watch?v=..." `
  --thumbnail-url "https://..." `
  --selected-reason "top viewed sample"
```

Archive a downloaded process source and update `manifest.json` in one operation:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py add-source `
  --run-dir <run-dir> `
  --file <downloaded-source-file> `
  --title "Interview about thumbnail process" `
  --url "https://..." `
  --source-type "interview"
```

Record a generated child skill or other artifact:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py set-artifact `
  --run-dir <run-dir> `
  --key child_skill `
  --value <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-mrbeast
```

Do not manually copy final research assets into the managed layout unless a tool cannot call the script. If manual recovery is unavoidable, update `manifest.json` before continuing.

## Retention

Default retention:

- `covers\`: raw public thumbnail files, delete after 30 days.
- `sources\`: downloaded articles, transcripts, and page captures, delete after 90 days.
- `distillation\research.md`: keep indefinitely unless the user asks to delete it.
- generated child skills: keep indefinitely unless the user asks to delete them.
- `prompts\` and `generated\`: keep indefinitely by default because they are user production artifacts.

Run cleanup before every new research run:

```powershell
python <CODEX_SKILLS_ROOT>\pigeonyang-cover-style-distiller\scripts\manage_research_workspace.py cleanup
```

This is not a scheduled OS task. It is deterministic enforcement inside the skill workflow. If the user wants calendar-based deletion without opening Codex, create a Windows Task Scheduler job only after explicit approval.

## Manifest Schema

Every run must have `manifest.json`:

```json
{
  "schema_version": 1,
  "creator_id": "mrbeast",
  "creator_name": "MrBeast",
  "run_id": "20260524-174500",
  "created_at": "2026-05-24T17:45:00+08:00",
  "retention": {
    "covers_delete_after_days": 30,
    "sources_delete_after_days": 90,
    "distillation": "keep",
    "prompts": "keep",
    "generated": "keep"
  },
  "covers": [],
  "process_sources": [],
  "artifacts": {
    "research_md": "distillation/research.md",
    "child_skill": null
  }
}
```

For each downloaded cover, append:

```json
{
  "index": 1,
  "video_title": "...",
  "video_url": "...",
  "thumbnail_url": "...",
  "local_path": "covers/001-title-slug.jpg",
  "selected_reason": "top viewed",
  "captured_at": "2026-05-24T17:50:00+08:00"
}
```

For each process source, append:

```json
{
  "title": "...",
  "url": "...",
  "local_path": "sources/articles/001-source-slug.md",
  "source_type": "interview|article|podcast|video|team-post",
  "captured_at": "2026-05-24T17:55:00+08:00"
}
```

## Rules

- If a cover is viewed but not downloaded, still record its URL in the research table.
- If a cover is downloaded, it must be under `covers\` and listed in `manifest.json`.
- If a source article/transcript is downloaded or copied, it must be under `sources\` and listed in `manifest.json`.
- Prefer `add-cover` and `add-source` over manual file moves because they copy the file and update `manifest.json` atomically from the agent workflow.
- If cleanup deletes raw files, keep the manifest entries and mark them with `"deleted_at"` and `"delete_reason"`.
- Child skills must not embed raw image files. They may embed distilled text and source URLs.

