from adwe.workflows.state import WorkflowState


def modify_code(state: WorkflowState):
    analysis = state["repository_analysis"]
    plan = state["implementation_plan"]

    patch = """diff --git a/ADWE_ANALYSIS.md b/ADWE_ANALYSIS.md
new file mode 100644
index 0000000..d4f3c2a
--- /dev/null
+++ b/ADWE_ANALYSIS.md
@@ -0,0 +1,5 @@
+# ADWE Analysis
+
+This repository was analyzed by ADWE.
+
+Generated as part of an agentic development workflow.
"""

    return {
        "code_modification": {
            "status": "proposed",
            "summary": "Generated a safe repository analysis documentation patch.",
            "patch": patch,
            "based_on": {
                "file_count": analysis.get("file_count"),
                "recommended_steps": plan.get("recommended_next_steps", []),
            },
        }
    }
