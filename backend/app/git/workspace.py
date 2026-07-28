from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

WORKSPACE_DIR = BASE_DIR / "workspace"

WORKSPACE_DIR.mkdir(exist_ok=True)


def repository_workspace(
    project_id: str,
    repository_id: str,
) -> Path:
    return WORKSPACE_DIR / project_id / repository_id