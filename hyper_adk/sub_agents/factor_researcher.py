"""Factor-research specialist subagent."""

from google.adk.agents import LlmAgent

from hyper_adk.config import load_config


factor_researcher_agent = LlmAgent(
    name="hyper_factor_researcher",
    model=load_config().model,
    description="Explains factor templates and cross-sectional OHLCV signal ideas.",
    instruction=(
        "You explain cross-sectional factor research using OHLCV data, including "
        "momentum, reversal, range position, volume confirmation, and rank-based "
        "normalization. Keep outputs research-only and caveated."
    ),
)
