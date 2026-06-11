from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cloud_run_deployment_files_exist():
    assert (PROJECT_ROOT / "Dockerfile").exists()
    assert (PROJECT_ROOT / ".dockerignore").exists()
    assert (PROJECT_ROOT / "scripts" / "launch_adk_web_demo.sh").exists()
    assert (PROJECT_ROOT / "scripts" / "start_adk_web_cloud_run.sh").exists()
    assert (PROJECT_ROOT / "scripts" / "deploy_cloud_run_adk_web.sh").exists()


def test_dockerfile_uses_safe_public_defaults():
    dockerfile = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "HYPER_ADK_ENABLE_LIVE_RUNS=false" in dockerfile
    assert "HYPER_ADK_ENABLE_GENERATED_CODE=false" in dockerfile
    assert "GOOGLE_CLOUD_LOCATION=global" in dockerfile
    assert "CMD [\"bash\", \"scripts/start_adk_web_cloud_run.sh\"]" in dockerfile


def test_cloud_run_deploy_script_sets_safe_env():
    deploy_script = (PROJECT_ROOT / "scripts" / "deploy_cloud_run_adk_web.sh").read_text(
        encoding="utf-8"
    )

    assert "HYPER_ADK_DEPLOY_REGION" in deploy_script
    assert "hyperagents-adk-factor-lab" in deploy_script
    assert "--allow-unauthenticated" in deploy_script
    assert "HYPER_ADK_ENABLE_LIVE_RUNS=false" in deploy_script
    assert "HYPER_ADK_ENABLE_GENERATED_CODE=false" in deploy_script
    assert "GOOGLE_CLOUD_LOCATION=global" in deploy_script


def test_cloud_run_startup_script_runs_smoke_and_adk_web():
    startup_script = (PROJECT_ROOT / "scripts" / "start_adk_web_cloud_run.sh").read_text(
        encoding="utf-8"
    )

    assert "python -m hyper_engine.runner" in startup_script
    assert "cloud_run_startup_smoke" in startup_script
    assert "adk web ." in startup_script
    assert "--host 0.0.0.0" in startup_script
    assert "--session_service_uri" in startup_script
    assert "HYPER_ADK_ENABLE_GENERATED_CODE" in startup_script


def test_dockerignore_excludes_credentials_and_artifacts():
    dockerignore = (PROJECT_ROOT / ".dockerignore").read_text(encoding="utf-8")

    assert ".env" in dockerignore
    assert "artifacts/" in dockerignore
    assert "__pycache__/" in dockerignore
    assert "demo_video/" in dockerignore
