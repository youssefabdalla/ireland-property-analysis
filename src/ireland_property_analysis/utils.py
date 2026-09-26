from pathlib import Path


def get_root_dir() -> Path:
    """
    Get the root directory of the project by searching for a 'pyproject.toml' file.
    Returns:
        Path: The root directory of the project.
    """
    start_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd().resolve()
    ROOT_DIR = next(
        (parent for parent in (start_dir, *start_dir.parents) if (parent / "pyproject.toml").is_file()),
        None,
    )
    if ROOT_DIR is None:
        raise FileNotFoundError(f"Could not find project root from {start_dir}")
    return ROOT_DIR

def get_file_encoding(path:str) -> str:
    """
    Get the file encoding used in the project.
    Returns:
        str: The file encoding used in the project.
    """
    from charset_normalizer import from_path

    match = from_path(path).best()
    return match.encoding
