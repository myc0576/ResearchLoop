"""Deterministic, evidence-weighted ranking for local retrieval results."""

from __future__ import annotations

import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


UTILITY_FIELDS = (
    "semantic_relevance",
    "domain_fit",
    "evidence_grade",
    "successful_reuse_count",
    "failed_reuse_count",
    "last_used_at",
    "last_feedback",
    "utility_score",
    "provenance",
    "status",
)

EVIDENCE_SCORES = {"A": 1.0, "B": 0.8, "C": 0.55, "D": 0.3, "unknown": 0.0}


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    return value if isinstance(value, dict) else {}


def load_utility_overrides(registry_dir: Path) -> dict[str, dict[str, Any]]:
    """Load optional per-item metadata without changing existing registry files."""
    data = _read_yaml(registry_dir / "utility_metadata.yaml")
    rows = data.get("items", [])
    if not isinstance(rows, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        key = str(row.get("id") or row.get("path") or "").strip()
        if key:
            result[key] = {field: row[field] for field in UTILITY_FIELDS if field in row}
    return result


def load_registry_items(registry_dir: Path) -> dict[str, dict[str, Any]]:
    """Index registry records by id and path for metadata enrichment."""
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(registry_dir.glob("*.yaml")):
        if path.name == "utility_metadata.yaml":
            continue
        data = _read_yaml(path)
        for rows in data.values():
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                for key in (row.get("id"), row.get("path"), row.get("asset_dir")):
                    if key:
                        result[str(key)] = row
    return result


def _parse_date(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _evidence_grade(item: dict[str, Any]) -> str:
    explicit = str(item.get("evidence_grade") or "").upper()
    if explicit in EVIDENCE_SCORES:
        return explicit
    status = str(item.get("status") or "").lower()
    refs = item.get("evidence_refs") or item.get("verification_refs") or []
    if status in {"validated", "reusable", "approved", "pass", "paper_ready"} and refs:
        return "A"
    if status in {"validated", "reusable", "approved", "pass", "paper_ready"}:
        return "B"
    if status in {"candidate", "pending validation", "hypothesis"}:
        return "C" if status != "hypothesis" else "D"
    return "unknown"


def _freshness(item: dict[str, Any], now: datetime) -> float:
    date = _parse_date(item.get("last_used_at") or item.get("last_verified_at") or item.get("updated_at"))
    if date is None:
        return 0.25
    age_days = max(0.0, (now - date.astimezone(timezone.utc)).total_seconds() / 86400)
    return math.exp(-age_days / 90.0)


def _reuse_score(item: dict[str, Any]) -> float:
    success = max(0, int(item.get("successful_reuse_count", 0) or 0))
    failed = max(0, int(item.get("failed_reuse_count", 0) or 0))
    if success + failed == 0:
        return 0.5
    return success / (success + failed)


def enrich_result(
    result: dict[str, Any],
    rank: int,
    registry_items: dict[str, dict[str, Any]],
    overrides: dict[str, dict[str, Any]],
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    key_candidates = [str(result.get("id") or ""), str(result.get("path") or "")]
    base = {}
    for key in key_candidates:
        if key in registry_items:
            base = {**base, **registry_items[key]}
        if key in overrides:
            base = {**base, **overrides[key]}
    registry_id = str(base.get("id") or "")
    if registry_id in overrides:
        base = {**base, **overrides[registry_id]}
    semantic = max(0.0, min(1.0, 1.0 / (rank + 1)))
    domain_fit = float(base.get("domain_fit", 0.5) or 0.5)
    evidence_grade = _evidence_grade(base)
    utility = (
        0.30 * semantic
        + 0.15 * domain_fit
        + 0.20 * _reuse_score(base)
        + 0.20 * EVIDENCE_SCORES[evidence_grade]
        + 0.15 * _freshness(base, now)
    )
    metadata = {
        "semantic_relevance": round(semantic, 4),
        "domain_fit": round(domain_fit, 4),
        "evidence_grade": evidence_grade,
        "successful_reuse_count": int(base.get("successful_reuse_count", 0) or 0),
        "failed_reuse_count": int(base.get("failed_reuse_count", 0) or 0),
        "last_used_at": base.get("last_used_at", ""),
        "last_feedback": base.get("last_feedback", ""),
        "utility_score": round(utility, 4),
        "provenance": base.get("provenance") or {"registry": base.get("id", ""), "path": result.get("path", "")},
        "status": base.get("status", "unrated"),
    }
    return {**result, "utility": metadata}


def rank_results(
    results: list[dict[str, Any]],
    registry_dir: Path,
    limit: int = 10,
    minimum_reliable_score: float = 0.45,
) -> dict[str, Any]:
    """Rank FTS results and return null reuse when no result clears the reliability gate."""
    registry_items = load_registry_items(registry_dir)
    overrides = load_utility_overrides(registry_dir)
    enriched = [enrich_result(item, index, registry_items, overrides) for index, item in enumerate(results)]
    enriched.sort(key=lambda item: item["utility"]["utility_score"], reverse=True)
    enriched = enriched[: max(1, min(int(limit), 50))]
    selected = next(
        (
            item
            for item in enriched
            if item["utility"]["utility_score"] >= minimum_reliable_score
            and item["utility"]["evidence_grade"] != "unknown"
        ),
        None,
    )
    return {
        "results": enriched,
        "result_count": len(enriched),
        "reliable_result_count": sum(
            item["utility"]["utility_score"] >= minimum_reliable_score
            and item["utility"]["evidence_grade"] != "unknown"
            for item in enriched
        ),
        "reuse": (
            {
                "selected_path": selected.get("path"),
                "selected_title": selected.get("title"),
                "utility_score": selected["utility"]["utility_score"],
            }
            if selected
            else None
        ),
    }
