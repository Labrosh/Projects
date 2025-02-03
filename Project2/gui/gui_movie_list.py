import tkinter as tk
from tkinter import messagebox
from models.movie import Movie

def add_movie(app):
    movie_title = app.movie_entry.get().strip()
    if movie_title:
        add_movie_to_watchlist(app, movie_title)
        app.load_movies()
        app.movie_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Movie name cannot be empty!")

def add_movie_to_watchlist(app, title, release_date="Unknown"):
    movie = Movie(None, title, release_date)
    app.movie_manager.add_movie(movie)

def remove_movie(app):
    selected_to_watch = app.to_watch_listbox.curselection()
    selected_watched = app.watched_listbox.curselection()

    if selected_to_watch:
        movie = app.movie_manager.movies_to_watch[selected_to_watch[0]]
        app.movie_manager.remove_movie(movie)
        app.load_movies()
    elif selected_watched:
        movie = app.movie_manager.movies_watched[selected_watched[0]]
        app.movie_manager.remove_movie(movie)
        app.load_movies()
    else:
        messagebox.showwarning("Warning", "Please select a movie to remove!")

def mark_as_watched(app):
    selected = app.to_watch_listbox.curselection()
    if selected:
        movie_title = app.to_watch_listbox.get(selected[0])
        movie = next((m for m in app.movie_manager.movies_to_watch if m.title == movie_title), None)
        if movie:
            app.movie_manager.mark_as_watched(movie)
            app.load_movies()
    else:
        messagebox.showwarning("Warning", "Please select a movie to mark as watched!")

def unwatch_movie(app):
    selected = app.watched_listbox.curselection()
    if selected:
        movie = app.movie_manager.movies_watched[selected[0]]
        app.movie_manager.movies_watched.remove(movie)
        app.movie_manager.movies_to_watch.append(movie)
        app.movie_manager.save_data()
        app.load_movies()
    else:
        messagebox.showwarning("Warning", "Please select a movie to un-watch!")
