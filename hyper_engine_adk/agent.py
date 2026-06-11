"""ADK-native smoke-cycle agent skeleton."""

from google.adk.agents import LlmAgent

from hyper_adk.config import load_config
from hyper_engine_adk.prompt import SMOKE_AGENT_PROMPT
from hyper_engine_adk.tools import (
    describe_smoke_engine_status,
    inspect_smoke_engine_run,
    list_smoke_datasets,
    list_smoke_engine_runs,
    run_smoke_self_learning_cycle,
)


root_agent = LlmAgent(
    name="hyperagents_smoke_cycle",
    model=load_config().model,
    description="ADK-native smoke-cycle agent for synthetic factor-research checks.",
    instruction=SMOKE_AGENT_PROMPT,
    tools=[
        describe_smoke_engine_status,
        list_smoke_datasets,
        run_smoke_self_learning_cycle,
        list_smoke_engine_runs,
        inspect_smoke_engine_run,
    ],
)
