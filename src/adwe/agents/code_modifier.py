from adwe.workflows.state import WorkflowState


def modify_code(state: WorkflowState):
    analysis = state["repository_analysis"]
    plan = state["implementation_plan"]

    patch = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1,3 +1,7 @@
+# Agentic Development Workflow Engine
+
+This repository was analyzed by ADWE.
+
"""

    return {
        "code_modification": {
            "status": "proposed",
            "summary": "Generated a safe README documentation patch.",
            "patch": patch,
            "based_on": {
                "file_count": analysis.get("file_count"),
                "recommended_steps": plan.get("recommended_next_steps", []),
            },
        }
    }
