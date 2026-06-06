import subprocess

from adwe.services.git_branch import create_branch


def test_create_branch(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    readme.write_text("hello\n")

    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "adwe@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "ADWE Bot"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, check=True)

    create_branch(tmp_path, "adwe/test-branch")

    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=tmp_path,
        text=True,
    ).strip()

    assert branch == "adwe/test-branch"
