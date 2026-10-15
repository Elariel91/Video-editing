---
name: filmcraft
description: Edit video projects with FilmCraft through its MCP server. Use for importing media, inspecting timelines, cutting and arranging clips, grading, mixing, previewing, and exporting FilmCraft projects.
---

# FilmCraft

Use the FilmCraft MCP tools to operate on the user's video project. This is a local integration guide based on the upstream documentation, not an upstream-distributed skill.

## Prerequisites

FilmCraft and `filmcraft-cli` must be installed, and the CLI must be registered as an MCP server in the agent client. See [connection instructions](references/connection.md). If the tools are unavailable, explain the missing connection; do not pretend edits or exports ran.

## Editing workflow

1. Establish the input media, desired edit, project location, and output requirements from the request and existing project.
2. Call `doc_inspect`, or `project_inspect` and `sequence_inspect`, to discover actual item, track, and clip IDs.
3. Use `command_list` to discover supported command IDs, parameters, and enabled states. Do not invent commands or reuse stale IDs.
4. Import media with `media_import` using absolute paths. Preserve the source media and save edits to the intended project.
5. Apply edits with `command_run`. For an ordered group, use `command_batch` with `stop_on_error` and inspect each result before continuing.
6. Check the resulting timeline and render representative frames with `render_frame` or `render_preview`. Inspect audio and export settings where relevant. Use `edit.undo` when an edit produces the wrong result.
7. Save the project and export only to the requested destination. Avoid overwriting unrelated files.
8. Verify export completion and the resulting media before claiming success. Report skipped or unavailable checks explicitly.

## Timing and export

FilmCraft uses 254016000000 ticks per second. Commands may support seconds, frames, or timecode; inspect their schemas and preserve the sequence's frame rate. Track parameters must refer to real tracks.

For headless video export, discover `file.exportMedia` parameters and use `wait: true` when waiting for completion. Otherwise inspect the returned job using the available job commands until it finishes. Check `offlineMedia`: a successful export can still contain placeholders for unavailable sources. Do not describe that result as a complete export without disclosing missing media.

## Desktop workflows

Bridge mode additionally exposes UI inspection, element discovery, clicks, drags, keyboard input, and screenshots. Prefer discovered element IDs and inspect the current UI before interacting. Headless mode has no desktop UI.

## Source

Upstream: https://github.com/storytold/filmcraft

Documentation reviewed at commit `8309f21a6c3f34ddf190af7fd9bfd913053a1fd5`: `docs/agents.md` and `README.md`. Consult current upstream documentation and live tool schemas when behavior differs.
