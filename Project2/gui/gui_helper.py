import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
from gui.color_scheme import ColorSchemeManager
from gui.widgets.movie_list_panel import MovieListPanel
from gui.widgets.control_panel import ControlPanel
from gui.widgets.entry_panel import EntryPanel
from gui.widgets.tooltip import TooltipManager
from gui.widgets.window_manager import WindowManager

class GUIHelper:
    def __init__(self, app):
        self.app = app
        self.window_manager = WindowManager(app)
        self.tooltip_manager = TooltipManager(app)
        
    def update_listbox(self, listbox, items):
        logging.debug(f"Updating listbox with {len(items)} items")
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, item)  # Pass the movie object instead of item.title
        listbox.update()

    def show_movie_poster(self, movie):
        poster_path = movie.get_poster_path()
        if (poster_path):
            if not poster_path.startswith("http"):
                poster_path = os.path.join("data/posters", os.path.basename(poster_path))
            if os.path.exists(poster_path):
                self.window_manager.show_poster_window(movie, poster_path)
            else:
                messagebox.showwarning("Warning", "Poster not found.")

    def show_movie_details(self, movie):
        details = movie.details
        if details:
            self.window_manager.show_details_window(movie)
        else:
            messagebox.showwarning("Warning", "Details not found.")

    def create_widgets(self):
        # Configure root window style
        ColorSchemeManager.apply_scheme(self.app.root, self.app.ui_settings)
        
        # Make the root window responsive
        self.app.root.grid_rowconfigure(0, weight=1)
        self.app.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        main_frame = tk.Frame(self.app.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        ColorSchemeManager.apply_scheme(main_frame, self.app.ui_settings)

        # Create panels
        control_panel = ControlPanel(main_frame, self.app)
        movie_list_panel = MovieListPanel(main_frame, self.app)
        entry_panel = EntryPanel(main_frame, self.app)

        # Setup tooltips for entry panel buttons
        entry_panel.quick_add_btn.bind("<Enter>", 
            lambda e: self.tooltip_manager.show_tooltip(entry_panel.quick_add_btn, 
            "Quickly add a movie without TMDb details"))
        entry_panel.quick_add_btn.bind("<Leave>", self.tooltip_manager.hide_tooltip)
        
        entry_panel.tmdb_btn.bind("<Enter>", 
            lambda e: self.tooltip_manager.show_tooltip(entry_panel.tmdb_btn, 
            "Search TMDb for movie details and poster"))
        entry_panel.tmdb_btn.bind("<Leave>", self.tooltip_manager.hide_tooltip)

        # Layout panels
        control_panel.grid(row=0, column=0, sticky="ns", padx=10)
        movie_list_panel.grid(row=0, column=1, sticky="nsew")
        entry_panel.grid(row=1, column=1, sticky="ew", pady=10)

        # Store references needed by app
        self.app.to_watch_listbox = movie_list_panel.to_watch_listbox
        self.app.watched_listbox = movie_list_panel.watched_listbox
        self.app.movie_entry = entry_panel.quick_add_entry
        self.app.search_entry = entry_panel.search_entry
        self.app.label_to_watch = movie_list_panel.label_to_watch
        self.app.label_watched = movie_list_panel.label_watched

        # Add status bar at bottom
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.app.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=self.app.ui_settings["secondary_bg"],
            fg=self.app.ui_settings["text_color"]
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def show_status(self, message, timeout=3000):
        """Show a message in the status bar that disappears after timeout ms"""
        self.status_var.set(message)
        self.app.root.after(timeout, lambda: self.status_var.set(""))

    def open_settings(self):
        self.window_manager.show_settings_window()
