"""Version information."""

from pathlib import Path

import tomli


def get_version() -> str:
    """Get version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    return pyproject["project"]["version"]


__version__ = get_version()
