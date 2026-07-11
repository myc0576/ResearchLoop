"""Agent-safe installation helpers for the local stdio MCP server."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .core import Paths


MCP_SERVER_NAME = "resevo"
MCP_DISPLAY_NAME = "Resevo"
SUPPORTED_AGENTS = {"codex", "claude"}


def command_for(agent: str, action: str, paths: Paths | None = None) -> list[str]:
    if agent not in SUPPORTED_AGENTS:
        raise ValueError(f"unsupported agent: {agent}")
    if action == "add":
        command = [agent, "mcp", "add", MCP_SERVER_NAME, "--", "resevo"]
        if paths is not None:
            command.extend(["--workspace-root", str(paths.workspace), "--engine-root", str(paths.engine)])
        return [*command, "mcp", "serve"]
    if action == "get":
        return [agent, "mcp", "get", MCP_SERVER_NAME]
    if action == "remove":
        return [agent, "mcp", "remove", MCP_SERVER_NAME]
    raise ValueError(action)


def snippet(agent: str, paths: Paths | None = None) -> str:
    command = command_for(agent, "add", paths) if agent in SUPPORTED_AGENTS else [agent, "mcp", "add", MCP_SERVER_NAME, "--", "resevo", "mcp", "serve"]
    return " ".join(command)


def _record_preflight(paths: Paths, agent: str, action: str, completed: subprocess.CompletedProcess[str] | None) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = (completed.stdout if completed else "") + (completed.stderr if completed else "")
    record = {
        "schema": "resevo_mcp_preflight.v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "action": action,
        "command": snippet(agent, paths),
        "returncode": completed.returncode if completed else None,
        "output_sha256": hashlib.sha256(output.encode("utf-8", errors="replace")).hexdigest(),
        "output_length": len(output),
        "note": "Output content is intentionally not persisted; use the agent's official status command for details.",
    }
    path = paths.user / "mcp-preflight" / f"{stamp}-{agent}-{action}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _run(command: list[str]) -> subprocess.CompletedProcess[str] | None:
    if not shutil.which(command[0]):
        return None
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=30)
    except OSError:
        return None


def install(paths: Paths, agent: str, *, print_only: bool = False, dry_run: bool = False) -> dict[str, Any]:
    if agent not in SUPPORTED_AGENTS:
        return {"ok": print_only or dry_run, "agent": agent, "status": "unsupported_agent", "snippet": snippet(agent), "changed": False}
    command = command_for(agent, "add", paths)
    if print_only or dry_run:
        return {"ok": True, "agent": agent, "status": "dry_run", "command": command, "snippet": " ".join(command), "changed": False}
    if not shutil.which(agent):
        return {"ok": False, "agent": agent, "status": "agent_not_found", "snippet": " ".join(command), "changed": False}
    current = _run(command_for(agent, "get"))
    preflight = _record_preflight(paths, agent, "get", current)
    if current is not None and current.returncode == 0:
        return {"ok": True, "agent": agent, "status": "already_configured", "changed": False, "preflight": str(preflight)}
    result = _run(command)
    if result is None:
        return {"ok": False, "agent": agent, "status": "agent_not_found", "snippet": " ".join(command), "changed": False, "preflight": str(preflight)}
    return {"ok": result.returncode == 0, "agent": agent, "status": "installed" if result.returncode == 0 else "install_failed", "changed": result.returncode == 0, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "preflight": str(preflight)}


def status(paths: Paths, agent: str, *, print_only: bool = False, dry_run: bool = False) -> dict[str, Any]:
    if agent not in SUPPORTED_AGENTS:
        return {"ok": print_only or dry_run, "agent": agent, "status": "unsupported_agent", "snippet": snippet(agent)}
    command = command_for(agent, "get")
    if print_only or dry_run:
        return {"ok": True, "agent": agent, "status": "dry_run", "command": command}
    result = _run(command)
    if result is None:
        return {"ok": False, "agent": agent, "status": "agent_not_found", "command": command}
    preflight = _record_preflight(paths, agent, "status", result)
    return {"ok": result.returncode == 0, "agent": agent, "status": "configured" if result.returncode == 0 else "not_configured", "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr, "preflight": str(preflight)}


def uninstall(paths: Paths, agent: str, *, print_only: bool = False, dry_run: bool = False) -> dict[str, Any]:
    if agent not in SUPPORTED_AGENTS:
        return {"ok": print_only or dry_run, "agent": agent, "status": "unsupported_agent", "snippet": snippet(agent)}
    command = command_for(agent, "remove")
    if print_only or dry_run:
        return {"ok": True, "agent": agent, "status": "dry_run", "command": command, "changed": False}
    if not shutil.which(agent):
        return {"ok": False, "agent": agent, "status": "agent_not_found", "snippet": " ".join(command), "changed": False}
    result = _run(command)
    preflight = _record_preflight(paths, agent, "remove", result)
    return {"ok": result is not None and result.returncode == 0, "agent": agent, "status": "removed" if result and result.returncode == 0 else "remove_failed", "changed": bool(result and result.returncode == 0), "returncode": result.returncode if result else None, "stdout": result.stdout if result else "", "stderr": result.stderr if result else "", "preflight": str(preflight)}
