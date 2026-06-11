"""Evaluation specialist subagent."""

from google.adk.agents import LlmAgent

from hyper_adk.config import load_config


evaluation_analyst_agent = LlmAgent(
    name="hyper_evaluation_analyst",
    model=load_config().model,
    description="Explains financial signal metrics, validation splits, and held-out tests.",
    instruction=(
        "You explain Rank IC, ICIR, Sharpe, drawdown, validation-selected "
        "evidence, and held-out test evidence. Be precise, caveated, and never "
        "translate research metrics into investment recommendations."
    ),
)
