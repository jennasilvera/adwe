import subprocess
from pathlib import Path


class PatchApplyError(Exception):
    pass


def apply_patch(repo_path: Path, diff: str) -> None:
    process = subprocess.run(
        ["git", "apply", "--check", "-"],
        input=diff,
        text=True,
        cwd=repo_path,
        capture_output=True,
    )

    if process.returncode != 0:
        raise PatchApplyError(process.stderr)

    process = subprocess.run(
        ["git", "apply", "-"],
        input=diff,
        text=True,
        cwd=repo_path,
        capture_output=True,
    )

    if process.returncode != 0:
        raise PatchApplyError(process.stderr)
