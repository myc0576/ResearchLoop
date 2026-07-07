from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).absolute().parents[1] / "scripts"))

import visual_to_editable_router as router


ROOT = Path(__file__).absolute().parents[1]
EXAMPLE = ROOT / "examples" / "visual_to_editable_minimal"


def make_request(input_type: str, signals: list[str], outputs: list[str]) -> dict[str, object]:
    return {
        "schema": "researchloop.visual_to_editable_request.v1",
        "source": {
            "reference": "local_only:test",
            "input_type": input_type,
            "sensitivity": "sanitized_example",
            "commit_allowed": False,
        },
        "visual_signals": signals,
        "target_outputs": outputs,
    }


@pytest.mark.parametrize(
    ("input_type", "signals", "outputs", "expected"),
    [
        ("slide_screenshot", ["slide", "text_heavy"], ["pptx"], "ppt_screenshot_reconstruction"),
        ("pdf_page", ["slide", "title"], ["pptx"], "ppt_screenshot_reconstruction"),
        ("image_based_pptx", ["slide", "card_layout"], ["pptx"], "ppt_screenshot_reconstruction"),
        ("scientific_figure", ["axis", "colorbar"], ["svg"], "scientific_figure_tracing"),
        ("chart", ["axis", "legend", "data_series"], ["native_chart"], "native_chart_rebuild"),
        ("table_screenshot", ["rows", "columns", "grid"], ["csv"], "editable_table_rebuild"),
        ("flowchart", ["arrow", "node", "process_flow"], ["mermaid"], "flowchart_to_mermaid_svg"),
        ("formula_screenshot", ["equation", "latex", "greek_symbols"], ["latex"], "formula_to_latex_ppt"),
        ("ui_screenshot", ["button", "navbar", "component"], ["html"], "ui_to_html_figma_ppt"),
    ],
)
def test_deterministic_route_selection(input_type: str, signals: list[str], outputs: list[str], expected: str) -> None:
    result = router.classify_request(make_request(input_type, signals, outputs))
    assert result["ok"] is True
    assert result["selected_route"] == expected


def test_ambiguous_input_falls_back_to_manual_review() -> None:
    result = router.classify_request(make_request("unknown", [], ["editable_asset"]))
    assert result["ok"] is True
    assert result["selected_route"] == "manual_review"
    assert result["confidence"] == "manual_review"


def test_minimal_example_case_validates() -> None:
    result = router.validate_case_dir(EXAMPLE)
    assert result["ok"] is True
    assert result["classification"]["selected_route"] == "flowchart_to_mermaid_svg"


def test_manifest_rejects_forbidden_committed_source() -> None:
    data = router.read_yaml_document(EXAMPLE / "visual_reconstruction_manifest.yaml")
    data = copy.deepcopy(data)
    data["source_policy"]["committed_source_paths"] = ["source.png"]
    result = router.validate_manifest_data(data, EXAMPLE)
    assert result["ok"] is False
    assert "forbidden_committed_source:source.png" in result["errors"]
    assert "commit_disallowed_but_committed_source_paths_present" in result["errors"]


def test_manifest_rejects_unsafe_validated_status() -> None:
    data = router.read_yaml_document(EXAMPLE / "visual_reconstruction_manifest.yaml")
    data = copy.deepcopy(data)
    data["status"] = "validated"
    data["human_approved"] = False
    result = router.validate_manifest_data(data, EXAMPLE)
    assert result["ok"] is False
    assert "unsafe_validated_without_human_approval" in result["errors"]


def test_case_reports_missing_qa_and_reproduction(tmp_path: Path) -> None:
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    (case_dir / "request.yaml").write_text((EXAMPLE / "request.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    (case_dir / "visual_reconstruction_manifest.yaml").write_text(
        (EXAMPLE / "visual_reconstruction_manifest.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (case_dir / "visual_reconstruction_prompt.md").write_text("prompt", encoding="utf-8")
    (case_dir / "figure_card.md").write_text("figure", encoding="utf-8")

    result = router.validate_case_dir(case_dir)
    assert result["ok"] is False
    assert "missing_case_file:visual_reconstruction_qa.md" in result["errors"]
    assert "missing_case_file:reproduction_entry.md" in result["errors"]
