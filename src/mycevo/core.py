"""Portable MycEvo paths and configuration primitives."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _path_from_env(*names: str) -> Path | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return Path(value).expanduser().resolve()
    return None


def engine_root() -> Path:
    return _path_from_env("MYCEVO_ENGINE_ROOT", "RESEVO_ENGINE_ROOT", "RESEARCHLOOP_ENGINE_ROOT", "RESEARCHLOOP_PUBLIC_ROOT") or Path(__file__).resolve().parents[2]


def default_workspace_root() -> Path:
    return _path_from_env("MYCEVO_WORKSPACE_ROOT", "MYCEVO_ROOT", "RESEVO_WORKSPACE_ROOT", "RESEVO_ROOT", "RESEARCHLOOP_ROOT") or Path.cwd().resolve()


def user_root() -> Path:
    return _path_from_env("MYCEVO_USER_ROOT", "RESEVO_USER_ROOT") or (Path.home() / ".mycevo").resolve()

    


@dataclass(frozen=True)
class Paths:
    engine: Path
    workspace: Path
    user: Path

    @property
    def workspace_meta(self) -> Path:
        return self.workspace / ".mycevo"

    @property
    def workspace_config(self) -> Path:
        return self.workspace_meta / "config.yaml"

    @property
    def legacy_workspace_meta(self) -> Path:
        return self.workspace / ".resevo"

    @property
    def user_config(self) -> Path:
        return self.user / "config.yaml"

    @property
    def workspaces_file(self) -> Path:
        return self.user / "workspaces.yaml"


def resolve_paths(workspace: str | Path | None = None, engine: str | Path | None = None) -> Paths:
    return Paths(
        engine=Path(engine).expanduser().resolve() if engine else engine_root(),
        workspace=Path(workspace).expanduser().resolve() if workspace else default_workspace_root(),
        user=user_root(),
    )


def read_yaml(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return default if data is None else data


def write_yaml_if_missing(path: Path, data: Any) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return True


def write_json_if_missing(path: Path, data: Any) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True
