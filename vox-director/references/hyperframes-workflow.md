# HyperFrames workflow

Load the installed `hyperframes` and `hyperframes-cli` skills before authoring or rendering. Their current rules override this summary.

## Structure

- Keep HTML as the source of truth.
- Use one root composition and sub-compositions for complex scenes.
- Build each scene's hero frame as static layout before adding GSAP.
- Use live HTML/CSS for headlines, labels and captions.
- Use wrappers for image transforms; do not animate media dimensions directly.
- Keep video muted and audio on separate tracks.

Map each `beats.json` layer to an element, reusable group, or background plate. There is no element-count cap. Use DOM groups for repeated decoration and CSS pseudo-elements for non-semantic texture when that reduces clutter.

## Motion vocabulary

Prefer paper-native motion:

- slide, reveal, peel, pivot, stamp, settle, drift, flutter and sway;
- depth-separated parallax;
- crop and mask reveals;
- paper-tear, ink-wipe, page-turn and color-field transitions;
- kinetic typography, marker strokes, circles and diagram traces;
- finite ambient grain, dust and light movement.

Keep motion deterministic. Do not use `Math.random()`, wall-clock time, asynchronous timeline construction, infinite repeats, or conflicting tweens.

## Scene choreography

- Offset the first entrance slightly from the scene start.
- Give every visible scene element an intentional entrance.
- Let the transition perform the exit; only the final scene may fade out directly.
- Vary entrance patterns and easing within and across scenes.
- Preserve the outgoing hero frame until the transition begins.
- Keep the caption safe area clear even in rich compositions.

## Audio and captions

Place narration and music as separate audio elements. Use real narration timing for subtitles. Keep normal caption text at readable video sizes and validate overflow at multiple timestamps.

## QA sequence

```bash
npx hyperframes lint
npx hyperframes check --samples 15 --at-transitions
npx hyperframes preview
npx hyperframes render --quality draft --output ../draft.mp4
npx hyperframes render --quality high --output ../final.mp4
```

`check` is the current combined runtime, layout, motion, and WCAG gate. Use `inspect` only when an older CLI does not provide `check`. Fix unexplained lint errors, contrast warnings, overflows, collisions, invisible elements, dead zones, abrupt transitions, and audio sync problems before final rendering.
