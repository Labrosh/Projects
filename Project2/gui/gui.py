import tkinter as tk
from tkinter import messagebox
from models.manager import MovieManager
from gui.gui_helper import GUIHelper
from gui.gui_settings import SettingsManager
from gui.gui_search import MovieSearchGUI
from gui.gui_movie_list import MovieListGUI
from gui.color_scheme import ColorSchemeManager
from gui.widgets.entry_panel import EntryPanel  # Ensure this import is included
from gui.widgets.api_key_dialog import APIKeyDialog
from api.tmdb_api import TMDbAPI
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MovieTrackerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Movie Tracker")
        
        # Initialize managers and GUIs
        self.settings_manager = SettingsManager()
        self.ui_settings = self.settings_manager.ui_settings
        self.movie_manager = MovieManager()
        
        # Initialize GUI components
        self.gui_helper = GUIHelper(self)
        self.movie_list_gui = MovieListGUI(self)
        self.movie_search_gui = MovieSearchGUI(self.root, self.movie_manager)
        
        # Check for API key
        self.check_api_key()
        
        # Set window dimensions from settings with increased height
        width = self.ui_settings.get("window_width", 1000)
        height = self.ui_settings.get("window_height", 900)  # Increased from 800 to 900
        
        # Calculate center position
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        
        # Set window geometry and constraints
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.minsize(800, 800)  # Increased minimum height from 700 to 800
        
        # Setup GUI
        self.gui_helper.create_widgets()
        self.load_movies()
        
        # Bind refresh event
        self.root.bind("<<RefreshMovieList>>", lambda e: self.refresh_movie_list())

    def run(self):
        self.root.mainloop()

    def load_movies(self):
        self.gui_helper.update_listbox(self.to_watch_listbox, self.movie_manager.movies_to_watch)
        self.gui_helper.update_listbox(self.watched_listbox, self.movie_manager.movies_watched)
        self.gui_helper.show_status("Movies loaded successfully")

    def update_ui(self):
        # Store current window dimensions before recreating widgets
        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()
        
        # Update UI
        for widget in self.root.winfo_children():
            widget.destroy()
        self.gui_helper.create_widgets()
        self.load_movies()
        
        # Restore window dimensions
        self.root.geometry(f"{current_width}x{current_height}")

    def show_selected_movie_details(self):
        if self.root.winfo_exists():  # Check if the root window exists
            selected_movie = self.get_selected_movie()
            if selected_movie:
                self.gui_helper.show_movie_details(selected_movie)
            else:
                messagebox.showwarning("Warning", "Please select a movie to view details!")

    def show_selected_movie_poster(self):
        if self.root.winfo_exists():  # Check if the root window exists
            selected_movie = self.get_selected_movie()
            if selected_movie:
                self.gui_helper.show_movie_poster(selected_movie)
            else:
                messagebox.showwarning("Warning", "Please select a movie to view poster!")

    def get_selected_movie(self):
        selected_index = self.to_watch_listbox.curselection()
        if selected_index:
            return self.to_watch_listbox.items[selected_index[0]]
        selected_index = self.watched_listbox.curselection()
        if selected_index:
            return self.watched_listbox.items[selected_index[0]]
        return None

    def open_settings(self):
        """Open the settings window"""
        self.gui_helper.open_settings()

    def get_ui_settings(self):
        return {
            "background_color": "#ffffff",
            "font_family": "Helvetica",
            "font_size": 12,
            "entry_bg": "#f0f0f0",
            "entry_fg": "#000000",
            "text_color": "#000000",
            "button_color": "#0078d7",
            "button_text_color": "#ffffff",
            "current_scheme": "default"  # Add this line to include the current scheme
        }

    def refresh_movie_list(self):
        """Refresh the movie list display"""
        self.load_movies()

    def check_api_key(self):
        """Check for API key and prompt if needed"""
        if not self.settings_manager.get_api_key() and not self.settings_manager.is_offline_mode():
            dialog = APIKeyDialog(self.root, self.settings_manager)
            self.root.wait_window(dialog)
            
            if dialog.result == "api_key":
                TMDbAPI.set_api_key(self.settings_manager.get_api_key())
            elif dialog.result == "offline":
                self.movie_search_gui.disable_search()

    def toggle_offline_mode(self, enable=True):
        """Toggle offline mode"""
        if enable:
            self.settings_manager.enable_offline_mode()
            self.movie_search_gui.disable_search()
        else:
            api_key = self.settings_manager.get_api_key()
            if api_key and TMDbAPI.validate_api_key(api_key):
                self.settings_manager.set_api_key(api_key)
                TMDbAPI.set_api_key(api_key)
                self.movie_search_gui.enable_search()

if __name__ == "__main__":
    app = MovieTrackerApp()
    app.run()
