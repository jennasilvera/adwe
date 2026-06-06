from adwe.core.config import settings


class GitHubPRError(Exception):
    pass


def create_pull_request(
    repository_url: str,
    branch_name: str,
    title: str,
    body: str,
) -> dict:
    if not settings.github_token:
        return {
            "repository_url": repository_url,
            "branch_name": branch_name,
            "title": title,
            "body": body,
            "status": "skipped",
            "url": None,
        }

    # Real GitHub API integration will be added next.
    return {
        "repository_url": repository_url,
        "branch_name": branch_name,
        "title": title,
        "body": body,
        "status": "prepared",
        "url": None,
    }
