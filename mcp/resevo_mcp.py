from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from resevo.core import Paths
from resevo.services import run_legacy

ROOT = Path(__file__).absolute().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from _harness_common import (  # noqa: E402
    REGISTRY_FILES,
    REUSABLE_KNOWLEDGE_ROOT,
    REUSABLE_PROMPTS_ROOT,
    STATE_DIR,
    append_ledger,
    is_subpath,
    now_iso,
    read_yaml,
    write_yaml,
)
import kb_index  # noqa: E402


mcp = FastMCP("Resevo")

ALLOWED_READ_ROOTS = [
    REUSABLE_KNOWLEDGE_ROOT,
    REUSABLE_PROMPTS_ROOT,
    ROOT / "system_design",
    ROOT / "skills",
    ROOT / "decisions",
    ROOT / "reports",
    ROOT / "registry",
]
FEEDBACK_TYPES = {"useful", "wrong", "outdated", "needs_review"}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def assert_allowed_doc(path: Path) -> None:
    resolved = path.resolve()
    if not any(is_subpath(resolved, root) for root in ALLOWED_READ_ROOTS):
        raise ValueError(f"path outside research harness readable roots: {path}")
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(str(path))


def _search_kb_impl(query: str, limit: int = 10) -> dict[str, Any]:
    if not (STATE_DIR / "kb_index" / "research_kb.sqlite").exists():
        kb_index.rebuild()
    return kb_index.search(query, max(1, min(int(limit), 50)))


def _read_kb_doc_impl(path: str) -> dict[str, Any]:
    doc = Path(path)
    assert_allowed_doc(doc)
    text = doc.read_text(encoding="utf-8", errors="replace")
    return {"path": str(doc), "content": text[:20000], "truncated": len(text) > 20000}


def _get_closeout_health_impl() -> dict[str, Any]:
    return read_json(STATE_DIR / "closeout_health.json")


def _get_project_health_impl(project_id: str | None = None) -> dict[str, Any]:
    data = read_json(STATE_DIR / "project_health.json")
    if project_id:
        projects = [row for row in data.get("projects", []) if row.get("project_id") == project_id]
        return {"project_id": project_id, "projects": projects, "count": len(projects)}
    return data


def _list_proposals_impl(status: str | None = None) -> dict[str, Any]:
    proposal_dir = STATE_DIR / "proposals"
    files = sorted(proposal_dir.glob("*_evolution_proposals.json")) if proposal_dir.exists() else []
    if not files:
        return {"proposal_count": 0, "proposals": []}
    data = read_json(files[-1])
    proposals = data.get("proposals", [])
    if status:
        proposals = [item for item in proposals if item.get("status") == status]
    return {"proposal_count": len(proposals), "source": str(files[-1]), "proposals": proposals}


def _list_candidates_impl() -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for name in ("knowledge", "prompts", "research_assets", "decisions", "workflow_improvement_backlog"):
        path = REGISTRY_FILES.get(name)
        if not path:
            continue
        data = read_yaml(path)
        for item in data.get(name, []) if isinstance(data, dict) else []:
            if str(item.get("status", "")).lower() in {"candidate", "pending validation"}:
                candidates.append({"registry": name, **item})
    return {"candidate_count": len(candidates), "candidates": candidates}


def _run_legacy_service(name: str, args: list[str]) -> dict[str, Any]:
    paths = Paths(engine=ENGINE_ROOT, workspace=ROOT, user=ROOT / ".resevo")
    return {"ok": run_legacy(name, args, paths) == 0, "command": [name, *args]}


def _record_feedback_impl(target_id: str, feedback_type: str, note: str = "") -> dict[str, Any]:
    if feedback_type not in FEEDBACK_TYPES:
        raise ValueError(f"feedback_type must be one of {sorted(FEEDBACK_TYPES)}")
    path = REGISTRY_FILES["feedback"]
    data = read_yaml(path)
    data.setdefault("version", 1)
    data.setdefault("feedback", [])
    item = {
        "id": f"fb_{now_iso().replace(':', '').replace('-', '')}_{uuid.uuid4().hex[:8]}",
        "target_id": target_id,
        "feedback_type": feedback_type,
        "note": note,
        "created_at": now_iso(),
        "source": "resevo_mcp",
    }
    data["feedback"].append(item)
    write_yaml(path, data)
    ledger = append_ledger("mcp_record_feedback", {"target_id": target_id, "feedback_type": feedback_type, "feedback_id": item["id"]})
    return {"ok": True, "feedback": item, "ledger_path": ledger["ledger_path"]}


@mcp.tool()
def search_kb(query: str, limit: int = 10) -> dict[str, Any]:
    """Search the local SQLite FTS5 research knowledge index."""
    return _search_kb_impl(query, limit)


@mcp.tool()
def search_knowledge(query: str, limit: int = 10) -> dict[str, Any]:
    """Search reusable knowledge and prompts through the local index."""
    result = _search_kb_impl(query, limit)
    result["results"] = [item for item in result.get("results", []) if item.get("kind") in {"knowledge", "prompts"}]
    result["result_count"] = len(result["results"])
    return result


@mcp.tool()
def search_workflows(query: str, limit: int = 10) -> dict[str, Any] | None:
    """Search workflow, decision, asset, and proposal records."""
    result = _search_kb_impl(query, limit)
    result["results"] = [item for item in result.get("results", []) if item.get("kind") in {"research_assets", "decisions", "workflow_improvement_backlog", "registry"}]
    result["result_count"] = len(result["results"])
    return result if result["results"] else {"ok": True, "query": query, "result_count": 0, "results": [], "reuse": None}


@mcp.tool()
def read_kb_doc(path: str) -> dict[str, Any]:
    """Read a whitelisted knowledge, prompt, harness design, registry, decision, or report document."""
    return _read_kb_doc_impl(path)


@mcp.tool()
def get_closeout_health() -> dict[str, Any]:
    """Return the latest closeout health JSON."""
    return _get_closeout_health_impl()


@mcp.tool()
def get_project_health(project_id: str | None = None) -> dict[str, Any]:
    """Return latest project health for all projects or a specific project_id."""
    return _get_project_health_impl(project_id)


@mcp.tool()
def list_proposals(status: str | None = None) -> dict[str, Any]:
    """List latest evolution proposals, optionally filtered by status."""
    return _list_proposals_impl(status)


@mcp.tool()
def list_candidates() -> dict[str, Any]:
    """List candidate and pending-validation workflow records."""
    return _list_candidates_impl()


@mcp.tool()
def record_feedback(target_id: str, feedback_type: str, note: str = "") -> dict[str, Any]:
    """Record feedback for a registry item. This is the MCP server's only write tool."""
    return _record_feedback_impl(target_id, feedback_type, note)


@mcp.tool()
def create_intake(project_root: str | None = None, trigger: str = "MCP intake", out: str | None = None) -> dict[str, Any]:
    """Create a candidate-first self-evolution intake through the CLI service."""
    target_root = Path(project_root or ROOT)
    output = Path(out) if out else target_root / ".resevo" / "intake.yaml"
    output.parent.mkdir(parents=True, exist_ok=True)
    result = _run_legacy_service("self-evolution", ["init", "--project-root", str(target_root), "--trigger", trigger, "--out", str(output)])
    return {**result, "out": str(output)}


@mcp.tool()
def run_closeout() -> dict[str, Any]:
    """Run the existing closeout service and return its status."""
    return _run_legacy_service("closeout", [])


@mcp.tool()
def propose_workflow_change() -> dict[str, Any]:
    """Create reviewable workflow proposals without applying or promoting them."""
    return _run_legacy_service("evolve", ["scan"])


def self_test() -> dict[str, Any]:
    rebuild = kb_index.rebuild()
    search = _search_kb_impl("SC-NMT", 5)
    health = _get_closeout_health_impl()
    projects = _get_project_health_impl()
    feedback = _record_feedback_impl("self-test", "needs_review", "MCP self-test write boundary check")
    return {
        "ok": bool(rebuild.get("ok")) and search.get("result_count", 0) >= 0 and feedback.get("ok"),
        "rebuild": rebuild,
        "search_result_count": search.get("result_count"),
        "closeout_health_loaded": bool(health),
        "project_health_loaded": bool(projects),
        "feedback_id": feedback["feedback"]["id"],
    }


def print_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Resevo MCP stdio server")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
        print_json(result)
        return 0 if result["ok"] else 1
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
