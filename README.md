# Vox Director for Codex

A Codex skill for turning a topic or script into a finished Vox-style editorial paper-collage video.

This edition adapts [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) for a local Codex workflow:

- Codex built-in ImageGen by default, or explicit `gpt-image-2` through the API path
- HyperFrames for deterministic collage animation and rendering
- Optional Remotion backend when explicitly requested
- MiniMax narration and music through `mmx-cli`
- Live-rendered titles, captions, times, and numbers instead of generated text inside images
- No Atlas Cloud dependency

## Install with Codex

Give Codex this repository path and ask it to install the skill:

```text
Install this skill:
https://github.com/kakaxi12/vox-director-codex/tree/main/vox-director
```

Manual installation:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/kakaxi12/vox-director-codex.git
cp -R vox-director-codex/vox-director ~/.codex/skills/vox-director
```

Start a new Codex task after installation.

## Example

```text
Use $vox-director to create a Vox paper-collage video about how AI changes an ordinary person's day, with Chinese female narration, about 60 seconds, vertical 9:16.
```

## Runtime requirements

- Codex built-in `imagegen` skill
- HyperFrames skills/plugin
- Node.js 22+
- FFmpeg
- `mmx-cli` plus the user's own MiniMax credentials for generated narration or music

Built-in ImageGen does not require the user to provide an OpenAI API key. No API keys, generated videos, or private assets are included in this repository.

## License and attribution

This repository preserves the upstream license in `vox-director/LICENSE`. The workflow is adapted from [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director).
