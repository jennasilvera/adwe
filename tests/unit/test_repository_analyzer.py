from pathlib import Path

from adwe.agents.repository_analyzer import _is_ignored, _relative


def test_repository_analyzer_ignores_generated_directories():
    assert _is_ignored(Path("repo/.git/config"))
    assert _is_ignored(Path("repo/__pycache__/module.pyc"))
    assert _is_ignored(Path("repo/node_modules/package/index.js"))


def test_repository_analyzer_relative_path():
    repo_path = Path("/tmp/repo")
    file_path = repo_path / "src" / "adwe" / "api" / "app.py"

    assert _relative(file_path, repo_path) == "src/adwe/api/app.py"
