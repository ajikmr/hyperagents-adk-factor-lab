"""Root ADK agent for HyperAgents-ADK Self-Learning Factor Lab."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from hyper_adk.config import load_config
from hyper_adk.prompt import ROOT_PROMPT
from hyper_adk.sub_agents.evaluation_analyst import evaluation_analyst_agent
from hyper_adk.sub_agents.factor_researcher import factor_researcher_agent
from hyper_adk.sub_agents.meta_agent import meta_agent
from hyper_adk.sub_agents.safety_reviewer import safety_reviewer_agent
from hyper_adk.sub_agents.self_learning_analyst import self_learning_analyst_agent
from hyper_adk.sub_agents.task_agent import task_agent
from hyper_adk.tools import (
    compare_conditions,
    explain_task_meta_roles,
    finance_safety_check,
    get_study_summary,
    inspect_learning_patch,
    inspect_smoke_engine_run,
    list_available_studies,
    list_learning_patch_examples,
    list_smoke_datasets,
    list_smoke_engine_runs,
    run_smoke_self_learning_cycle,
)

MODEL = load_config().model

root_agent = LlmAgent(
    name="hyperagents_adk_factor_lab",
    model=MODEL,
    description=(
        "Research assistant for inspecting self-learning financial factor "
        "experiments, smoke-test evidence, and safety caveats."
    ),
    instruction=ROOT_PROMPT,
    tools=[
        list_available_studies,
        get_study_summary,
        compare_conditions,
        list_learning_patch_examples,
        inspect_learning_patch,
        explain_task_meta_roles,
        finance_safety_check,
        list_smoke_datasets,
        run_smoke_self_learning_cycle,
        list_smoke_engine_runs,
        inspect_smoke_engine_run,
        AgentTool(agent=task_agent),
        AgentTool(agent=meta_agent),
        AgentTool(agent=factor_researcher_agent),
        AgentTool(agent=evaluation_analyst_agent),
        AgentTool(agent=self_learning_analyst_agent),
        AgentTool(agent=safety_reviewer_agent),
    ],
)
