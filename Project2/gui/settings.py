import json

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.ui_settings = {
            "font_size": 16,
            "element_spacing": 5,
            "listbox_height": 10,
            "listbox_width": 50,
            "window_width": 600,
            "window_height": 900
        }
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as file:
                self.ui_settings.update(json.load(file))
        except FileNotFoundError:
            pass

    def save_settings_to_file(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.ui_settings, file)

    def update_settings(self, new_settings):
        self.ui_settings.update(new_settings)
        self.save_settings_to_file()
