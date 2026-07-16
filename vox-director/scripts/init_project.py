#!/usr/bin/env python3
"""Initialize a Vox Director v2 project without making paid API calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--title")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--aspect", choices=("16:9", "9:16", "1:1", "4:5"), default="16:9")
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--fps", type=int, choices=(24, 30, 60), default=30)
    parser.add_argument("--motion", choices=("hyperframes", "remotion"), default="hyperframes")
    parser.add_argument("--image", choices=("codex-imagegen", "gpt-image-2"), default="codex-imagegen")
    parser.add_argument("--force", action="store_true", help="Replace only generated metadata files")
    args = parser.parse_args()

    if args.duration <= 0:
        parser.error("--duration must be positive")

    root = args.project_dir.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "prompts").mkdir(exist_ok=True)

    generated = [root / "project.json", root / "beats.json", root / "assets.json", root / "DESIGN.md"]
    existing = [p for p in generated if p.exists()]
    if existing and not args.force:
        names = ", ".join(p.name for p in existing)
        parser.error(f"refusing to overwrite existing files: {names}; use --force intentionally")

    title = args.title or args.topic
    project = {
        "schema_version": 2,
        "stage": "plan",
        "approvals": {"beat_map": False, "visual_identity": False},
    }
    beats = {
        "schema_version": 2,
        "project": {
            "title": title,
            "topic": args.topic,
            "language": args.language,
            "aspect": args.aspect,
            "fps": args.fps,
            "target_duration": args.duration,
            "motion_backend": args.motion,
            "image_backend": args.image,
            "audio_backend": "minimax",
        },
        "visual": {"preset": "pending", "density": "rich", "style_prompt": "pending approval"},
        "beats": [
            {
                "id": "b01",
                "duration": args.duration,
                "purpose": "hook-to-payoff placeholder",
                "narration": "",
                "headline": title,
                "visual_intent": "Replace with the approved beat map.",
                "transition": "final-fade",
                "layers": [],
            }
        ],
    }
    assets = {"schema_version": 2, "assets": []}
    design = f"""# {title} — Visual Identity

## Style Prompt

Pending style bake-off and approval.

## Colors

- Background: `#F3E8CF`
- Ink: `#181411`
- Accent: `#D94832`

## Typography

- Display: pending
- Body and captions: pending

## Motion Language

Paper-native entrances, layered parallax, deterministic transitions. Refine after approval.

## What NOT to Do

- No glossy 3D or plastic CGI.
- No generic slideshow zooms.
- No random motion without narrative purpose.
"""

    write_json(root / "project.json", project)
    write_json(root / "beats.json", beats)
    write_json(root / "assets.json", assets)
    (root / "DESIGN.md").write_text(design, encoding="utf-8")

    print(f"initialized {root}")
    for path in generated:
        print(path.relative_to(root))
    print("next: approve beats.json, approve DESIGN.md, then scaffold the selected motion backend")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
