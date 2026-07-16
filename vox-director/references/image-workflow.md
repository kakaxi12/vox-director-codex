# Image workflow

Load the installed `imagegen` skill before using this reference.

## Choose the path

1. Use built-in ImageGen by default. It needs no `OPENAI_API_KEY`.
2. Use the bundled ImageGen CLI only when the user explicitly requests `gpt-image-2`, API/CLI control, or unattended batch generation.
3. Never substitute another model silently.

## Decompose each scene

Plan assets by visual role, not by a numeric quota. A scene may contain as many independently useful elements as it needs:

- background plates and large paper fields;
- isolated hero subjects;
- supporting subjects, objects, diagrams and icons;
- foreground occluders;
- texture, tape, shadows, marks and collage debris;
- full-poster fallback plates for scenes that do not need element-level motion.

Keep separate anything that needs independent timing, parallax, masking, emphasis, or reuse. Merge decoration only when it improves clarity or render performance.

## Generate

- Use one built-in ImageGen call per distinct asset or variant.
- Keep prompts under `prompts/` and tie them to asset IDs.
- Generate assets at the target aspect or with adequate crop room.
- Keep exact titles, numbers, labels and captions out of the bitmap.
- For isolated opaque paper cutouts, request a flat chroma-key background and follow the ImageGen skill's removal helper.
- For complex hair, glass, smoke, translucency, or reflective edges, do not claim a clean cutout until alpha validation passes. Prefer a full plate, mask, or compositing treatment before requesting a model downgrade.

## Persist and verify

Built-in ImageGen outputs initially live under `$CODEX_HOME/generated_images/`. Copy the selected project-bound output into `video/media/images/` with a stable, descriptive filename. Do not overwrite an accepted asset unless replacement was explicitly requested; use a versioned sibling filename.

Inspect each selected output for:

- correct subject, pose and crop;
- consistency with `DESIGN.md`;
- focal hierarchy and usable negative space;
- exact invariants for edits;
- no accidental words, watermarks, duplicated limbs, or malformed focal objects;
- clean alpha edges when transparency is required.

Update `assets.json` only after the final file is in the project.
