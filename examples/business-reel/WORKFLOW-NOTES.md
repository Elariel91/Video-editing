# Lessons from the completed edit

## Tool ownership

Use FilmCraft for source ranges, cuts, reframing, color correction and final sound/export. Use HyperFrames for seekable text animation, graphics and word-timed captions. Use PhotoCraft for layered covers. Add other effects tools only when the edit benefits.

## FilmCraft CLI

- Inspect `commands --json`, `describe`, `effects.list` and the active sequence instead of guessing schemas.
- Source monitor state does not survive independent CLI invocations. Put `source.open` and `source.overwrite` in one JSONL `run` call.
- `exec` usually returns one JSON object; `run` returns JSON Lines. Parse both forms.
- Time is 254016000000 ticks per second. Align edit positions to frames before converting to ticks.
- Discover item, clip and track IDs. The original clean sequence used item 8 and clip 9; those numbers are not a universal contract.
- To add another sound layer without overwriting the voice, place it after the current sequence, then move the new clip to the intended audio track at time zero.
- Save and verify the timeline. The finished example has eight picture cuts, eight markers and three separate audio clips.
- Use `file.exportMedia` with `wait: true`; inspect export results for offline media before reporting completion.

## HyperFrames

- Start IDs with letters. Numeric-leading IDs break unescaped CSS/GSAP selectors.
- Read and write all source JSON/HTML as UTF-8. Platform-default text decoding caused visible punctuation corruption during the first pass.
- A caption overlay inheriting `inset:0` needs `bottom:auto` and a bounded content height; otherwise its black background can extend down the frame.
- Keep headline, takeaway, teaching graphics and captions in separate vertical zones. Long headlines can wrap and collide with the takeaway.
- Match a footage clip's declared time window to the scene. The example slows its five-second selects to cover the complete scene, avoiding a black panel after the source ends.
- Use one paused registered timeline per composition. Animate children, leaving framework-controlled clip visibility alone.
- Keep fonts and GSAP local for the render. Run the full check and inspect a contact sheet before encoding.
- One render worker was reliable on the original 8 GB Windows computer. More workers consume more browser memory.

## Audio and delivery

- Plan timing from the generated speech, not estimated reading speed. Keep deliberate pauses between steps.
- Measure integrated loudness and true peak. The example applies voice gain, a quiet original score, short accents, fades and a master limiter in FilmCraft, then requests −16 LUFS on export.
- Decode the actual final MP4 and inspect sample frames after the final editor export. A clean graphics render does not prove that the finishing export is correct.
- Verify duration, dimensions, frame rate, audio streams and missing-media status before delivery.

## Portability

Resolve application executables from PATH or environment variables. Keep dependencies in a virtual environment and local npm folder. Do not commit application binaries, caches, personal logs, credentials or machine-specific project files. Rebuild FilmCraft projects on the destination computer so media paths resolve there.
