from pathlib import Path
from os.path import join


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


# flask realted config variables
ENVIRONMENT = "production"
FLASK_ENV = "production"
THEME = "default"
DEBUG = "False"

# model related config variables
MODEL_DIR = join(get_project_root(), "model")
