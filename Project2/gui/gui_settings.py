import json
import os
import stat
from gui.color_scheme import ColorSchemeManager

class SettingsManager:
    def __init__(self):
        # Use user's home directory for settings
        self.settings_file = os.path.join(os.path.expanduser("~"), ".movielog", "settings.json")
        self._ensure_settings_dir()
        
        # Base settings
        self.ui_settings = {
            # Window settings
            "window_width": 1000,
            "window_height": 900,
            "minimum_width": 800,
            "minimum_height": 800,
            
            # UI element settings
            "font_family": "Helvetica",
            "font_size": 12,
            "button_width": 15,
            "button_padding": 5,
            "element_spacing": 10,
            "listbox_height": 15,
            "listbox_width": 40,
            
            # Application state
            "offline_mode": False,
            "api_key": None,
            "current_scheme": "Dark Purple",
        }
        
        self.load_settings()
        # Add color scheme colors
        self.ui_settings.update(
            ColorSchemeManager.get_scheme(self.ui_settings["current_scheme"]).colors
        )

    def _ensure_settings_dir(self):
        """Create settings directory with proper permissions"""
        settings_dir = os.path.dirname(self.settings_file)
        os.makedirs(settings_dir, exist_ok=True)
        # Set directory permissions to 700 (rwx------)
        os.chmod(settings_dir, stat.S_IRWXU)

    def load_settings(self):
        """Load settings from file, creating if needed"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as file:
                    loaded_settings = json.load(file)
                    self.ui_settings.update(loaded_settings)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.save_settings_to_file()
            
    def save_settings_to_file(self):
        """Save current settings to file"""
        # Ensure directory exists with proper permissions
        self._ensure_settings_dir()
        
        with open(self.settings_file, "w") as file:
            json.dump(self.ui_settings, file, indent=2)
        # Set file permissions to 600 (rw-------)
        os.chmod(self.settings_file, stat.S_IRUSR | stat.S_IWUSR)

    def update_settings(self, new_settings):
        """Update settings while preserving window dimensions"""
        current_width = self.ui_settings.get("window_width")
        current_height = self.ui_settings.get("window_height")
        
        self.ui_settings.update(new_settings)
        
        # Preserve window dimensions
        if "window_width" in new_settings or "window_height" in new_settings:
            self.ui_settings["window_width"] = current_width
            self.ui_settings["window_height"] = current_height
        
        # Update color scheme if changed
        if "current_scheme" in new_settings:
            self.ui_settings.update(
                ColorSchemeManager.get_scheme(new_settings["current_scheme"]).colors
            )
        
        self.save_settings_to_file()

    # API key management
    def set_api_key(self, api_key):
        """Set API key and disable offline mode"""
        self.ui_settings["api_key"] = api_key
        self.ui_settings["offline_mode"] = False
        self.save_settings_to_file()

    def enable_offline_mode(self):
        """Enable offline mode"""
        self.ui_settings["offline_mode"] = True
        self.save_settings_to_file()

    def is_offline_mode(self):
        """Check if offline mode is enabled"""
        return self.ui_settings.get("offline_mode", False)

    def get_api_key(self):
        """Get stored API key"""
        return self.ui_settings.get("api_key")

    # Theme management
    def get_available_schemes(self):
        """Get list of available color schemes"""
        return ColorSchemeManager.get_available_schemes()
