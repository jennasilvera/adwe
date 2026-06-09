from pathlib import Path

from git import Repo

from adwe.core.config import settings
from adwe.services.errors import RepositoryCloneError


def build_clone_url(repository_url: str) -> str:
    if settings.github_token and repository_url.startswith("https://github.com/"):
        return repository_url.replace(
            "https://github.com/",
            f"https://x-access-token:{settings.github_token}@github.com/",
            1,
        )

    return repository_url


def clone_repository(repository_url: str, destination: Path) -> Path:
    try:
        clone_url = build_clone_url(repository_url)
        Repo.clone_from(clone_url, destination)
        return destination
    except Exception as exc:
        raise RepositoryCloneError(str(exc)) from exc
