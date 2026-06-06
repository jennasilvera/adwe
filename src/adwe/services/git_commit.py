import subprocess
from pathlib import Path


class GitCommitError(Exception):
    pass


def commit_changes(repo_path: Path, message: str) -> str:
    subprocess.run(
        ["git", "config", "user.email", "adwe@example.com"],
        cwd=repo_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "ADWE Bot"],
        cwd=repo_path,
        check=True,
    )

    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise GitCommitError(result.stderr)

    sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path,
        text=True,
    ).strip()

    return sha
