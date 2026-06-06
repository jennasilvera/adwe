import subprocess
from pathlib import Path


class GitPushError(Exception):
    pass


def push_branch(repo_path: Path, branch_name: str) -> None:
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise GitPushError(result.stderr)
