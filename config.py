import json
from pathlib import Path

CONFIG_PATH = Path("block.json")

def load_block_list():
    if not CONFIG_PATH.exists():
        return []
    try:
        with open(CONFIG_PATH, "r") as f:
            return [x.lower() for x in json.load(f)]
    except json.JSONDecodeError:
        return []

def save_block_list(apps):
    with open(CONFIG_PATH, "w") as f:
        json.dump(apps, f, indent=2)