import os
import subprocess
from pathlib import Path


def run_tests(repo_path: Path, command: list[str]) -> dict:
    env = os.environ.copy()
    env.pop("GITHUB_TOKEN", None)

    process = subprocess.run(
        command,
        cwd=repo_path,
        env=env,
        capture_output=True,
        text=True,
    )

    return {
        "passed": process.returncode == 0,
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }
