import tempfile
from pathlib import Path

from git import Repo

from adwe.workflows.state import WorkflowState

IGNORED_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache"}


def analyze_repository(state: WorkflowState):
    repository_url = state["repository_url"]

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "repo"
        Repo.clone_from(repository_url, repo_path)

        files = [
            str(path.relative_to(repo_path))
            for path in repo_path.rglob("*")
            if path.is_file()
            and not any(part in IGNORED_DIRS for part in path.parts)
        ]

    return {
        "repository_analysis": {
            "repository_url": repository_url,
            "file_count": len(files),
            "sample_files": files[:25],
        }
    }
