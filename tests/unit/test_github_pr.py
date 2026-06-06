from adwe.services.github_pr import create_pull_request, parse_github_repo


def test_parse_github_repo_https_url():
    owner, repo = parse_github_repo("https://github.com/pallets/flask")

    assert owner == "pallets"
    assert repo == "flask"


def test_parse_github_repo_git_suffix():
    owner, repo = parse_github_repo("https://github.com/pallets/flask.git")

    assert owner == "pallets"
    assert repo == "flask"


def test_create_pull_request_skips_without_token():
    result = create_pull_request(
        repository_url="https://github.com/pallets/flask",
        branch_name="adwe/test",
        title="Test PR",
        body="Test body",
    )

    assert result["status"] == "skipped"
    assert result["url"] is None
