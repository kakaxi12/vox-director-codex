# Optional Remotion workflow

Use this backend only when the user explicitly requests Remotion or needs React/TypeScript components and Remotion Studio editing. Do not build both HyperFrames and Remotion versions in one project.

Load `remotion-best-practices` and every rule file it routes to for the requested features.

- Scaffold with the current Remotion command from that skill.
- Keep assets under `public/` and load them through `staticFile()`.
- Animate from `useCurrentFrame()` with `interpolate()`; do not use CSS animations or transitions.
- Use `<Sequence>` for beat timing and `@remotion/media` for audio/video.
- Keep composition dimensions, FPS, duration and default props visible together.
- Render representative still frames before a full MP4.
- Preserve the same `beats.json`, `assets.json`, `DESIGN.md`, ImageGen workflow and MiniMax audio workflow used by the HyperFrames route.
