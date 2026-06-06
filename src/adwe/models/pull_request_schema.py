from pydantic import BaseModel


class PullRequestCreate(BaseModel):
    repository_url: str
    branch_name: str
    title: str
    body: str


class PullRequestRead(BaseModel):
    repository_url: str
    branch_name: str
    title: str
    body: str
    status: str
    url: str | None = None
