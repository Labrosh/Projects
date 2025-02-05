import json
import os
from gui.color_scheme import ColorSchemeManager  # This import is correct now

class SettingsManager:
    def __init__(self, settings_file="gui/settings.json"):  # Updated path to be in gui folder
        self.settings_file = os.path.join(os.path.expanduser("~"), ".movielog", "settings.json")
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        # Update base settings with fixed window dimensions
        self.ui_settings = {
            "font_size": 12,
            "element_spacing": 10,
            "listbox_height": 15,
            "listbox_width": 40,
            "window_width": 1000,
            "window_height": 900,    # Increased from 800 to 900
            "minimum_width": 800,
            "minimum_height": 800,   # Increased from 700 to 800
            "button_width": 15,
            "button_padding": 5,
            "font_family": "Helvetica",
            "offline_mode": False,
            "api_key": None,
            "current_scheme": "Dark Purple",
        }
        self.load_settings()
        # Add color scheme colors to settings
        self.ui_settings.update(ColorSchemeManager.get_scheme(self.ui_settings["current_scheme"]).colors)

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as file:
                loaded_settings = json.load(file)
                self.ui_settings.update(loaded_settings)
                # Update color scheme colors
                self.ui_settings.update(ColorSchemeManager.get_scheme(self.ui_settings["current_scheme"]).colors)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings_to_file()

    def save_settings_to_file(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.ui_settings, file)

    def update_settings(self, new_settings):
        # Preserve window dimensions when updating settings
        current_width = self.ui_settings.get("window_width", 1000)
        current_height = self.ui_settings.get("window_height", 800)
        
        # Update settings
        self.ui_settings.update(new_settings)
        
        # Restore window dimensions
        self.ui_settings["window_width"] = current_width
        self.ui_settings["window_height"] = current_height
        
        # Update color scheme colors if scheme changed
        if "current_scheme" in new_settings:
            self.ui_settings.update(ColorSchemeManager.get_scheme(new_settings["current_scheme"]).colors)
        
        self.save_settings_to_file()

    def get_available_schemes(self):
        return ColorSchemeManager.get_available_schemes()

    def set_api_key(self, api_key):
        self.ui_settings["api_key"] = api_key
        self.ui_settings["offline_mode"] = False
        self.save_settings_to_file()

    def enable_offline_mode(self):
        self.ui_settings["offline_mode"] = True
        self.save_settings_to_file()

    def is_offline_mode(self):
        return self.ui_settings.get("offline_mode", False)

    def get_api_key(self):
        return self.ui_settings.get("api_key")
