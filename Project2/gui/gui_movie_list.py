import tkinter as tk
from tkinter import messagebox
import logging
from models.movie import Movie
from models.manager import MovieManager
from gui.color_scheme import ColorSchemeManager

class MovieListGUI:
    def __init__(self, app):
        self.app = app
        self.movie_manager = app.movie_manager  # Use the app's MovieManager instance

    def add_movie(self):
        logging.debug("Adding movie...")
        movie_title = self.app.movie_entry.get().strip()
        if movie_title:
            self.add_movie_to_watchlist(movie_title)
            self.app.load_movies()  # Ensure the movie list is updated after adding a movie
            self.app.movie_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    def add_movie_to_watchlist(self, title, release_date="Unknown"):
        logging.debug(f"Adding movie to watchlist: {title}")
        movie = Movie(None, title, release_date)
        self.movie_manager.add_movie(movie)
        self.app.load_movies()  # Ensure the movie list is updated after adding a movie to the watchlist

    def remove_movie(self):
        logging.debug("Removing movie...")
        selected_to_watch = self.app.to_watch_listbox.curselection()
        selected_watched = self.app.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_manager.movies_to_watch[selected_to_watch[0]]
            self.movie_manager.remove_movie(movie)
            self.app.load_movies()  # Ensure the movie list is updated after removing a movie
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            self.movie_manager.remove_movie(movie)
            self.app.load_movies()  # Ensure the movie list is updated after removing a movie
        else:
            messagebox.showwarning("Warning", "Please select a movie to remove!")

    def mark_as_watched(self):
        logging.debug("Marking movie as watched...")
        selected = self.app.to_watch_listbox.curselection()
        if selected:
            movie_title = self.app.to_watch_listbox.get(selected[0])
            movie = next((m for m in self.movie_manager.movies_to_watch if m.title == movie_title), None)
            if movie:
                self.movie_manager.mark_as_watched(movie)
                self.app.load_movies()  # Ensure the movie list is updated after marking a movie as watched
        else:
            messagebox.showwarning("Warning", "Please select a movie to mark as watched!")

    def unwatch_movie(self):
        logging.debug("Unwatching movie...")
        selected = self.app.watched_listbox.curselection()
        if selected:
            movie_title = self.app.watched_listbox.get(selected[0])
            movie = next((m for m in self.movie_manager.movies_watched if m.title == movie_title), None)
            if movie:
                self.movie_manager.unwatch_movie(movie)
                self.app.load_movies()  # Ensure the movie list is updated after unwatching a movie
        else:
            messagebox.showwarning("Warning", "Please select a movie to un-watch!")
