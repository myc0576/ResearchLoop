"""Small append-only provenance records for local research workflow runs."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _hash(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def record_run(
    workspace: Path,
    label: str,
    command: Iterable[str],
    *,
    inputs: Iterable[str | Path] = (),
    outputs: Iterable[str | Path] = (),
    decision: dict[str, Any] | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Write a run and its hashes without copying any artifact contents."""
    run_id = run_id or f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    run_dir = workspace / ".resevo" / "runs" / run_id
    input_paths = [Path(item).expanduser() for item in inputs]
    output_paths = [Path(item).expanduser() for item in outputs]
    artifacts = [
        {"role": "input", "path": str(path), "sha256": _hash(path)} for path in input_paths
    ] + [
        {"role": "output", "path": str(path), "sha256": _hash(path)} for path in output_paths
    ]
    created_at = _now()
    run = {
        "schema": "resevo.run.v1",
        "run_id": run_id,
        "label": label,
        "created_at": created_at,
        "command": list(command),
        "workspace": str(workspace),
        "environment_summary": {"python": sys.version.split()[0], "platform": platform.platform()},
        "input_hashes": {str(path): _hash(path) for path in input_paths},
        "output_hashes": {str(path): _hash(path) for path in output_paths},
    }
    manifest = {"schema": "resevo.artifact_manifest.v1", "run_id": run_id, "artifacts": artifacts}
    decision_record = {
        "schema": "resevo.decision_record.v1",
        "run_id": run_id,
        "decision": decision or {"status": "recorded", "human_promotion_required": True},
        "created_at": created_at,
    }
    _write_json(run_dir / "run.json", run)
    _write_json(run_dir / "artifact_manifest.json", manifest)
    _write_json(run_dir / "decision_record.json", decision_record)
    _write_json(run_dir / "environment.json", run["environment_summary"])
    trace = run_dir / "trace.jsonl"
    with trace.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event": "run_recorded", "run_id": run_id, "created_at": created_at}, ensure_ascii=False) + "\n")
    reproduction = [
        f"# Reproduction Entry: {label}",
        "",
        f"- run_id: `{run_id}`",
        f"- command: `{list(command)}`",
        f"- workspace: `{workspace}`",
        "- Inputs and outputs are referenced by path and SHA-256; contents are not copied into Resevo.",
        "- Re-run the command after verifying the referenced paths and the human decision gate.",
        "",
    ]
    (run_dir / "reproduction_entry.md").write_text("\n".join(reproduction), encoding="utf-8")
    return {"ok": True, "run_id": run_id, "run_dir": str(run_dir), "artifact_count": len(artifacts)}
