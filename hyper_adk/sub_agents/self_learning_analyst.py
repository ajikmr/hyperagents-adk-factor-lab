"""Self-learning workflow specialist subagent."""

from google.adk.agents import LlmAgent

from hyper_adk.config import load_config


self_learning_analyst_agent = LlmAgent(
    name="hyper_self_learning_analyst",
    model=load_config().model,
    description="Explains archive search, parent selection, and meta-agent changes.",
    instruction=(
        "You explain self-learning agent mechanics such as archive search, "
        "parent selection, UCB exploration, task-agent prompt changes, and "
        "evaluation gaming risks. Emphasize that noisy validation gains may not "
        "survive held-out testing."
    ),
)
