# src/utils/path_config.py

import os

# Global project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_path(relative_path: str) -> str:
    """
    Append the relative path to the project root and return a string path.

    :param relative_path: Path relative to the project root.
    :return: Full string path to the file.
    """
    return os.path.join(PROJECT_ROOT, relative_path)
