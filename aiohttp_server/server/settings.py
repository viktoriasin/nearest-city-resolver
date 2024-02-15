import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
PACKAGE_NAME = 'server'


def load_config(conf_path):
    with open(BASE_DIR / "config" / conf_path, 'r') as f:
        conf = yaml.safe_load(f)
    return conf
