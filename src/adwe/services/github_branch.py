from git import Repo


def create_branch(repo_path: str, branch_name: str) -> str:
    repo = Repo(repo_path)

    if branch_name in repo.heads:
        return branch_name

    repo.git.checkout("-b", branch_name)
    return branch_name


def branch_exists(repo_path: str, branch_name: str) -> bool:
    repo = Repo(repo_path)
    return branch_name in [head.name for head in repo.heads]


def delete_branch(repo_path: str, branch_name: str) -> None:
    repo = Repo(repo_path)

    if branch_name in [head.name for head in repo.heads]:
        repo.git.branch("-D", branch_name)
