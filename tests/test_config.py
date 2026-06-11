from pathlib import Path

from hyper_adk.config import APP_ROOT, load_config


def test_load_config_defaults(monkeypatch):
    monkeypatch.delenv("HYPER_ADK_MODEL", raising=False)
    monkeypatch.delenv("HYPER_ADK_ENABLE_LIVE_RUNS", raising=False)
    monkeypatch.delenv("HYPER_ADK_ENABLE_GENERATED_CODE", raising=False)

    config = load_config(env_file=Path("/tmp/nonexistent-hyperagents-adk.env"))

    assert config.model == "gemini-3.5-flash"
    assert config.app_root == APP_ROOT
    assert config.default_dataset == "sp500_smoke"
    assert config.enable_live_runs is False
    assert config.enable_generated_code is False


def test_load_config_env_overrides(monkeypatch):
    monkeypatch.setenv("HYPER_ADK_MODEL", "gemini-test")
    monkeypatch.setenv("HYPER_ADK_ENABLE_LIVE_RUNS", "true")
    monkeypatch.setenv("HYPER_ADK_ENABLE_GENERATED_CODE", "yes")

    config = load_config(env_file=Path("/tmp/nonexistent-hyperagents-adk.env"))

    assert config.model == "gemini-test"
    assert config.enable_live_runs is True
    assert config.enable_generated_code is True
