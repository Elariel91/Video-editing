# FilmCraft + HyperFrames + PhotoCraft: business Reel

Reusable source from a completed 54.5-second, 1080×1920, 30 fps Reel. The original version was rendered with FilmCraft 0.8.0, HyperFrames 0.8.162 and PhotoCraft 0.9.0 on Windows. This package removes the original computer's paths.

## Set up another computer

Install Python 3.11+, Node.js 22+, Chrome, FilmCraft and PhotoCraft. Obtain the Craft apps from their official projects: [FilmCraft](https://github.com/storytold/filmcraft) and [PhotoCraft](https://github.com/storytold/photocraft). Use the tested versions above when reproducing the example; inspect CLI command schemas before adapting to newer versions.

From the repository root, in PowerShell:

```powershell
cd examples/business-reel
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
npm install --prefix tools

# Set these to the actual files on THIS computer, or put both CLIs on PATH.
$env:FILMCRAFT_CLI = 'C:\path\to\filmcraft-cli.exe'
$env:PHOTOCRAFT_CLI = 'C:\path\to\photocraft-cli.exe'
```

Do not copy the example paths literally. These environment variables are process-local. The scripts can resolve CLIs on PATH on other operating systems, but only Windows was tested. The bundled ffprobe dependency might not provide every architecture; install ffprobe on PATH if needed.

## Build the video

Run these stages in order from this directory:

```powershell
python tools/run.py assets
python tools/run.py narrate
python tools/run.py prepare
python tools/run.py broll
python tools/run.py build
python tools/run.py check
python tools/run.py snapshot
python tools/run.py preview
```

Inspect the preview and contact sheet. Fix errors before rendering, then run:

```powershell
python tools/run.py render
python tools/run.py finish
python tools/run.py cover
```

The finished MP4, script, SRT and layered cover are written to `deliverables/`. The editable FilmCraft project is `business-reel-final.fcproj`. The finishing stage refuses to replace an existing final project; move previous outputs aside before rebuilding. The B-roll stage reuses existing corrected selects; move those aside if you change their settings.

Narration uses Microsoft Aria through `edge-tts`, which requires network access and an available remote speech endpoint; it is not offline TTS. The asset stage downloads stock clips and open-license fonts from their publishers. Check current source terms in [SOURCES.md](SOURCES.md). Applications, dependencies, footage and generated media are not redistributed here. The score and sound accents are generated locally by `prepare_media.py`.

## What is reusable

- `scenes.json`: narration, labels, headlines and short teaching prompts.
- `tools/filmcraft_broll.py`: marked source ranges, reframing and restrained Lumetri correction.
- `tools/build_video.py`: eight portrait scenes, a consistent graphic treatment, word-timed captions and SRT.
- `tools/finish_filmcraft.py`: separate voice/music/accent tracks, music fades, master limiter, scene markers and final export.
- `tools/make_cover.py`: editable PhotoCraft type and shape layers with PSD, PNG and JPEG exports.
- [WORKFLOW-NOTES.md](WORKFLOW-NOTES.md): practical lessons and verification steps.

This is an adaptable worked example, not a general-purpose video editor. It expects eight scenes: hook, six steps, close. Layouts, cover copy and footage selections are tailored to this topic. To change the topic, edit both `scenes.json` and the relevant layout/cover constants. Keep headlines short and validate the result. `SCRIPT.md` is regenerated from the narration input. The music timing follows actual speech duration; the preparation stage checks the 40–60 second requirement.

The scripts use the tested clean-project FilmCraft ID allocation in the B-roll example. Before changing sequence track counts or adding earlier imports, inspect returned IDs and update the example. Regenerated FilmCraft projects contain absolute media paths for the current computer, so rebuild them on the new machine rather than copying an old `.fcproj` alone.

## Validation

The original production passed HyperFrames lint/runtime/layout/contrast checks, and its finished FilmCraft MP4 decoded successfully. The final measured duration was 54.485 seconds with H.264 video, AAC stereo audio and approximately −16.06 LUFS integrated loudness. The portable package has been syntax-checked; it has not been rendered on a second computer.
