from langgraph.graph import END, StateGraph

from adwe.agents.code_modifier import modify_code
from adwe.agents.planner import create_plan
from adwe.agents.repository_analyzer import analyze_repository
from adwe.workflows.state import WorkflowState

builder = StateGraph(WorkflowState)

builder.add_node("repository_analysis", analyze_repository)
builder.add_node("planning", create_plan)
builder.add_node("code_modification", modify_code)

builder.set_entry_point("repository_analysis")

builder.add_edge("repository_analysis", "planning")
builder.add_edge("planning", "code_modification")
builder.add_edge("code_modification", END)

workflow_graph = builder.compile()
