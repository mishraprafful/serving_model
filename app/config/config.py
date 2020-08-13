from pathlib import Path
from os.path import join


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


# flask realted config variables
THEME = "default"
DEBUG = "True"

# model related config variables
MODEL_DIR = join(get_project_root(), "model")
