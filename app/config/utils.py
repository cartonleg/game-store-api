from pathlib import Path


def resolve_env_files() -> str | None:
    env_file = str(Path(__file__).resolve().parents[2] / ".env")

    if Path(env_file).exists():
        return env_file
    return None
