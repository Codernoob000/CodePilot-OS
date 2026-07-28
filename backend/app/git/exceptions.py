class GitServiceError(Exception):
    """Base exception for Git operations."""


class CloneFailedError(GitServiceError):
    """Raised when cloning a repository fails."""


class RepositoryAlreadyExistsError(GitServiceError):
    """Raised when the repository already exists locally."""