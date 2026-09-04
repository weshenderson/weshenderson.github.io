"""
Source the Alea config file and make available
to all modules as 'config'.
"""

from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = REPO_ROOT / ".alea.yaml"

def resolve_path(path):
    """Resolve a configured path relative to the repository root."""
    if not path:
        return path

    return REPO_ROOT / path

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
