from adwe.workflows.state import WorkflowState


def _analysis_markdown(analysis: dict, plan: dict) -> str:
    tools = analysis.get("detected_tools", {})
    architecture = plan.get("architecture", {})
    strengths = plan.get("strengths", [])
    risks = plan.get("risks", [])
    steps = plan.get("recommended_next_steps", [])

    lines = [
        "# ADWE Analysis",
        "",
        "This repository was analyzed by ADWE.",
        "",
        "## Repository Summary",
        "",
        f"- Files analyzed: {analysis.get('file_count', 0)}",
        f"- API routes detected: {architecture.get('api_route_count', 0)}",
        f"- Database models detected: {architecture.get('database_model_count', 0)}",
        f"- Migrations detected: {architecture.get('migration_count', 0)}",
        f"- Tests detected: {architecture.get('test_count', 0)}",
        "",
        "## Detected Tooling",
        "",
    ]

    for name, detected in sorted(tools.items()):
        status = "yes" if detected else "no"
        lines.append(f"- {name}: {status}")

    if strengths:
        lines.extend(["", "## Strengths", ""])
        lines.extend(f"- {item}" for item in strengths)

    if risks:
        lines.extend(["", "## Risks", ""])
        lines.extend(f"- {item}" for item in risks)

    if steps:
        lines.extend(["", "## Recommended Next Steps", ""])
        lines.extend(f"- {item}" for item in steps)

    lines.extend(["", "Generated as part of an agentic development workflow."])

    return "\n".join(lines) + "\n"


def _new_file_patch(path: str, content: str) -> str:
    added_lines = "".join(f"+{line}\n" for line in content.splitlines())

    return (
        f"diff --git a/{path} b/{path}\n"
        "new file mode 100644\n"
        "index 0000000..d4f3c2a\n"
        "--- /dev/null\n"
        f"+++ b/{path}\n"
        f"@@ -0,0 +1,{len(content.splitlines())} @@\n"
        f"{added_lines}"
    )


def modify_code(state: WorkflowState):
    analysis = state["repository_analysis"]
    plan = state["implementation_plan"]

    content = _analysis_markdown(analysis, plan)
    patch = _new_file_patch("ADWE_ANALYSIS.md", content)

    return {
        "code_modification": {
            "status": "proposed",
            "summary": "Generated a repository-specific ADWE analysis artifact.",
            "patch": patch,
            "target_file": "ADWE_ANALYSIS.md",
            "based_on": {
                "file_count": analysis.get("file_count"),
                "detected_tools": analysis.get("detected_tools", {}),
                "recommended_steps": plan.get("recommended_next_steps", []),
            },
        }
    }
