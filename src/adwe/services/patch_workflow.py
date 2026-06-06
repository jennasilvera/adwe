import tempfile
from pathlib import Path

from adwe.services.git_branch import create_branch
from adwe.services.git_commit import commit_changes
from adwe.services.patch_apply import apply_patch
from adwe.services.repository_clone import clone_repository


def apply_patch_workflow(
    repository_url: str,
    branch_name: str,
    diff: str,
    commit_message: str,
) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "repo"

        clone_repository(repository_url, repo_path)
        create_branch(repo_path, branch_name)
        apply_patch(repo_path, diff)
        commit_sha = commit_changes(repo_path, commit_message)

        return {
            "branch_name": branch_name,
            "commit_sha": commit_sha,
            "status": "committed",
        }
