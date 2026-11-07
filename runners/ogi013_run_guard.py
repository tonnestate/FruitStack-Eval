from pathlib import Path


def ensure_empty_output(path: Path) -> None:
    if path.exists() and (not path.is_dir() or next(path.iterdir(), None) is not None):
        raise FileExistsError(f"output directory must be empty: {path}")
