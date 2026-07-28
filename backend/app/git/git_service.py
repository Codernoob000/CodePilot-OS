from pathlib import Path

from git import GitCommandError, Repo

from app.git.exceptions import (
    CloneFailedError,
    RepositoryAlreadyExistsError,
)


class GitService:
    """Service responsible for Git operations."""

    def clone_repository(
        self,
        remote_url: str,
        destination: Path,
    ) -> Repo:

        if destination.exists():
            raise RepositoryAlreadyExistsError(
                "Repository already cloned."
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            return Repo.clone_from(
                remote_url,
                destination,
            )

        except GitCommandError as exc:
            raise CloneFailedError(str(exc)) from exc

    def open_repository(
    self,
    repository_path: Path,
    ) -> Repo:
        """
        Open an existing local Git repository.
        """
        return Repo(repository_path)

    def get_status(
    self,
    repository_path: Path,
    ) -> dict:
        repo = self.open_repository(repository_path)

        return {
            "branch": repo.active_branch.name,
            "clean": not repo.is_dirty(untracked_files=True),
            "modified": repo.git.diff("--name-only").splitlines(),
            "untracked": repo.untracked_files,
            "staged": repo.git.diff(
                "--cached",
                "--name-only",
            ).splitlines(),
        }