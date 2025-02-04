import json
import os
from gui.color_scheme import ColorSchemeManager  # This import is correct now

class SettingsManager:
    def __init__(self, settings_file="gui/settings.json"):  # Updated path to be in gui folder
        self.settings_file = settings_file
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)
        
        # Base settings without theme colors
        self.ui_settings = {
            "font_size": 12,
            "element_spacing": 10,
            "listbox_height": 15,
            "listbox_width": 40,
            "window_width": 1200,
            "window_height": 600,
            "button_width": 15,
            "button_padding": 5,
            "font_family": "Helvetica",
            "current_scheme": "Dark Purple",  # Default scheme
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
        # Update settings
        self.ui_settings.update(new_settings)
        # Update color scheme colors if scheme changed
        if "current_scheme" in new_settings:
            self.ui_settings.update(ColorSchemeManager.get_scheme(new_settings["current_scheme"]).colors)
        self.save_settings_to_file()

    def get_available_schemes(self):
        return ColorSchemeManager.get_available_schemes()
