# MiniMax audio workflow

Load the installed `mmx-cli` skill before generating audio.

## Preflight

```bash
mmx auth status --output json --quiet
```

Do not print or store the full key. The CLI may use its persisted config even when `MINIMAX_API_KEY` is not exported.

## Narration

List the live voice IDs and choose one that matches the narration language and tone:

```bash
mmx speech voices --output json --quiet
```

Always pass `--voice` explicitly; the CLI default is an English narrator even when `--language zh` is set. Create one narration script from approved beats and keep a consistent voice, language and speed. Example:

```bash
mmx speech synthesize \
  --text-file narration.txt \
  --model speech-2.8-hd \
  --voice "Chinese (Mandarin)_News_Anchor" \
  --language zh \
  --subtitles \
  --out video/media/audio/narration.mp3 \
  --non-interactive --quiet
```

If subtitle output is unavailable or inaccurate, transcribe the final narration through HyperFrames and use that timing. Do not time captions from estimated reading speed after final audio exists.

## Music

Prefer instrumental music that supports the selected visual identity without competing with narration:

```bash
mmx music generate \
  --prompt "editorial documentary score, tactile percussion, restrained build" \
  --instrumental \
  --use-case "background music for a narrated collage explainer" \
  --out video/media/audio/music.mp3 \
  --non-interactive --quiet
```

Use the free model only when its rate and quality trade-offs are acceptable. Direct MiniMax calls may consume quota; do not claim that bypassing Atlas makes image, speech, or music generation universally free.

## Mix

- Narration leads at all times.
- Duck music under speech and fade it cleanly at the end.
- Normalize obvious loudness differences without crushing dynamics.
- Keep captions aligned to the final narration file.
- Do not use copyrighted reference tracks or cloned voices without authorization.
