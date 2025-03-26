"""
Config loader for EfficientSpeech
"""

import yaml
from pathlib import Path

def load_preprocess_config():
    """Load and return preprocess configuration"""
    config_path = Path(__file__).parent / "preprocess.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Make the config available when importing the package
preprocess_config = load_preprocess_config()