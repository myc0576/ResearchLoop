from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).absolute().parents[1]
RULES_PATH = ROOT / "workflows" / "visual_to_editable" / "router_rules.yaml"

FORBIDDEN_REPO_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".gif",
    ".webp",
    ".pdf",
    ".pptx",
    ".mp4",
    ".mov",
}

TEXT_ASSET_EXTENSIONS = {
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".csv",
    ".mmd",
    ".svg",
}

REQUEST_FIELDS = ["source", "target_outputs"]
MANIFEST_FIELDS = [
    "schema",
    "reconstruction_id",
    "status",
    "selected_route",
    "external_tool",
    "source_policy",
    "prompt_path",
    "output_paths",
    "editable_output_inventory",
    "qa",
    "reproduction_command",
    "closeout_links",
]
SOURCE_POLICY_FIELDS = ["source_reference", "input_type", "sensitivity", "commit_allowed", "committed_source_paths"]
QA_FIELDS = [
    "editability_score",
    "editable_text_count",
    "ocr_text_alignment_status",
    "layout_overlap_score",
    "render_comparison_status",
    "full_slide_background_residue",
    "manual_review_status",
]
CASE_REQUIRED_FILES = [
    "request.yaml",
    "visual_reconstruction_manifest.yaml",
    "visual_reconstruction_qa.md",
    "visual_reconstruction_prompt.md",
    "figure_card.md",
    "reproduction_entry.md",
]


def ensure_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def norm(value: Any) -> str:
    return str(value or "").strip().lower()


def norm_set(values: Any) -> set[str]:
    return {norm(value) for value in ensure_list(values) if norm(value)}


def read_yaml_document(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".md":
        text = extract_yaml_from_markdown(text)
    data = yaml.safe_load(text) if text.strip() else {}
    return data if isinstance(data, dict) else {}


def extract_yaml_from_markdown(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("---"):
        match = re.match(r"(?s)^---\s*\n(.*?)\n---", stripped)
        if match:
            return match.group(1)
    match = re.search(r"(?s)```ya?ml\s*\n(.*?)\n```", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def load_rules(path: Path = RULES_PATH) -> dict[str, Any]:
    data = read_yaml_document(path)
    data.setdefault("routes", [])
    data.setdefault("default_route", "manual_review")
    return data


def route_ids(rules: dict[str, Any]) -> set[str]:
    return {str(route.get("id")) for route in rules.get("routes", []) if route.get("id")}


def route_by_id(rules: dict[str, Any], route_id: str) -> dict[str, Any] | None:
    for route in rules.get("routes", []):
        if route.get("id") == route_id:
            return route
    return None


def infer_input_type(source: dict[str, Any]) -> str:
    explicit = norm(source.get("input_type"))
    if explicit:
        return explicit
    raw_path = str(source.get("path") or source.get("reference") or "")
    suffix = Path(raw_path).suffix.lower()
    if suffix == ".pdf":
        return "slide_pdf"
    if suffix == ".pptx":
        return "image_based_pptx"
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}:
        return "slide_image"
    return ""


def score_route(request: dict[str, Any], route: dict[str, Any]) -> tuple[float, dict[str, list[str]]]:
    source = ensure_dict(request.get("source"))
    input_type = infer_input_type(source)
    signals = norm_set(request.get("visual_signals"))
    targets = norm_set(request.get("target_outputs"))

    route_input_types = norm_set(route.get("input_types"))
    route_signals = norm_set(route.get("visual_signals"))
    route_targets = norm_set(route.get("target_outputs"))

    matched = {
        "input_type": [],
        "visual_signals": sorted(signals & route_signals),
        "target_outputs": sorted(targets & route_targets),
    }
    score = 0.0
    if input_type and input_type in route_input_types:
        score += 30
        matched["input_type"] = [input_type]
    score += len(matched["visual_signals"]) * 5
    score += len(matched["target_outputs"]) * 4
    if norm(request.get("route_hint")) == norm(route.get("id")):
        score += 100
    return score, matched


def confidence_for_score(score: float) -> str:
    if score >= 40:
        return "high"
    if score >= 20:
        return "medium"
    if score > 0:
        return "low"
    return "manual_review"


def manual_review_result(request: dict[str, Any], warnings: list[str]) -> dict[str, Any]:
    return {
        "ok": True,
        "selected_route": "manual_review",
        "confidence": "manual_review",
        "score": 0,
        "matched": {"input_type": [], "visual_signals": [], "target_outputs": []},
        "route": {
            "id": "manual_review",
            "external_tool_candidates": [],
            "target_outputs": ensure_list(request.get("target_outputs")),
            "closeout_required": [
                "source_policy",
                "human_route_decision",
                "visual_reconstruction_manifest",
            ],
            "safety_notes": ["Route is ambiguous or under-specified; require human review before reconstruction."],
        },
        "warnings": warnings,
    }


def classify_request(request: dict[str, Any], rules: dict[str, Any] | None = None) -> dict[str, Any]:
    rules = rules or load_rules()
    warnings: list[str] = []
    for field in REQUEST_FIELDS:
        if field not in request or request.get(field) in (None, "", []):
            warnings.append(f"missing_request_field:{field}")

    explicit_route = norm(request.get("route_hint"))
    if explicit_route and explicit_route in route_ids(rules):
        route = route_by_id(rules, explicit_route)
        assert route is not None
        return {
            "ok": True,
            "selected_route": explicit_route,
            "confidence": "high",
            "score": 100,
            "matched": {"input_type": [], "visual_signals": [], "target_outputs": []},
            "route": route_summary(route),
            "warnings": warnings,
        }

    best_route: dict[str, Any] | None = None
    best_score = 0.0
    best_rank = -1.0
    best_matched: dict[str, list[str]] = {"input_type": [], "visual_signals": [], "target_outputs": []}
    for route in rules.get("routes", []):
        score, matched = score_route(request, route)
        priority = float(route.get("priority") or 0) / 1000
        ranked = score + priority
        if score > 0 and ranked > best_rank:
            best_route = route
            best_score = score
            best_rank = ranked
            best_matched = matched

    if not best_route or best_score <= 0:
        return manual_review_result(request, warnings)

    score_without_priority = round(best_score, 2)
    return {
        "ok": True,
        "selected_route": best_route["id"],
        "confidence": confidence_for_score(score_without_priority),
        "score": score_without_priority,
        "matched": best_matched,
        "route": route_summary(best_route),
        "warnings": warnings,
    }


def route_summary(route: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "id",
        "target_outputs",
        "external_tool_candidates",
        "closeout_required",
        "safety_notes",
    ]
    return {key: route.get(key, [] if key != "id" else "") for key in keys}


def resolve_relative(base_dir: Path, raw: Any) -> Path | None:
    if not raw:
        return None
    path = Path(str(raw))
    if path.is_absolute():
        return path
    return base_dir / path


def suffix_for(raw: Any) -> str:
    return Path(str(raw)).suffix.lower()


def is_forbidden_repo_payload(raw: Any) -> bool:
    return suffix_for(raw) in FORBIDDEN_REPO_EXTENSIONS


def is_text_asset(raw: Any) -> bool:
    return suffix_for(raw) in TEXT_ASSET_EXTENSIONS


def check_relative_file(base_dir: Path, raw: Any, label: str, errors: list[str], warnings: list[str]) -> None:
    if not raw:
        errors.append(f"missing_path:{label}")
        return
    path = resolve_relative(base_dir, raw)
    if path is None:
        errors.append(f"missing_path:{label}")
        return
    if not path.exists():
        errors.append(f"missing_path:{label}:{raw}")
    elif path.is_file() and is_forbidden_repo_payload(path):
        errors.append(f"forbidden_repo_payload:{label}:{raw}")
    elif path.is_file() and not path.is_absolute() and not is_text_asset(path):
        warnings.append(f"non_text_asset_path:{label}:{raw}")


def validate_manifest_data(data: dict[str, Any], base_dir: Path, rules: dict[str, Any] | None = None) -> dict[str, Any]:
    rules = rules or load_rules()
    errors: list[str] = []
    warnings: list[str] = []

    for field in MANIFEST_FIELDS:
        if field not in data or data.get(field) in (None, "", []):
            errors.append(f"missing_required_field:{field}")

    selected_route = str(data.get("selected_route") or "")
    allowed_routes = route_ids(rules) | {"manual_review"}
    if selected_route and selected_route not in allowed_routes:
        errors.append(f"unknown_route:{selected_route}")

    status = norm(data.get("status"))
    if status == "validated" and data.get("human_approved") is not True:
        errors.append("unsafe_validated_without_human_approval")

    external_tool = ensure_dict(data.get("external_tool"))
    if not external_tool.get("id"):
        errors.append("missing_external_tool:id")

    source_policy = ensure_dict(data.get("source_policy"))
    for field in SOURCE_POLICY_FIELDS:
        if field not in source_policy or source_policy.get(field) in (None, ""):
            if field == "commit_allowed" and source_policy.get(field) is False:
                continue
            if field == "committed_source_paths" and source_policy.get(field) == []:
                continue
            errors.append(f"missing_source_policy:{field}")

    committed_sources = ensure_list(source_policy.get("committed_source_paths"))
    for raw in committed_sources:
        if is_forbidden_repo_payload(raw):
            errors.append(f"forbidden_committed_source:{raw}")
    if source_policy.get("commit_allowed") is False and committed_sources:
        errors.append("commit_disallowed_but_committed_source_paths_present")

    qa = ensure_dict(data.get("qa"))
    for field in QA_FIELDS:
        if field not in qa or qa.get(field) in (None, ""):
            errors.append(f"missing_qa_field:{field}")
    for field in ["editability_score", "layout_overlap_score"]:
        if field in qa:
            try:
                score = float(qa[field])
            except (TypeError, ValueError):
                errors.append(f"invalid_score:{field}")
            else:
                if score < 0 or score > 1:
                    errors.append(f"score_out_of_range:{field}:{score}")
    if "editable_text_count" in qa:
        try:
            count = int(qa["editable_text_count"])
        except (TypeError, ValueError):
            errors.append("invalid_editable_text_count")
        else:
            if count < 0:
                errors.append("invalid_editable_text_count")

    output_paths = ensure_dict(data.get("output_paths"))
    for raw in ensure_list(output_paths.get("editable_assets")):
        if is_forbidden_repo_payload(raw):
            errors.append(f"forbidden_repo_payload:editable_asset:{raw}")
        path = resolve_relative(base_dir, raw)
        if path and not path.exists() and not Path(str(raw)).is_absolute():
            errors.append(f"missing_path:editable_asset:{raw}")
    for label, raw in [
        ("prompt_path", data.get("prompt_path")),
        ("output_manifest", output_paths.get("output_manifest")),
        ("qa_report", output_paths.get("qa_report")),
    ]:
        check_relative_file(base_dir, raw, label, errors, warnings)

    closeout_links = ensure_dict(data.get("closeout_links"))
    for label in ["figure_card", "reproduction_entry", "qa_report"]:
        check_relative_file(base_dir, closeout_links.get(label), f"closeout_links.{label}", errors, warnings)

    if not data.get("reproduction_command"):
        errors.append("missing_reproduction_command")

    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "selected_route": selected_route,
        "status": data.get("status"),
    }


def validate_manifest_file(path: Path) -> dict[str, Any]:
    data = read_yaml_document(path)
    result = validate_manifest_data(data, path.parent)
    result["manifest"] = str(path)
    return result


def scan_forbidden_case_payloads(case_dir: Path) -> list[str]:
    found: list[str] = []
    for path in case_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in FORBIDDEN_REPO_EXTENSIONS:
            found.append(str(path.relative_to(case_dir)))
    return sorted(found)


def validate_case_dir(case_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not case_dir.exists() or not case_dir.is_dir():
        return {"ok": False, "errors": [f"missing_case_dir:{case_dir}"], "warnings": [], "case_dir": str(case_dir)}

    for name in CASE_REQUIRED_FILES:
        if not (case_dir / name).exists():
            errors.append(f"missing_case_file:{name}")

    for rel in scan_forbidden_case_payloads(case_dir):
        errors.append(f"forbidden_case_payload:{rel}")

    classification: dict[str, Any] = {}
    request_path = case_dir / "request.yaml"
    if request_path.exists():
        classification = classify_request(read_yaml_document(request_path))
    else:
        classification = {"ok": False, "selected_route": "", "warnings": []}

    expected_path = case_dir / "expected_route.yaml"
    if expected_path.exists() and classification.get("selected_route"):
        expected = read_yaml_document(expected_path)
        expected_route = expected.get("selected_route")
        if expected_route and expected_route != classification.get("selected_route"):
            errors.append(f"route_mismatch:expected:{expected_route}:actual:{classification.get('selected_route')}")

    manifest_result: dict[str, Any] = {}
    manifest_path = case_dir / "visual_reconstruction_manifest.yaml"
    if manifest_path.exists():
        manifest_result = validate_manifest_file(manifest_path)
        errors.extend(manifest_result.get("errors", []))
        warnings.extend(manifest_result.get("warnings", []))
        if classification.get("selected_route") and manifest_result.get("selected_route") != classification.get("selected_route"):
            errors.append(
                f"manifest_route_mismatch:classification:{classification.get('selected_route')}:manifest:{manifest_result.get('selected_route')}"
            )

    qa_text = (case_dir / "visual_reconstruction_qa.md").read_text(encoding="utf-8", errors="replace") if (case_dir / "visual_reconstruction_qa.md").exists() else ""
    for token in ["Editability", "OCR", "Layout", "Background Residue", "Manual Review"]:
        if token.lower() not in qa_text.lower():
            errors.append(f"qa_missing_section:{token}")

    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "case_dir": str(case_dir),
        "classification": classification,
        "manifest": manifest_result,
    }


def print_result(data: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
        return
    status = "ok" if data.get("ok") else "failed"
    print(f"{status}: {data.get('selected_route') or data.get('case_dir') or data.get('manifest', '')}")
    for error in data.get("errors", []):
        print(f"error: {error}")
    for warning in data.get("warnings", []):
        print(f"warning: {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="ResearchLoop visual-to-editable router")
    sub = parser.add_subparsers(dest="command", required=True)

    classify_parser = sub.add_parser("classify")
    classify_parser.add_argument("--request", required=True)
    classify_parser.add_argument("--json", action="store_true")

    manifest_parser = sub.add_parser("validate-manifest")
    manifest_parser.add_argument("--manifest", required=True)
    manifest_parser.add_argument("--json", action="store_true")

    case_parser = sub.add_parser("validate-case")
    case_parser.add_argument("--case-dir", required=True)
    case_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command == "classify":
        result = classify_request(read_yaml_document(Path(args.request)))
        print_result(result, args.json)
        return 0 if result.get("ok") else 1
    if args.command == "validate-manifest":
        result = validate_manifest_file(Path(args.manifest))
        print_result(result, args.json)
        return 0 if result.get("ok") else 1
    if args.command == "validate-case":
        result = validate_case_dir(Path(args.case_dir))
        print_result(result, args.json)
        return 0 if result.get("ok") else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
