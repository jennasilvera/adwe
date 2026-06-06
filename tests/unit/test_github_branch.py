import subprocess

from adwe.services.github_branch import branch_exists, create_branch, delete_branch


def test_create_and_delete_branch(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "adwe@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "ADWE Bot"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    readme.write_text("hello\n")

    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, check=True)

    create_branch(str(tmp_path), "adwe/test-branch")

    assert branch_exists(str(tmp_path), "adwe/test-branch") is True

    subprocess.run(["git", "checkout", "master"], cwd=tmp_path, check=True)

    delete_branch(str(tmp_path), "adwe/test-branch")

    assert branch_exists(str(tmp_path), "adwe/test-branch") is False
