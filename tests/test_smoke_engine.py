from hyper_adk.tools import (
    inspect_smoke_engine_run,
    list_smoke_datasets,
    list_smoke_engine_runs,
    run_smoke_self_learning_cycle,
)
from hyper_engine.evaluator import CrossSectionalSmokeEvaluator, EvaluationConfig
from hyper_engine.factor_templates import TEMPLATES, list_factor_templates, run_template
from hyper_engine.runner import inspect_smoke_run, list_smoke_runs, run_smoke_cycle
from hyper_engine.smoke_data import load_panel


def test_factor_templates_are_whitelisted_and_runnable():
    panel = load_panel("sp500_smoke", "val")
    evaluator = CrossSectionalSmokeEvaluator(
        EvaluationConfig(dataset="sp500_smoke", split="val")
    )

    assert len(list_factor_templates()) == 4
    for template_id in TEMPLATES:
        signals = run_template(template_id, panel)
        assert set(signals.columns) == {"date", "symbol", "signal"}
        assert len(signals) == len(panel)
        metrics = evaluator.evaluate_signals(signals)
        assert metrics["can_run"] == 1.0
        assert metrics["n_valid_days"] >= 20


def test_smoke_cycle_writes_manifest(tmp_path):
    result = run_smoke_cycle(
        dataset="sp500_smoke",
        split="val",
        run_id="test_smoke_run",
        artifact_root=tmp_path,
    )

    assert result["status"] == "completed"
    assert result["execution_mode"]["arbitrary_generated_code_executed"] is False
    assert result["execution_mode"]["docker_launched"] is False
    assert result["task_agent_step"]["candidate_count"] == 4
    assert result["best_candidate"]["template_id"] in TEMPLATES

    listed = list_smoke_runs(tmp_path)
    assert listed["count"] == 1
    inspected = inspect_smoke_run("test_smoke_run", tmp_path)
    assert inspected["run_id"] == "test_smoke_run"


def test_adk_smoke_tools_use_default_artifact_root(monkeypatch, tmp_path):
    monkeypatch.setenv("HYPER_ADK_ARTIFACT_ROOT", str(tmp_path))

    datasets = list_smoke_datasets()
    assert datasets["count"] == 2

    result = run_smoke_self_learning_cycle(dataset="csi300_smoke", split="val")
    assert result["dataset"] == "csi300_smoke"
    assert result["best_candidate"]["template_id"] in TEMPLATES

    runs = list_smoke_engine_runs()
    assert runs["count"] == 1
    inspected = inspect_smoke_engine_run(result["run_id"])
    assert inspected["run_id"] == result["run_id"]
