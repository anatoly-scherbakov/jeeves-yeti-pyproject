from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class Reason(StrEnum):
    """Represents the reason for a GitHub notification."""

    review_requested = 'review_requested'
    mention = 'mention'
    assign = 'assign'
    author = 'author'
    comment = 'comment'
    ci_activity = 'ci_activity'
    manual = 'manual'
    state_change = 'state_change'
    subscribed = 'subscribed'
    team_mention = 'team_mention'


class SubjectType(StrEnum):
    """Represents the type of the subject for a GitHub notification."""

    pull_request = 'PullRequest'
    issue = 'Issue'
    release = 'Release'


class RepositoryOwnerType(StrEnum):
    """Represents the type of the owner of a GitHub repository."""

    user = 'User'
    organization = 'Organization'


class Subject(BaseModel):   # type: ignore
    """Subject of a GitHub notification: PR, Issue, or Release."""

    title: str
    url: str
    latest_comment_url: str | None = None
    type: SubjectType


class RepositoryOwner(BaseModel):   # type: ignore
    """Owner of a GitHub repository, a user or an organization."""

    login: str
    id: int
    node_id: str
    avatar_url: str
    url: str
    html_url: str
    type: RepositoryOwnerType
    site_admin: bool


class Repository(BaseModel):   # type: ignore
    """Represents a GitHub repository involved in a notification."""

    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: RepositoryOwner
    html_url: str
    description: str | None = None
    fork: bool
    url: str


class Notification(BaseModel):   # type: ignore
    """GitHub notification."""

    id: str
    unread: bool
    reason: Reason
    updated_at: datetime
    last_read_at: datetime | None = None
    subject: Subject
    repository: Repository
    url: str
    subscription_url: str


class ViewPullRequest(BaseModel):   # type: ignore
    """Result of viewing the details of a PR."""

    closed: bool
