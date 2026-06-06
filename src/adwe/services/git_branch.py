import subprocess
from pathlib import Path


class GitBranchError(Exception):
    pass


def create_branch(repo_path: Path, branch_name: str) -> None:
    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise GitBranchError(result.stderr)
