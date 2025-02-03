import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
from models.manager import MovieManager
from models.movie import Movie
from api.tmdb_api import TMDbAPI
from gui.gui_helper import update_listbox, show_movie_poster, show_movie_details, create_widgets, open_settings
from gui.settings import SettingsManager
from gui.gui_search import MovieSearchGUI
from gui.gui_movie_list import MovieListGUI, add_movie, add_movie_to_watchlist, remove_movie, mark_as_watched, unwatch_movie

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movielog - Movie Tracker")
        self.settings_manager = SettingsManager()
        self.ui_settings = self.settings_manager.ui_settings
        self.root.geometry(f"{self.ui_settings['window_width']}x{self.ui_settings['window_height']}")
        self.movie_manager = MovieManager()
        self.movie_search_gui = MovieSearchGUI(self)
        self.movie_list_gui = MovieListGUI(self)
        create_widgets(self)
        self.load_movies()

    def load_movies(self):
        update_listbox(self.to_watch_listbox, self.movie_manager.movies_to_watch)
        update_listbox(self.watched_listbox, self.movie_manager.movies_watched)

    def add_movie(self):
        add_movie(self)

    def add_movie_to_watchlist(self, title, release_date="Unknown"):
        add_movie_to_watchlist(self, title, release_date)

    def search_movie(self):
        self.movie_search_gui.search_movie()

    def display_search_results(self, results):
        self.movie_search_gui.display_search_results(results)

    def remove_movie(self):
        remove_movie(self)

    def mark_as_watched(self):
        mark_as_watched(self)

    def unwatch_movie(self):
        unwatch_movie(self)

    def open_settings(self):
        open_settings(self)

    def update_ui(self):
        self.root.geometry(f"{self.ui_settings['window_width']}x{self.ui_settings['window_height']}")
        self.label_to_watch.config(font=("Arial", self.ui_settings["font_size"]))
        self.label_watched.config(font=("Arial", self.ui_settings["font_size"]))
        self.to_watch_listbox.config(height=self.ui_settings["listbox_height"], width=self.ui_settings["listbox_width"])
        self.watched_listbox.config(height=self.ui_settings["listbox_height"], width=self.ui_settings["listbox_width"])

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
