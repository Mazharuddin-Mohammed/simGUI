"""
settings.py - Application settings management for Vulkan GUI
"""
import json
import os
from datetime import datetime

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",
    "recent_files": [],
    "performance": {
        "vsync": True,
        "max_fps": 60
    },
    "debug_overlay": {
        "show_fps": True,
        "show_memory": False,
        "show_device_info": False,
        "enabled": True
    },
    "log_level": "info"
}

def load_settings():
    """Load settings from disk, merging with defaults."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                data = json.load(f)
                def merge(d, default):
                    for k, v in default.items():
                        if k not in d:
                            d[k] = v
                        elif isinstance(v, dict):
                            merge(d[k], v)
                    return d
                return merge(data, DEFAULT_SETTINGS.copy())
            except Exception:
                return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to disk."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def reset_settings():
    """Delete settings file from disk."""
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)

def add_recent_file(settings, path):
    """Add a file to the recent files list, keeping max 10."""
    if path not in settings["recent_files"]:
        settings["recent_files"].insert(0, path)
        settings["recent_files"] = settings["recent_files"][:10]
        save_settings(settings)

def get_timestamp():
    """Return a timestamp string for filenames."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
