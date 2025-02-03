import json
import os
from gui.theme import ThemeManager

class SettingsManager:
    def __init__(self, settings_file="data/settings.json"):
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
            "current_theme": "Dark Purple",  # Default theme
        }
        self.load_settings()
        # Add theme colors to settings
        self.ui_settings.update(ThemeManager.get_theme(self.ui_settings["current_theme"]).colors)

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as file:
                loaded_settings = json.load(file)
                self.ui_settings.update(loaded_settings)
                # Update theme colors
                self.ui_settings.update(ThemeManager.get_theme(self.ui_settings["current_theme"]).colors)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings_to_file()

    def save_settings_to_file(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.ui_settings, file)

    def update_settings(self, new_settings):
        # Update settings
        self.ui_settings.update(new_settings)
        # Update theme colors if theme changed
        if "current_theme" in new_settings:
            self.ui_settings.update(ThemeManager.get_theme(new_settings["current_theme"]).colors)
        self.save_settings_to_file()

    def get_available_themes(self):
        return ThemeManager.get_available_themes()
