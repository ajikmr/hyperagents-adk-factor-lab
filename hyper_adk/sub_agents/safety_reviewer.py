"""Finance-safety specialist subagent."""

from google.adk.agents import LlmAgent

from hyper_adk.config import load_config


safety_reviewer_agent = LlmAgent(
    name="hyper_safety_reviewer",
    model=load_config().model,
    description="Reviews outputs for finance-safety and overclaiming risks.",
    instruction=(
        "You enforce the project's safety boundaries. Do not allow buy/sell/hold "
        "recommendations, do not overstate validation results, and require clear "
        "distinctions between synthetic smoke data, validation evidence, and "
        "held-out test evidence."
    ),
)
