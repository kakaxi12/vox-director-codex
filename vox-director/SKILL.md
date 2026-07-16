---
name: vox-director
description: Turn one topic into a finished Vox-style editorial paper-collage explainer or ad video using Codex ImageGen or explicit gpt-image-2, deterministic HyperFrames motion, MiniMax narration and music, captions, and local rendering. Use for requests such as "Vox video", "paper collage explainer", "motion collage", "拼贴视频", "Vox 风格视频", or turning a topic, product, person, event, or script into a narrated collage MP4 without Atlas Cloud or AI image-to-video.
---

# Vox Director

Create a rich editorial paper-collage video from one topic. Codex directs the workflow, ImageGen creates raster assets, HyperFrames animates them deterministically, MiniMax produces narration and music, and FFmpeg renders the final media.

Do not use Atlas Cloud. Do not use an AI image-to-video model unless the user explicitly asks for one as an exception.

## Load the required skills

Before doing production work:

1. Load the installed `imagegen` skill before generating or editing any bitmap.
2. Load `hyperframes` and `hyperframes-cli` before authoring, validating, previewing, or rendering motion.
3. Load `mmx-cli` before generating MiniMax speech or music.
4. Load `remotion-best-practices` only when the user explicitly chooses Remotion instead of HyperFrames.

Follow every loaded skill's save-path, validation, and fallback rules. Never reimplement their bundled tools.

## Default backends

| Stage | Default | Optional |
|---|---|---|
| Images | Codex built-in ImageGen | ImageGen CLI with explicit `gpt-image-2` and `OPENAI_API_KEY` |
| Motion | HyperFrames HTML/CSS/GSAP | Remotion when explicitly requested |
| Narration | MiniMax Speech via `mmx` | User-supplied audio |
| Music | MiniMax Music via `mmx` | User-supplied music or no music |
| Final render | HyperFrames + FFmpeg | Remotion render when selected |

Built-in ImageGen is the normal path and does not require `OPENAI_API_KEY`. Use the ImageGen CLI only when the user explicitly requests the API/model path, unattended batch generation, or exact `gpt-image-2` control. Never silently downgrade models.

## Project layout

Keep one project under `out/<slug>/`:

```text
out/<slug>/
├── project.json
├── beats.json
├── assets.json
├── DESIGN.md
├── prompts/
└── video/
    ├── index.html
    ├── compositions/
    └── media/
        ├── images/
        └── audio/
```

Initialize it with:

```bash
python3 scripts/init_project.py out/<slug> \
  --topic "<topic>" --language zh --aspect 16:9 --duration 30
npx --yes hyperframes init out/<slug>/video --example blank --non-interactive
mkdir -p out/<slug>/video/media/images out/<slug>/video/media/audio
```

If HyperFrames initialized `DESIGN.md` inside `video/`, keep the root `DESIGN.md` authoritative and copy its final values into the composition project.

## Workflow

### 1. Preflight

Check without exposing secrets:

```bash
node --version
ffmpeg -version
mmx auth status --output json --quiet
```

Require Node.js 22+, FFmpeg, and authenticated `mmx` only for stages that use them. Built-in ImageGen needs no API key.

### 2. Draft the beat map — Gate 1

Read `references/beat-layer.md` and `references/project-schema.md`. Build `beats.json` with:

- one narrative arc;
- hook, setup, escalation, payoff, and close;
- narration and exact on-screen text;
- duration and transition for every beat;
- a visual intent and a layer plan for every scene.

Present the beat map for approval before generating assets. This is the first human decision gate.

### 3. Define the visual identity — Gate 2

Read `references/visual-system.md`. Create `DESIGN.md` with:

- `## Style Prompt`
- `## Colors`
- `## Typography`
- `## Motion Language`
- `## What NOT to Do`

Generate the same representative beat in 3–4 coherent visual directions. Let the user choose by eye. This is the second human decision gate.

Do not pause again for routine production choices. Escalate only when a decision changes the narrative, identity, licensing, safety, or cost materially.

### 4. Plan and generate layered assets

Read `references/image-workflow.md`, then update `assets.json` before generation.

There is **no fixed limit** on cutouts, subjects, props, textures, labels, or decorative layers. Use as many elements as the scene benefits from. Control richness with hierarchy and readability:

- every layer must serve narrative, depth, rhythm, emphasis, or texture;
- group low-value decoration into reusable background plates when DOM or render cost rises;
- keep hero subjects and important props independently movable;
- keep critical text in HTML/CSS rather than baking it into images;
- avoid visual clutter that hides the focal point or captions.

For built-in ImageGen, generate one distinct asset or variant per tool call. Move every selected project asset into `video/media/images/`; never leave a referenced asset only under `$CODEX_HOME/generated_images/`.

For cutouts, follow the ImageGen skill's built-in chroma-key workflow and local removal helper. Use opaque torn-paper silhouettes, masks, CSS clipping, or full-poster motion when transparency would be fragile. Ask before any model/path downgrade required for complex native transparency.

Store the final prompt for every generated asset under `prompts/` and record its relative path and role in `assets.json`.

### 5. Generate narration and music

Read `references/audio-workflow.md`.

Generate one consistent narration track from the approved script. Prefer subtitle output from MiniMax; otherwise transcribe the final narration so caption timing reflects the actual audio.

Generate instrumental background music only when requested or appropriate. Keep narration dominant and duck music beneath speech.

### 6. Build deterministic motion

Read `references/hyperframes-workflow.md`, then follow the loaded HyperFrames skills.

Use the generated layers as a 2.5D paper stage:

- animate entrances, parallax, paper drift, pivot, scale, masks, texture movement, camera crops, and kinetic type;
- keep motion deterministic and timeline-seekable;
- build each scene's hero frame before animation;
- use transitions between every scene;
- keep exact text and captions as HTML;
- keep video and audio on separate tracks.

HyperFrames is the default because collage motion benefits from CSS layout, masks, blend modes, and GSAP choreography. If the user explicitly requests Remotion, read `references/remotion-workflow.md` and use React/TypeScript instead; do not maintain both backends in the same project.

### 7. Validate and render

Validate project data first:

```bash
python3 scripts/validate_project.py out/<slug> --stage plan
python3 scripts/validate_project.py out/<slug> --stage assets
```

Then validate the HyperFrames composition:

```bash
cd out/<slug>/video
npx hyperframes lint
npx hyperframes check --samples 15 --at-transitions
npx hyperframes render --quality draft --output ../draft.mp4
npx hyperframes render --quality high --output ../final.mp4
```

Inspect hero frames, transitions, caption readability, text overflow, contrast, clipping, narration sync, music ducking, and final duration. `check` is the current combined runtime, layout, motion, and contrast gate; use `inspect` only with an older HyperFrames CLI that does not provide `check`. Fix every unexplained error or warning before final delivery.

## Quality rules

- Keep the editorial paper-collage identity visible in every beat.
- Prefer rich, purposeful layering over arbitrary element counts.
- Vary scale, crop, rhythm, color field, and motion pattern across beats.
- Preserve the same palette, texture family, typography, and cutout treatment across the film.
- Avoid generic slideshow motion, repeated zooms, random movement, and empty scenes.
- Do not invent logos, copyrighted characters, celebrity likenesses, or licensed music beyond the user's authorization.
- Record plan versus generated assets accurately; do not mark a stage complete until files exist and validation passes.

## References

- `references/beat-layer.md` — narrative arcs, pacing, shots, and anti-monotony.
- `references/project-schema.md` — `beats.json` and `assets.json` contracts.
- `references/visual-system.md` — collage themes, style bake-off, typography, and prompt construction.
- `references/image-workflow.md` — ImageGen asset decomposition, generation, transparency, and save rules.
- `references/hyperframes-workflow.md` — composition structure, motion vocabulary, captions, QA, and render flow.
- `references/remotion-workflow.md` — optional Remotion backend.
- `references/audio-workflow.md` — MiniMax narration, music, captions, and mixing.
