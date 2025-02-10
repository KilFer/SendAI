import yaml

def load_config():
    """Load configuration from a YAML file."""
    with open("../config/config.yaml", "r") as file:
        return yaml.safe_load(file)

CONFIG = load_config()  # Global config dictionary