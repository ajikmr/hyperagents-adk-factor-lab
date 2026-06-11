from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DEMO_URL = "https://hyperagents-adk-factor-lab-597409326013.asia-south1.run.app/dev-ui/"


def test_submission_docs_exist():
    assert (PROJECT_ROOT / "SUBMISSION.md").exists()
    assert (PROJECT_ROOT / "DEVPOST_SUBMISSION_DRAFT.md").exists()
    assert (PROJECT_ROOT / "PRESENTATION_STRATEGY.md").exists()


def test_submission_doc_contains_track_and_safety_boundaries():
    text = (PROJECT_ROOT / "SUBMISSION.md").read_text(encoding="utf-8")

    assert "Track 1" in text
    assert "task agent" in text.lower()
    assert "meta agent" in text.lower()
    assert "HYPER_ADK_ENABLE_GENERATED_CODE=false" in text
    assert PUBLIC_DEMO_URL in text
    assert "not an autonomous trading bot" in text.lower()


def test_devpost_draft_contains_required_links_and_google_stack():
    text = (PROJECT_ROOT / "DEVPOST_SUBMISSION_DRAFT.md").read_text(encoding="utf-8")

    assert PUBLIC_DEMO_URL in text
    assert "Track 1" in text
    assert "Google Agent Development Kit" in text
    assert "Gemini" in text
    assert "Cloud Run" in text
    assert "MCP" in text
    assert "31 passed" in text


def test_presentation_strategy_contains_demo_safety_guidance():
    text = (PROJECT_ROOT / "PRESENTATION_STRATEGY.md").read_text(encoding="utf-8")

    assert PUBLIC_DEMO_URL in text
    assert "Do not call it a trading bot" in text
    assert "Which stocks should I buy" in text
    assert "assets/architecture.png" in text
    assert "Cloud Run demo works for all three agents" in text
