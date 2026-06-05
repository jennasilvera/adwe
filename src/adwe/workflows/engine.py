from langgraph.graph import StateGraph
from langgraph.graph import END

from adwe.workflows.state import WorkflowState
from adwe.agents.repository_analyzer import analyze_repository
from adwe.agents.planner import create_plan


builder = StateGraph(WorkflowState)

builder.add_node(
    "repository_analysis",
    analyze_repository,
)

builder.add_node(
    "planning",
    create_plan,
)

builder.set_entry_point(
    "repository_analysis"
)

builder.add_edge(
    "repository_analysis",
    "planning",
)

builder.add_edge(
    "planning",
    END,
)

workflow_graph = builder.compile()
