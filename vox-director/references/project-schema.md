# Project schema

Use `beats.json` for narrative and scene intent. Use `assets.json` for actual generated or supplied files. Never store secrets in either file.

## `beats.json`

```json
{
  "schema_version": 2,
  "project": {
    "title": "A brief history of money",
    "topic": "How money changed",
    "language": "en",
    "aspect": "16:9",
    "fps": 30,
    "target_duration": 15,
    "motion_backend": "hyperframes",
    "image_backend": "codex-imagegen",
    "audio_backend": "minimax"
  },
  "visual": {
    "preset": "american-retro",
    "density": "rich",
    "style_prompt": "Editorial torn-paper collage..."
  },
  "beats": [
    {
      "id": "b01",
      "duration": 5,
      "purpose": "hook",
      "narration": "Before coins, value had many shapes.",
      "headline": "BEFORE MONEY",
      "visual_intent": "A dense field of barter objects converges on a coin-shaped void.",
      "transition": "paper-tear-wipe",
      "layers": [
        {
          "id": "barter-field",
          "role": "supporting-collage",
          "asset_kind": "generated-cutout-group",
          "motion": "staggered-rise-parallax",
          "z": 20
        }
      ]
    }
  ]
}
```

Rules:

- `schema_version` must be `2`.
- Beat IDs and layer IDs must be unique within their scope.
- Every duration must be positive.
- Every beat must have narration or an explicit silent purpose.
- `layers` may contain any number of entries, including zero for a deliberate type-only scene. There is no fixed cap.
- `z` controls visual stacking; it does not replace HyperFrames track indices.
- `transition` names intent. The final implementation must map it to a valid deterministic transition.

## `assets.json`

```json
{
  "schema_version": 2,
  "assets": [
    {
      "id": "b01-barter-field",
      "beat_id": "b01",
      "layer_id": "barter-field",
      "role": "supporting-collage",
      "path": "video/media/images/b01-barter-field.png",
      "source": "codex-imagegen",
      "prompt_file": "prompts/b01-barter-field.txt",
      "status": "ready",
      "license_note": "AI generated for this project"
    }
  ]
}
```

Allowed `status` values: `planned`, `ready`, `rejected`, `missing`.

For `ready`, the referenced file must exist. Record user-supplied asset provenance and license limits accurately. Do not mark planned assets ready after merely generating a prompt.

## `project.json`

Use `project.json` for stage state only:

```json
{
  "schema_version": 2,
  "stage": "plan",
  "approvals": {
    "beat_map": false,
    "visual_identity": false
  }
}
```

Advance `stage` only after the corresponding files exist and validation succeeds.
