#!/usr/bin/env python3
"""Validate Vox Director v2 planning, asset, and render state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DESIGN_HEADINGS = (
    "## Style Prompt",
    "## Colors",
    "## Typography",
    "## Motion Language",
    "## What NOT to Do",
)


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing {path.name}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name} must contain a JSON object")
        return {}
    return value


def duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}


def validate(root: Path, stage: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    state = load_json(root / "project.json", errors)
    beats_doc = load_json(root / "beats.json", errors)
    assets_doc = load_json(root / "assets.json", errors)

    for name, doc in (("project.json", state), ("beats.json", beats_doc), ("assets.json", assets_doc)):
        if doc and doc.get("schema_version") != 2:
            errors.append(f"{name} schema_version must be 2")

    design_path = root / "DESIGN.md"
    if not design_path.is_file():
        errors.append("missing DESIGN.md")
    else:
        design = design_path.read_text(encoding="utf-8")
        for heading in DESIGN_HEADINGS:
            if heading not in design:
                errors.append(f"DESIGN.md missing heading: {heading}")
        if "pending" in design.lower():
            warnings.append("DESIGN.md still contains pending values")

    project = beats_doc.get("project", {}) if isinstance(beats_doc.get("project"), dict) else {}
    for field in ("title", "topic", "language", "aspect", "fps", "target_duration", "motion_backend", "image_backend"):
        if not project.get(field):
            errors.append(f"beats.json project.{field} is required")

    beats = beats_doc.get("beats", [])
    if not isinstance(beats, list) or not beats:
        errors.append("beats.json beats must be a non-empty list")
        beats = []

    beat_ids: list[str] = []
    layer_ids_by_beat: dict[str, set[str]] = {}
    total_duration = 0.0
    for index, beat in enumerate(beats):
        where = f"beats[{index}]"
        if not isinstance(beat, dict):
            errors.append(f"{where} must be an object")
            continue
        beat_id = beat.get("id")
        if not isinstance(beat_id, str) or not beat_id:
            errors.append(f"{where}.id is required")
            continue
        beat_ids.append(beat_id)
        duration = beat.get("duration")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"{where}.duration must be positive")
        else:
            total_duration += float(duration)
        if not beat.get("narration") and not beat.get("silent_purpose"):
            warnings.append(f"{beat_id} has no narration or silent_purpose")
        for field in ("purpose", "visual_intent", "transition"):
            if not beat.get(field):
                errors.append(f"{where}.{field} is required")
        layers = beat.get("layers", [])
        if not isinstance(layers, list):
            errors.append(f"{where}.layers must be a list")
            layers = []
        layer_ids: list[str] = []
        for layer_index, layer in enumerate(layers):
            if not isinstance(layer, dict):
                errors.append(f"{where}.layers[{layer_index}] must be an object")
                continue
            layer_id = layer.get("id")
            if not isinstance(layer_id, str) or not layer_id:
                errors.append(f"{where}.layers[{layer_index}].id is required")
            else:
                layer_ids.append(layer_id)
        for duplicate in sorted(duplicates(layer_ids)):
            errors.append(f"duplicate layer id in {beat_id}: {duplicate}")
        layer_ids_by_beat[beat_id] = set(layer_ids)

    for duplicate in sorted(duplicates(beat_ids)):
        errors.append(f"duplicate beat id: {duplicate}")

    target = project.get("target_duration")
    if isinstance(target, (int, float)) and target > 0 and beats:
        tolerance = max(0.5, float(target) * 0.05)
        if abs(total_duration - float(target)) > tolerance:
            warnings.append(f"beat duration total {total_duration:.2f}s differs from target {float(target):.2f}s")

    assets = assets_doc.get("assets", [])
    if not isinstance(assets, list):
        errors.append("assets.json assets must be a list")
        assets = []
    asset_ids: list[str] = []
    allowed_statuses = {"planned", "ready", "rejected", "missing"}
    for index, asset in enumerate(assets):
        where = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{where} must be an object")
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id:
            errors.append(f"{where}.id is required")
        else:
            asset_ids.append(asset_id)
        beat_id = asset.get("beat_id")
        if beat_id not in layer_ids_by_beat:
            errors.append(f"{where}.beat_id references unknown beat: {beat_id}")
        layer_id = asset.get("layer_id")
        if layer_id and beat_id in layer_ids_by_beat and layer_id not in layer_ids_by_beat[beat_id]:
            errors.append(f"{where}.layer_id references unknown layer: {beat_id}/{layer_id}")
        status = asset.get("status", "planned")
        if status not in allowed_statuses:
            errors.append(f"{where}.status must be one of {sorted(allowed_statuses)}")
        rel_path = asset.get("path")
        if status == "ready":
            if not isinstance(rel_path, str) or not rel_path:
                errors.append(f"{where}.path is required when status is ready")
            elif not (root / rel_path).is_file():
                errors.append(f"ready asset file missing: {rel_path}")
            prompt_file = asset.get("prompt_file")
            if prompt_file and not (root / prompt_file).is_file():
                errors.append(f"prompt file missing: {prompt_file}")

    for duplicate in sorted(duplicates(asset_ids)):
        errors.append(f"duplicate asset id: {duplicate}")

    approvals = state.get("approvals", {}) if isinstance(state.get("approvals"), dict) else {}
    if stage in {"assets", "render"}:
        if not approvals.get("beat_map"):
            errors.append("beat map is not approved in project.json")
        if not approvals.get("visual_identity"):
            errors.append("visual identity is not approved in project.json")
        ready_count = sum(1 for asset in assets if isinstance(asset, dict) and asset.get("status") == "ready")
        if ready_count == 0:
            warnings.append("no ready generated or supplied assets are recorded")

    if stage == "render":
        backend = project.get("motion_backend")
        if backend == "hyperframes" and not (root / "video" / "index.html").is_file():
            errors.append("missing video/index.html for HyperFrames render stage")
        if backend == "remotion" and not (root / "video" / "package.json").is_file():
            errors.append("missing video/package.json for Remotion render stage")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--stage", choices=("plan", "assets", "render"), default="plan")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = args.project_dir.expanduser().resolve()
    errors, warnings = validate(root, args.stage)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"validation {'passed' if not errors else 'failed'}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
