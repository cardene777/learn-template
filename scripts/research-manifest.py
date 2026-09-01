#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / ".codex" / "research-runs"
ALLOWED_STAGES = {
    "pending",
    "writing",
    "interrogating",
    "reviewing",
    "needs_revalidation",
    "blocked",
    "done",
}


def read_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        data[key.strip()] = value
    return data


def source_index() -> tuple[dict[str, dict], dict[str, str | None]]:
    by_id: dict[str, dict] = {}
    parents: dict[str, str | None] = {}
    for path in (ROOT / "contents").rglob("*.md"):
        fm = read_front_matter(path)
        item_id = fm.get("id")
        if not item_id:
            continue
        rel = path.relative_to(ROOT).as_posix()
        by_id[item_id] = {"path": rel, "front": fm, "text": path.read_text(encoding="utf-8")}
        parents[item_id] = fm.get("directoryId") or None
    return by_id, parents


def under_root(item_id: str, root_id: str, parents: dict[str, str | None]) -> bool:
    if item_id == root_id:
        return True
    seen: set[str] = set()
    cur = parents.get(item_id)
    while cur and cur not in seen:
        if cur == root_id:
            return True
        seen.add(cur)
        cur = parents.get(cur)
    return False


def manifest_paths(explicit: list[str]) -> list[Path]:
    if explicit:
        return [(ROOT / p).resolve() if not Path(p).is_absolute() else Path(p) for p in explicit]
    if not MANIFEST_DIR.exists():
        return []
    return sorted(MANIFEST_DIR.glob("*.json"))


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: manifest JSON unreadable: {exc}"]

    name = manifest.get("target") or path.stem
    root_id = manifest.get("rootDirectoryId")
    items = manifest.get("items")
    if not root_id:
        errors.append(f"{name}: rootDirectoryId is required")
    if not isinstance(items, list) or not items:
        errors.append(f"{name}: items must be a non-empty list")
        return errors

    by_id, parents = source_index()
    planned_ids: set[str] = set()

    for index, item in enumerate(items):
        prefix = f"{name}: items[{index}]"
        item_id = item.get("id")
        if not item_id:
            errors.append(f"{prefix}: id is required")
            continue
        if item_id in planned_ids:
            errors.append(f"{name}: duplicate planned id: {item_id}")
        planned_ids.add(item_id)

        stage = item.get("stage", "pending")
        if stage not in ALLOWED_STAGES:
            errors.append(f"{name}: {item_id}: invalid stage={stage}")
        if manifest.get("status") == "done" and stage != "done":
            errors.append(f"{name}: {item_id}: manifest is done but item stage={stage}")

        actual = by_id.get(item_id)
        if not actual:
            errors.append(f"{name}: planned item missing from source: {item_id}")
            continue

        expected_path = item.get("sourcePath")
        if expected_path and actual["path"] != expected_path:
            errors.append(
                f"{name}: {item_id}: path mismatch expected={expected_path} actual={actual['path']}"
            )

        front = actual["front"]
        for field in ("type", "title", "directoryId", "permalink"):
            expected = item.get(field)
            if expected is None:
                continue
            actual_value = front.get(field) or None
            if actual_value != expected:
                errors.append(
                    f"{name}: {item_id}: {field} mismatch expected={expected!r} actual={actual_value!r}"
                )

        if item.get("kind") and front.get("type") != item.get("kind"):
            errors.append(
                f"{name}: {item_id}: kind mismatch expected={item.get('kind')} actual={front.get('type')}"
            )

        if front.get("type") == "Note" and item.get("route") in {"Overview", "Mechanism"}:
            text = actual["text"]
            if "<details>" not in text or "<summary>" not in text or "</details>" not in text:
                errors.append(f"{name}: {item_id}: routed Note has no source Markdown term toggle")
            if "<details class=" in text or 'markdown="1"' in text:
                errors.append(
                    f"{name}: {item_id}: toggle syntax must stay simple (<details>/<summary> only)"
                )

    if root_id:
        actual_ids = {
            item_id
            for item_id in by_id
            if under_root(item_id, root_id, parents)
        }
        ignored = set(manifest.get("ignoreActualIds", []))
        unexpected = sorted(actual_ids - planned_ids - ignored)
        missing = sorted(planned_ids - actual_ids)
        if unexpected:
            errors.append(f"{name}: unexpected actual items under {root_id}: {', '.join(unexpected)}")
        if missing:
            errors.append(f"{name}: planned items not reachable under {root_id}: {', '.join(missing)}")

    return errors


def validate(paths: list[Path]) -> int:
    if not paths:
        print("Research manifest validation: no manifests found.")
        return 0
    errors: list[str] = []
    for path in paths:
        errors.extend(validate_manifest(path))
    if errors:
        print("Research manifest validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Research manifest validation OK: {len(paths)} manifest(s).")
    return 0


def resume(path: Path) -> int:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for item in manifest.get("items", []):
        if item.get("stage", "pending") != "done":
            print(json.dumps(item, ensure_ascii=False, indent=2))
            return 0
    print("ALL_DONE")
    return 0


def checkpoint(path: Path, item_id: str, stage: str) -> int:
    if stage not in ALLOWED_STAGES:
        raise SystemExit(f"invalid stage: {stage}")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    found = False
    for item in manifest.get("items", []):
        if item.get("id") == item_id:
            item["stage"] = stage
            item["attempts"] = int(item.get("attempts", 0)) + (1 if stage == "writing" else 0)
            item["updatedAt"] = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")
            found = True
            break
    if not found:
        raise SystemExit(f"item not found: {item_id}")
    manifest["status"] = "done" if all(i.get("stage") == "done" for i in manifest.get("items", [])) else "in_progress"
    manifest["updatedAt"] = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M JST")
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"checkpointed {item_id} -> {stage}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and resume approved research build manifests")
    sub = parser.add_subparsers(dest="command")
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("paths", nargs="*")
    p_resume = sub.add_parser("resume")
    p_resume.add_argument("path")
    p_checkpoint = sub.add_parser("checkpoint")
    p_checkpoint.add_argument("path")
    p_checkpoint.add_argument("item_id")
    p_checkpoint.add_argument("stage", choices=sorted(ALLOWED_STAGES))
    args = parser.parse_args()

    if args.command in (None, "validate"):
        return validate(manifest_paths(getattr(args, "paths", [])))
    if args.command == "resume":
        return resume((ROOT / args.path).resolve())
    if args.command == "checkpoint":
        return checkpoint((ROOT / args.path).resolve(), args.item_id, args.stage)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
