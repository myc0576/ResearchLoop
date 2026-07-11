"""Guarded, deterministic workflow evolution primitives."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROMOTION_STATUSES = {"validated", "reusable", "approved", "pass", "paper_ready"}


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def evaluate_guard(
    workspace: Path,
    workflow_id: str,
    champion_score: float,
    candidate_score: float,
    *,
    held_out_pass: bool = False,
    minimum_improvement: float = 0.05,
    diff: dict[str, Any] | None = None,
    next_bottleneck: str = "Collect more held-out task evidence.",
) -> dict[str, Any]:
    """Evaluate a candidate without promoting any registry status."""
    run_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    run_dir = workspace / ".mycevo" / "evolution" / run_id
    improvement = float(candidate_score) - float(champion_score)
    threshold_pass = improvement >= float(minimum_improvement)
    accepted = bool(held_out_pass and threshold_pass)
    status = "candidate_accepted_for_experiment" if accepted else "reverted"
    contract = {
        "schema": "mycevo.evolution_contract.v1",
        "workflow_id": workflow_id,
        "minimum_improvement": float(minimum_improvement),
        "requires_held_out_pass": True,
        "requires_human_promotion": True,
        "forbidden_automatic_statuses": sorted(PROMOTION_STATUSES),
    }
    metrics = {
        "champion_score": float(champion_score),
        "candidate_score": float(candidate_score),
        "improvement": round(improvement, 8),
        "held_out_pass": bool(held_out_pass),
        "threshold_pass": threshold_pass,
    }
    decision = {
        "schema": "mycevo.evolution_decision.v1",
        "run_id": run_id,
        "workflow_id": workflow_id,
        "status": status,
        "apply_allowed": accepted,
        "promotion_required": True,
        "metrics": metrics,
        "next_bottleneck": next_bottleneck,
        "rollback": {
            "performed": not accepted,
            "champion_preserved": True,
            "reason": "candidate did not clear held-out and minimum-improvement gates" if not accepted else "available if later validation regresses",
        },
        "created_at": _now(),
    }
    _write_json(run_dir / "contract.json", contract)
    _write_json(run_dir / "champion.json", {"workflow_id": workflow_id, "score": float(champion_score), "role": "champion"})
    _write_json(run_dir / "candidate.json", {"workflow_id": workflow_id, "score": float(candidate_score), "role": "candidate", "status": "candidate"})
    _write_json(run_dir / "diff.json", diff or {"changed": [], "note": "No executable mutation supplied; guard records the comparison only."})
    _write_json(run_dir / "state.json", {"phase": "reverted" if not accepted else "apply_allowed_pending_human_review", **decision})
    _append_jsonl(run_dir / "trace.jsonl", {"event": "observe", "created_at": _now(), "workflow_id": workflow_id})
    _append_jsonl(run_dir / "trace.jsonl", {"event": "evaluate", "created_at": _now(), "metrics": metrics})
    _append_jsonl(run_dir / "trace.jsonl", {"event": "diagnose", "created_at": _now(), "next_bottleneck": next_bottleneck})
    _append_jsonl(run_dir / "trace.jsonl", {"event": "apply_or_revert", "created_at": _now(), "status": status})
    _write_json(run_dir / "decision.json", decision)
    return {**decision, "run_dir": str(run_dir)}
