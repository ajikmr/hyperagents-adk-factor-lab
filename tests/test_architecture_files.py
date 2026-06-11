from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_task_and_meta_agent_files_exist():
    task_agent = PROJECT_ROOT / "hyper_adk" / "sub_agents" / "task_agent.py"
    meta_agent = PROJECT_ROOT / "hyper_adk" / "sub_agents" / "meta_agent.py"

    assert task_agent.exists()
    assert meta_agent.exists()


def test_root_prompt_names_task_and_meta_agents():
    prompt_path = PROJECT_ROOT / "hyper_adk" / "prompt.py"
    prompt = prompt_path.read_text(encoding="utf-8")

    assert "task agent" in prompt
    assert "meta agent" in prompt
