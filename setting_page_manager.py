import os
import json

SETTING_FILE = "settings.json"

def load_setting() -> dict:
    """Load user setting or create default"""

    if os.path.exists(SETTING_FILE):
        with open(SETTING_FILE, "r") as f: #r = read
            return json.load(f)
    
    return {"download_path" : os.path.join(os.path.expanduser("~"), "Downloads")}

def save_setting(new_data : dict) -> None:
    """Update and save user settings safely"""

    settings = load_setting()
    settings.update(new_data)

    with open(SETTING_FILE, "w") as f: #w = write
        json.dump(settings, f, indent=4)



