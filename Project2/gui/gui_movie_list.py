import tkinter as tk
from tkinter import messagebox
from models.movie import Movie
from movie_data import MovieDataManager

class MovieListGUI:
    def __init__(self, app):
        self.app = app
        self.movie_data_manager = MovieDataManager()

    def add_movie(self):
        movie_title = self.app.movie_entry.get().strip()
        if movie_title:
            self.add_movie_to_watchlist(movie_title)
            self.app.load_movies()
            self.app.movie_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    def add_movie_to_watchlist(self, title, release_date="Unknown"):
        movie = Movie(None, title, release_date)
        self.movie_data_manager.add_movie(movie)

    def remove_movie(self):
        selected_to_watch = self.app.to_watch_listbox.curselection()
        selected_watched = self.app.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_data_manager.movies_to_watch[selected_to_watch[0]]
            self.movie_data_manager.remove_movie(movie)
            self.app.load_movies()
        elif selected_watched:
            movie = self.movie_data_manager.movies_watched[selected_watched[0]]
            self.movie_data_manager.remove_movie(movie)
            self.app.load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to remove!")

    def mark_as_watched(self):
        selected = self.app.to_watch_listbox.curselection()
        if selected:
            movie_title = self.app.to_watch_listbox.get(selected[0])
            movie = next((m for m in self.movie_data_manager.movies_to_watch if m.title == movie_title), None)
            if movie:
                self.movie_data_manager.mark_as_watched(movie)
                self.app.load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to mark as watched!")

    def unwatch_movie(self):
        selected = self.app.watched_listbox.curselection()
        if selected:
            movie = self.movie_data_manager.movies_watched[selected[0]]
            self.movie_data_manager.movies_watched.remove(movie)
            self.movie_data_manager.movies_to_watch.append(movie)
            self.movie_data_manager.save_data()
            self.app.load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to un-watch!")
