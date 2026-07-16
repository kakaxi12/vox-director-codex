# Visual system

Use this reference when defining `DESIGN.md`, running the style bake-off, or writing prompts for editorial collage assets.

## Visual identity

The shared identity is modern editorial paper collage:

- hand-cut silhouettes, torn edges, tape, staples, folds, newsprint, halftone and risograph grain;
- strong editorial hierarchy with one unmistakable focal point;
- flat printed materials with shallow 2.5D depth rather than glossy 3D objects;
- a controlled palette that changes emphasis without changing the film's identity;
- typography rendered in HTML/CSS for exact text and animation.

`DESIGN.md` is authoritative. Define exact colors, type families, texture treatment, motion language, and anti-patterns before composing video.

## Style bake-off

Pick one representative beat with a clear subject and meaningful composition. Create 3–4 directions using the same content, aspect ratio, and headline. Change only the visual system so the user can compare fairly.

Suggested presets:

| Preset | Palette | Type | Print finish | Motion character |
|---|---|---|---|---|
| `american-retro` | bold primaries | slab / wood type | aged halftone | punchy |
| `swiss-modern` | neutral + red accent | grotesk | clean grain | precise |
| `punk-zine` | black/white + spot color | ransom / condensed | photocopy | chaotic but controlled |
| `constructivist` | red/black/cream | condensed diagonal | letterpress | forceful |
| `wpa-poster` | muted triad | stencil / gothic | screenprint | steady |
| `70s-groovy` | mustard/rust/avocado | display serif | risograph | elastic |
| `chinese-ink` | ink/vermilion/rice | brush + seal accents | fibrous paper | lyrical |
| `atomic-age` | teal/orange/cream | geometric display | halftone | buoyant |

The user may mix or name another direction. Do not force a preset when explicit brand or reference material exists.

## Prompt structure

Write one prompt per distinct generated asset. Start with the asset's role and scene, then subject, material, composition, light, palette, and constraints.

```text
Use case: ads-marketing or illustration-story
Asset type: <background plate | hero cutout | prop | texture | decorative layer>
Primary request: <what the asset must depict>
Scene/backdrop: <environment or flat chroma key>
Subject: <main subject and pose>
Style/medium: editorial paper collage, hand-cut printed paper
Composition/framing: <crop, angle, negative space, intended placement>
Lighting/mood: flat printed shading, <mood>
Color palette: <DESIGN.md colors>
Materials/textures: torn fibers, newsprint, tape, halftone, ink misregistration
Constraints: isolated silhouette where required; no watermark; no unintended text
Avoid: glossy 3D, smooth vector gradients, plastic CGI, crowded focal area
```

Do not ask the image model to solve motion. Generate a readable asset in its most useful hero-frame state; HyperFrames supplies animation later.

## Text policy

Keep these as live HTML/CSS whenever possible:

- headlines and labels;
- dates, numbers and quotations;
- captions and credits;
- brand copy that must be exact.

Bake text into imagery only when illegibility is intentional texture, such as newspaper fragments or background scribbles. Never rely on baked text for the main message.

## Richness without a layer cap

There is no minimum or maximum layer count. Build richness from roles:

- background plate and large color fields;
- hero subjects;
- supporting subjects and props;
- foreground occluders;
- paper scraps, tape, marks, arrows and diagrams;
- texture and light overlays;
- live typography and captions.

Keep every independently meaningful or independently moving element separate. Combine repeated low-value decoration into a plate when it improves render performance or clarity.

## Consistency checks

- Same edge language: torn, scissor-cut, or geometric—not all three randomly.
- Same shadow logic: direction, softness, and depth.
- Same grain family and paper temperature.
- Same typography roles across scenes.
- Palette variations remain traceable to `DESIGN.md`.
- Motion vocabulary supports the visual identity rather than fighting it.
