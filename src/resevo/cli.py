"""The supported Resevo command-line interface."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .core import resolve_paths
from .services import (
    doctor,
    init_workspace,
    migration_plan,
    run_legacy,
    status,
    workspace_add,
    workspace_list,
    workspace_remove,
    record_provenance,
)
from .mcp_installer import install as install_mcp
from .mcp_installer import status as mcp_status
from .mcp_installer import uninstall as uninstall_mcp
from .evolution import evaluate_guard


LEGACY_COMMANDS = {
    "closeout-check",
    "daily-cycle",
    "evaluate-legacy",
    "evolve-proposals",
    "kb-index",
    "project-bridge",
    "project-health",
    "registry",
    "run-capture",
    "self-evolution",
    "validate-asset-evolution",
    "validate-project",
    "visual-to-editable",
    "war-room",
}


def print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resevo",
        description="Resevo: Evidence-Governed Self-Evolving Research Workflow Harness.",
    )
    parser.add_argument("--root", "--workspace-root", dest="workspace_root", default=os.environ.get("RESEVO_WORKSPACE_ROOT") or os.environ.get("RESEVO_ROOT"))
    parser.add_argument("--engine-root", default=os.environ.get("RESEVO_ENGINE_ROOT"))
    parser.add_argument(
        "command",
        choices=sorted({"init", "doctor", "status", "workspace", "recall", "intake", "closeout", "evaluate", "evolve", "mcp", "migrate", "provenance", *LEGACY_COMMANDS}),
    )
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def _subparser(description: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=description)


def dispatch(command: str, args: list[str], paths) -> int:
    if command == "init":
        parser = _subparser("Initialize user and workspace-local Resevo state")
        parser.add_argument("--json", action="store_true")
        ns = parser.parse_args(args)
        result = init_workspace(paths)
        print_json(result)
        return 0
    if command == "doctor":
        parser = _subparser("Check Resevo installation and workspace")
        parser.add_argument("--json", action="store_true")
        parser.parse_args(args)
        result = doctor(paths)
        print_json(result)
        return 0 if result["ok"] else 1
    if command == "status":
        parser = _subparser("Show Resevo installation and workspace status")
        parser.add_argument("--json", action="store_true")
        parser.parse_args(args)
        print_json(status(paths))
        return 0
    if command == "workspace":
        parser = _subparser("Manage registered Resevo workspaces")
        parser.add_argument("action", choices=["add", "list", "remove"])
        parser.add_argument("name", nargs="?")
        parser.add_argument("root", nargs="?")
        ns = parser.parse_args(args)
        if ns.action == "list":
            print_json(workspace_list(paths))
            return 0
        if not ns.name:
            parser.error("workspace add/remove requires a name")
        if ns.action == "add":
            if not ns.root:
                parser.error("workspace add requires a root")
            print_json(workspace_add(paths, ns.name, ns.root))
            return 0
        print_json(workspace_remove(paths, ns.name))
        return 0
    if command == "recall":
        parser = _subparser("Recall reusable workflow evidence")
        parser.add_argument("--query", required=True)
        parser.add_argument("--project-root", default=str(paths.workspace))
        parser.add_argument("--limit", type=int, default=10)
        parser.add_argument("--json", action="store_true")
        ns = parser.parse_args(args)
        return run_legacy("self-evolution", ["recall", "--query", ns.query, "--project-root", ns.project_root, "--limit", str(ns.limit), "--json"], paths)
    if command == "intake":
        parser = _subparser("Create a self-evolution intake")
        parser.add_argument("--project-root", default=str(paths.workspace))
        parser.add_argument("--trigger", default="workflow improvement")
        parser.add_argument("--out", required=True)
        parser.add_argument("--json", action="store_true")
        ns = parser.parse_args(args)
        return run_legacy("self-evolution", ["init", "--project-root", ns.project_root, "--trigger", ns.trigger, "--out", ns.out], paths)
    if command == "closeout":
        result = run_legacy("closeout", args, paths)
        if result == 0:
            record_provenance(
                paths,
                "closeout",
                ["resevo", "closeout"],
                inputs=[],
                outputs=[str(paths.workspace / "state" / "closeout_health.json")],
            )
        return result
    if command == "evaluate":
        return run_legacy("evaluate", args or ["evaluate", "--target", "all", "--json"], paths)
    if command == "evolve":
        parser = _subparser("Propose or apply guarded workflow changes")
        parser.add_argument("action", choices=["propose", "apply", "promote"])
        parser.add_argument("--workflow-id", default="default-workflow")
        parser.add_argument("--champion-score", type=float)
        parser.add_argument("--candidate-score", type=float)
        parser.add_argument("--min-improvement", type=float, default=0.05)
        parser.add_argument("--held-out-pass", action="store_true")
        parser.add_argument("--next-bottleneck", default="Collect more held-out task evidence.")
        ns, remainder = parser.parse_known_args(args)
        if ns.action == "propose":
            return run_legacy("evolve", ["scan", *remainder], paths)
        if ns.action == "apply":
            if ns.champion_score is not None and ns.candidate_score is not None:
                result = evaluate_guard(
                    paths.workspace,
                    ns.workflow_id,
                    ns.champion_score,
                    ns.candidate_score,
                    held_out_pass=ns.held_out_pass,
                    minimum_improvement=ns.min_improvement,
                    next_bottleneck=ns.next_bottleneck,
                )
                print_json(result)
                return 0 if result["status"] == "candidate_accepted_for_experiment" else 1
            return run_legacy("evolve", ["scan", "--apply-safe", *remainder], paths)
        print_json({"ok": False, "status": "human_confirmation_required", "message": "Promotion is intentionally not automated by the current service layer."})
        return 2
    if command == "mcp":
        if args and args[0] == "--self-test":
            return run_legacy("mcp", ["--self-test", *args[1:]], paths)
        print_only = "--print" in args
        dry_run = "--dry-run" in args
        args = [item for item in args if item not in {"--print", "--dry-run"}]
        parser = _subparser("Serve the local Resevo MCP")
        parser.add_argument("action", choices=["serve", "self-test", "install", "status", "uninstall"])
        parser.add_argument("agent", nargs="?")
        parser.add_argument("args", nargs=argparse.REMAINDER)
        ns = parser.parse_args(args)
        if ns.action in {"install", "status", "uninstall"}:
            if not ns.agent:
                parser.error(f"mcp {ns.action} requires an agent")
            if ns.action == "install":
                result = install_mcp(paths, ns.agent, print_only=print_only, dry_run=dry_run)
            elif ns.action == "status":
                result = mcp_status(paths, ns.agent, print_only=print_only, dry_run=dry_run)
            else:
                result = uninstall_mcp(paths, ns.agent, print_only=print_only, dry_run=dry_run)
            print_json(result)
            return 0 if result.get("ok") else 1
        return run_legacy("mcp", (["--self-test"] if ns.action == "self-test" else ns.args), paths)
    if command == "migrate":
        parser = _subparser("Migrate ResearchLoop naming without rewriting history")
        parser.add_argument("target", choices=["researchloop"])
        parser.add_argument("--apply", action="store_true")
        ns = parser.parse_args(args)
        print_json(migration_plan(paths, ns.apply))
        return 0
    if command == "provenance":
        parser = _subparser("Record append-only run provenance")
        parser.add_argument("--label", default="resevo-run")
        parser.add_argument("--command", action="append", default=[])
        parser.add_argument("--input", action="append", default=[])
        parser.add_argument("--output", action="append", default=[])
        ns = parser.parse_args(args)
        print_json(record_provenance(paths, ns.label, ns.command, ns.input, ns.output))
        return 0
    if command in LEGACY_COMMANDS:
        aliases = {
            "closeout-check": "closeout",
            "evaluate-legacy": "evaluate",
            "evolve-proposals": "evolve",
            "project-health": "project-health",
            "self-evolution": "self-evolution",
            "registry": "registry",
            "kb-index": "kb-index",
        }
        return run_legacy(aliases.get(command, command), args, paths)
    raise SystemExit(f"unsupported Resevo command: {command}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    paths = resolve_paths(ns.workspace_root, ns.engine_root)
    return dispatch(ns.command, ns.args, paths)


if __name__ == "__main__":
    raise SystemExit(main())
