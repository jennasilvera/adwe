import subprocess

from adwe.services.git_commit import commit_changes


def test_commit_changes(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    readme.write_text("hello\n")

    sha = commit_changes(tmp_path, "initial commit")

    assert len(sha) == 40
