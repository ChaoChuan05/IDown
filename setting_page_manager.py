from common_import import *

# Determine where to store user settings
if getattr(sys, 'frozen', False):
    # Running as a bundled exe — store settings in user’s AppData or home folder
    app_dir = os.path.join(os.path.expanduser("~"), "IDownSettings")
else:
    # Running from source — store settings in the same folder
    app_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the folder exists
os.makedirs(app_dir, exist_ok=True)

SETTING_FILE = os.path.join(app_dir, "settings.json")


def load_setting() -> dict:
    """Load user setting or create default"""
    if os.path.exists(SETTING_FILE):
        with open(SETTING_FILE, "r") as f:
            return json.load(f)
    return {"download_path": os.path.join(os.path.expanduser("~"), "Downloads")}


def save_setting(new_data: dict) -> None:
    """Update and save user settings safely"""
    settings = load_setting()
    settings.update(new_data)
    with open(SETTING_FILE, "w") as f:
        json.dump(settings, f, indent=4)


