from adwe.workflows.state import WorkflowState


def modify_code(state: WorkflowState):
    analysis = state["repository_analysis"]

    diff = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1,3 +1,7 @@
+# Agentic Development Workflow Engine
+
+This repository is analyzed by ADWE.
+
"""

    return {
        "code_modification": {
            "status": "proposed",
            "summary": "Generated safe README patch proposal.",
            "proposed_changes": [
                "Add project title to README.",
                "Add short ADWE-generated repository note.",
            ],
            "diff": diff,
            "based_on_file_count": analysis.get("file_count"),
        }
    }
