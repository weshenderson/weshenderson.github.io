"""
Source the Alea config file and make available
to all modules as 'config'.
"""

import yaml

CONFIG_FILE = ".alea.yaml"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
