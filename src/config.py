from pathlib import Path

# Global project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_path(relative_path: str) -> str:
    """
    Append the relative path to the project root and return a string path.

    :param relative_path: Path relative to the project root.
    :return: Full string path to the file.
    """
    return str(PROJECT_ROOT / relative_path)
