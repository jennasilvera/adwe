import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from adwe.services.repository_clone import clone_repository


@contextmanager
def repository_workspace(repository_url: str) -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / "repo"
        clone_repository(repository_url, repo_path)
        yield repo_path
