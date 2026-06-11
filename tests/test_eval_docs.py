import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = PROJECT_ROOT / "eval"


def test_eval_configs_are_valid_json_and_have_rubrics():
    config_paths = sorted(EVAL_ROOT.glob("*_eval_config.json")) + [
        EVAL_ROOT / "eval_config.json"
    ]
    assert len(config_paths) >= 5

    for path in config_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        criteria = payload["criteria"]["rubric_based_final_response_quality_v1"]
        assert criteria["threshold"] >= 0.8
        assert criteria["judge_model_options"]["judge_model"] == "gemini-3.5-flash"
        assert criteria["rubrics"]


def test_eval_data_files_are_valid_adk_shape():
    data_paths = sorted((EVAL_ROOT / "data").glob("*.test.json"))
    assert {path.name for path in data_paths} == {
        "hyper_adk_mcp.test.json",
        "hyper_adk_research.test.json",
        "hyper_adk_safety.test.json",
        "hyper_adk_smoke.test.json",
    }

    for path in data_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["eval_set_id"].startswith("hyperagents-adk")
        assert payload["eval_cases"]
        for case in payload["eval_cases"]:
            assert case["eval_id"]
            assert case["session_input"]["app_name"] in {
                "hyper_adk",
                "hyper_engine_adk",
                "hyper_adk_mcp",
            }
            turn = case["conversation"][0]
            assert turn["user_content"]["parts"][0]["text"]
            assert turn["final_response"]["parts"][0]["text"]


def test_architecture_docs_reference_key_components():
    architecture = (PROJECT_ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
    demo = (PROJECT_ROOT / "DEMO_SCRIPT.md").read_text(encoding="utf-8")

    for text in (architecture, demo):
        assert "hyper_task_agent" in text or "task agent" in text
        assert "hyper_meta_agent" in text or "meta agent" in text
        assert "Docker" in text
        assert "arbitrary generated" in text
        assert "MCP" in text


def test_mermaid_sources_exist():
    assets = PROJECT_ROOT / "assets"
    assert (assets / "architecture.mmd").exists()
    assert (assets / "native_adk_flow.mmd").exists()
    assert (assets / "mcp_flow.mmd").exists()


def test_rendered_architecture_pngs_exist():
    assets = PROJECT_ROOT / "assets"
    assert (assets / "architecture.png").exists()
    assert (assets / "native_adk_flow.png").exists()
    assert (assets / "mcp_flow.png").exists()
