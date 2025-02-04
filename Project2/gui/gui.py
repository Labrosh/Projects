import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
from models.manager import MovieManager
from gui.gui_helper import GUIHelper
from gui.gui_settings import SettingsManager  # Updated import path
from gui.gui_search import MovieSearchGUI
from gui.gui_movie_list import MovieListGUI
from gui.color_scheme import ColorSchemeManager
import platform

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
        self.movie_search_gui = MovieSearchGUI(self)
        
        # Force a reasonable initial size and position
        self.root.withdraw()  # Hide window initially
        
        # Set reasonable fixed dimensions
        width = 1000
        height = 700
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set exact geometry before showing window
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Setup GUI
        self.gui_helper.create_widgets()
        self.load_movies()
        
        # Show window only after everything is set up
        self.root.deiconify()
        self.root.update_idletasks()
        self.root.minsize(800, 600)

    def run(self):
        self.root.mainloop()

    def load_movies(self):
        self.gui_helper.update_listbox(self.to_watch_listbox, self.movie_manager.movies_to_watch)
        self.gui_helper.update_listbox(self.watched_listbox, self.movie_manager.movies_watched)
        self.gui_helper.show_status("Movies loaded successfully")

    def update_ui(self):
        # Recreate widgets with new settings
        for widget in self.root.winfo_children():
            widget.destroy()
        self.gui_helper.create_widgets()
        self.load_movies()
        self.root.geometry(f"{self.ui_settings['window_width']}x{self.ui_settings['window_height']}")

    def show_selected_movie_details(self):
        """Show details for the currently selected movie"""
        selected_to_watch = self.to_watch_listbox.curselection()
        selected_watched = self.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_manager.movies_to_watch[selected_to_watch[0]]
            self.gui_helper.show_movie_details(movie)
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            self.gui_helper.show_movie_details(movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view details!")

    def show_selected_movie_poster(self):
        """Show poster for the currently selected movie"""
        selected_to_watch = self.to_watch_listbox.curselection()
        selected_watched = self.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_manager.movies_to_watch[selected_to_watch[0]]
            self.gui_helper.show_movie_poster(movie)
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            self.gui_helper.show_movie_poster(movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view poster!")

    def open_settings(self):
        """Open the settings window"""
        self.gui_helper.open_settings()

if __name__ == "__main__":
    app = MovieTrackerApp()
    app.run()
