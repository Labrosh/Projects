import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
from models.manager import MovieManager
from gui.gui_helper import update_listbox, show_movie_poster, show_movie_details, create_widgets, open_settings
from data.settings import SettingsManager  # Updated import path
from gui.gui_search import MovieSearchGUI
from gui.gui_movie_list import MovieListGUI, add_movie, add_movie_to_watchlist, remove_movie, mark_as_watched, unwatch_movie
from gui.theme import ThemeManager

# Set up logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.settings_manager = SettingsManager()
        self.ui_settings = self.settings_manager.ui_settings
        
        # Configure root window before anything else
        self.root.configure(bg=self.ui_settings["background_color"])
        self.root.option_add("*Background", self.ui_settings["background_color"])
        self.root.option_add("*Foreground", self.ui_settings["text_color"])
        self.root.option_add("*selectBackground", self.ui_settings["selection_bg"])
        self.root.option_add("*selectForeground", self.ui_settings["selection_fg"])
        
        self.root.title("Movielog - Movie Tracker")
        self.root.geometry(f"{self.ui_settings['window_width']}x{self.ui_settings['window_height']}")
        
        # Apply theme to root window and force update
        ThemeManager.apply_theme(self.root, self.ui_settings)
        self.root.update_idletasks()
        
        self.movie_manager = MovieManager()
        self.movie_search_gui = MovieSearchGUI(self)
        self.movie_list_gui = MovieListGUI(self)
        create_widgets(self)
        self.load_movies()

    def load_movies(self):
        logging.debug("Loading movies...")
        update_listbox(self.to_watch_listbox, self.movie_manager.movies_to_watch)
        update_listbox(self.watched_listbox, self.movie_manager.movies_watched)

    def add_movie(self):
        add_movie(self)
        self.load_movies()  # Ensure the movie list is updated after adding a movie

    def add_movie_to_watchlist(self, title, release_date="Unknown"):
        add_movie_to_watchlist(self, title, release_date)
        self.load_movies()  # Ensure the movie list is updated after adding a movie to the watchlist

    def search_movie(self):
        self.movie_search_gui.search_movie()

    def display_search_results(self, results):
        self.movie_search_gui.display_search_results(results)

    def remove_movie(self):
        remove_movie(self)
        self.load_movies()  # Ensure the movie list is updated after removing a movie

    def mark_as_watched(self):
        mark_as_watched(self)
        self.load_movies()  # Ensure the movie list is updated after marking a movie as watched

    def unwatch_movie(self):
        unwatch_movie(self)
        self.load_movies()  # Ensure the movie list is updated after unwatching a movie

    def open_settings(self):
        open_settings(self)

    def update_ui(self):
        # Only set minimum size, allow window to be larger
        self.root.minsize(
            self.ui_settings["window_width"],
            self.ui_settings["window_height"]
        )
        
        self.label_to_watch.config(font=("Arial", self.ui_settings["font_size"]))
        self.label_watched.config(font=("Arial", self.ui_settings["font_size"]))
        
        # Update just the font sizes and colors, let the geometry manager handle sizing
        self.to_watch_listbox.config(font=("Arial", self.ui_settings["font_size"]))
        self.watched_listbox.config(font=("Arial", self.ui_settings["font_size"]))

    def show_selected_movie_details(self):
        selected_to_watch = self.to_watch_listbox.curselection()
        selected_watched = self.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_manager.movies_to_watch[selected_to_watch[0]]
            show_movie_details(self.root, movie)
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            show_movie_details(self.root, movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view the details!")

    def show_selected_movie_poster(self):
        selected_to_watch = self.to_watch_listbox.curselection()
        selected_watched = self.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_manager.movies_to_watch[selected_to_watch[0]]
            self.show_movie_poster(self.root, movie)
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            self.show_movie_poster(self.root, movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view the poster!")

    def show_movie_poster(self, root, movie):
        poster_path = movie.get_poster_path()
        if poster_path and os.path.exists(poster_path):
            poster_window = tk.Toplevel(root)
            poster_window.title(movie.title)
            ThemeManager.apply_theme(poster_window, self.ui_settings)
            poster_image = Image.open(poster_path)
            poster_image = poster_image.resize((300, 450), Image.LANCZOS)
            poster_photo = ImageTk.PhotoImage(poster_image)
            poster_label = tk.Label(poster_window, image=poster_photo)
            poster_label.image = poster_photo
            poster_label.pack()
        else:
            messagebox.showwarning("Warning", "Poster not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
