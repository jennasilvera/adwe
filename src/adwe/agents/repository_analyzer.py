import tempfile
from collections import Counter
from pathlib import Path

from git import Repo

from adwe.workflows.state import WorkflowState

IGNORED_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache", "dist", "build"}

LANGUAGE_BY_EXT = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".rb": "Ruby",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".md": "Markdown",
}


def analyze_repository(state: WorkflowState):
    repository_url = state["repository_url"]

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "repo"
        Repo.clone_from(repository_url, repo_path)

        files = [
            path
            for path in repo_path.rglob("*")
            if path.is_file()
            and not any(part in IGNORED_DIRS for part in path.parts)
        ]

        relative_files = [str(path.relative_to(repo_path)) for path in files]

        languages = Counter(
            LANGUAGE_BY_EXT.get(path.suffix, "Other")
            for path in files
        )

        detected_tools = {
            "docker": any(path.name in {"Dockerfile", "docker-compose.yml"} for path in files),
            "python_project": any(path.name == "pyproject.toml" for path in files),
            "github_actions": any(".github/workflows" in str(path.relative_to(repo_path)) for path in files),
            "alembic": any("migrations" in path.parts for path in files),
        }

    return {
        "repository_analysis": {
            "repository_url": repository_url,
            "file_count": len(relative_files),
            "languages": dict(languages),
            "detected_tools": detected_tools,
            "sample_files": relative_files[:30],
        }
    }
