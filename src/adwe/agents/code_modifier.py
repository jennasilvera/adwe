from adwe.workflows.state import WorkflowState


def _new_file_patch(path: str, content: str) -> str:
    lines = content.splitlines()
    added_lines = "".join(f"+{line}\n" for line in lines)

    return (
        f"diff --git a/{path} b/{path}\n"
        "new file mode 100644\n"
        "index 0000000..d4f3c2a\n"
        "--- /dev/null\n"
        f"+++ b/{path}\n"
        f"@@ -0,0 +1,{len(lines)} @@\n"
        f"{added_lines}"
    )


def _select_patch_target(analysis: dict, plan: dict) -> tuple[str, str]:
    tools = analysis.get("detected_tools", {})
    steps = plan.get("recommended_next_steps", [])

    if tools.get("alembic") and any("migration validation" in step.lower() for step in steps):
        return "docs/adwe-migration-validation.md", "Generated migration validation documentation."

    if tools.get("docker") and any("health checks" in step.lower() for step in steps):
        return "docs/adwe-docker-healthchecks.md", "Generated Docker Compose health check recommendations."

    if tools.get("fastapi") and analysis.get("api_routes"):
        return "docs/adwe-api-surface.md", "Generated API surface analysis documentation."

    return "ADWE_ANALYSIS.md", "Generated repository-specific ADWE analysis artifact."


def _analysis_markdown(analysis: dict, plan: dict, target_file: str) -> str:
    tools = analysis.get("detected_tools", {})
    architecture = plan.get("architecture", {})
    strengths = plan.get("strengths", [])
    risks = plan.get("risks", [])
    steps = plan.get("recommended_next_steps", [])

    lines = [
        "# ADWE Generated Artifact",
        "",
        f"Target file: `{target_file}`",
        "",
        "This file was generated from repository analysis and implementation planning.",
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


def modify_code(state: WorkflowState):
    analysis = state["repository_analysis"]
    plan = state["implementation_plan"]

    target_file, summary = _select_patch_target(analysis, plan)
    content = _analysis_markdown(analysis, plan, target_file)
    patch = _new_file_patch(target_file, content)

    return {
        "code_modification": {
            "status": "proposed",
            "summary": summary,
            "patch": patch,
            "target_file": target_file,
            "based_on": {
                "file_count": analysis.get("file_count"),
                "detected_tools": analysis.get("detected_tools", {}),
                "recommended_steps": plan.get("recommended_next_steps", []),
            },
        }
    }
