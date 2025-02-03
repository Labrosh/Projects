import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
from models.manager import MovieManager  # This file defines the MovieManager class. It handles loading, saving, and managing lists of movies.
from models.movie import Movie  # This file defines the Movie class. It encapsulates all logic and behavior for a single movie object.
from api.tmdb_api import TMDbAPI
from gui.gui_helper import update_listbox, show_movie_poster, show_movie_details
from gui.settings import SettingsManager

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movielog - Movie Tracker")
        self.settings_manager = SettingsManager()
        self.ui_settings = self.settings_manager.ui_settings
        self.root.geometry(f"{self.ui_settings['window_width']}x{self.ui_settings['window_height']}")
        self.movie_manager = MovieManager()
        self.create_widgets()
        self.load_movies()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        label_to_watch = tk.Label(main_frame, text="Movies to Watch", font=("Arial", self.ui_settings["font_size"]))
        label_to_watch.pack(pady=self.ui_settings["element_spacing"])

        self.to_watch_listbox = tk.Listbox(main_frame, height=self.ui_settings["listbox_height"], width=self.ui_settings["listbox_width"])
        self.to_watch_listbox.pack(pady=self.ui_settings["element_spacing"])

        label_watched = tk.Label(main_frame, text="Movies Watched", font=("Arial", self.ui_settings["font_size"]))
        label_watched.pack(pady=self.ui_settings["element_spacing"])

        self.watched_listbox = tk.Listbox(main_frame, height=self.ui_settings["listbox_height"], width=self.ui_settings["listbox_width"])
        self.watched_listbox.pack(pady=self.ui_settings["element_spacing"])

        movie_entry_frame = tk.Frame(main_frame)
        movie_entry_frame.pack(pady=self.ui_settings["element_spacing"])

        self.movie_entry = tk.Entry(movie_entry_frame, width=40)
        self.movie_entry.pack(side=tk.LEFT, padx=self.ui_settings["element_spacing"])

        add_button = tk.Button(movie_entry_frame, text="Add Movie", command=self.add_movie)
        add_button.pack(side=tk.LEFT, padx=self.ui_settings["element_spacing"])

        search_frame = tk.Frame(main_frame)
        search_frame.pack(pady=self.ui_settings["element_spacing"])

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=self.ui_settings["element_spacing"])

        search_button = tk.Button(search_frame, text="Search & Add Movie", command=self.search_movie)
        search_button.pack(side=tk.LEFT, padx=self.ui_settings["element_spacing"])

        remove_button = tk.Button(main_frame, text="Remove Movie", command=self.remove_movie)
        remove_button.pack(pady=self.ui_settings["element_spacing"])

        watched_button = tk.Button(main_frame, text="Mark as Watched", command=self.mark_as_watched)
        watched_button.pack(pady=self.ui_settings["element_spacing"])

        unwatch_button = tk.Button(main_frame, text="Un-Watch", command=self.unwatch_movie)
        unwatch_button.pack(pady=self.ui_settings["element_spacing"])

        settings_button = tk.Button(main_frame, text="Settings", command=self.open_settings)
        settings_button.pack(pady=self.ui_settings["element_spacing"])

        view_details_button = tk.Button(main_frame, text="View Details", command=self.show_selected_movie_details)
        view_details_button.pack(pady=self.ui_settings["element_spacing"])

        view_poster_button = tk.Button(main_frame, text="View Poster", command=self.show_selected_movie_poster)
        view_poster_button.pack(pady=self.ui_settings["element_spacing"])

    def load_movies(self):
        update_listbox(self.to_watch_listbox, self.movie_manager.movies_to_watch)
        update_listbox(self.watched_listbox, self.movie_manager.movies_watched)

    def add_movie(self):
        movie_title = self.movie_entry.get().strip()
        if movie_title:
            self.add_movie_to_watchlist(movie_title)
            self.load_movies()
            self.movie_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    def add_movie_to_watchlist(self, title, release_date="Unknown"):
        movie = Movie(None, title, release_date)
        self.movie_manager.add_movie(movie)

    def search_movie(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a movie name to search!")
            return

        try:
            results = TMDbAPI.search_movie(query)
            if not results:
                messagebox.showinfo("Info", "No results found.")
            else:
                self.display_search_results(results)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except ConnectionError as e:
            messagebox.showerror("Error", "Failed to connect to TMDb.")

    def display_search_results(self, results):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Results")
        search_window.geometry("400x300")

        result_listbox = tk.Listbox(search_window, height=self.ui_settings["listbox_height"], width=self.ui_settings["listbox_width"])
        result_listbox.pack(pady=self.ui_settings["element_spacing"])

        for movie in results:
            result_listbox.insert(tk.END, f"{movie['title']} ({movie['release_date']})")

        def add_selected_movie():
            selected = result_listbox.curselection()
            if selected:
                movie = results[selected[0]]
                poster_path = self.movie_manager.save_poster(movie)
                details = TMDbAPI.get_movie_details(movie['id'])
                self.movie_manager.add_movie(Movie(movie['id'], movie['title'], movie['release_date'], poster_path or movie['poster_path'], details))
                self.load_movies()
                search_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a movie!")

        def show_movie_poster(event):
            selected = result_listbox.curselection()
            if selected:
                movie = results[selected[0]]
                if movie['poster_path']:
                    poster_window = tk.Toplevel(self.root)
                    poster_window.title(movie['title'])
                    poster_image = Image.open(requests.get(movie['poster_path'], stream=True).raw)
                    poster_image = poster_image.resize((300, 450), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)
                    poster_label = tk.Label(poster_window, image=poster_photo)
                    poster_label.image = poster_photo
                    poster_label.pack()

        result_listbox.bind('<<ListboxSelect>>', show_movie_poster)

        add_result_button = tk.Button(search_window, text="Add Selected Movie", command=add_selected_movie)
        add_result_button.pack(pady=self.ui_settings["element_spacing"])

    def remove_movie(self):
        selected_to_watch = self.to_watch_listbox.curselection()
        selected_watched = self.watched_listbox.curselection()

        if selected_to_watch:
            movie = self.movie_manager.movies_to_watch[selected_to_watch[0]]
            self.movie_manager.remove_movie(movie)
            self.load_movies()
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            self.movie_manager.remove_movie(movie)
            self.load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to remove!")

    def mark_as_watched(self):
        selected = self.to_watch_listbox.curselection()
        if selected:
            movie_title = self.to_watch_listbox.get(selected[0])
            movie = next((m for m in self.movie_manager.movies_to_watch if m.title == movie_title), None)
            if movie:
                self.movie_manager.mark_as_watched(movie)
                self.load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to mark as watched!")

    def unwatch_movie(self):
        selected = self.watched_listbox.curselection()
        if selected:
            movie = self.movie_manager.movies_watched[selected[0]]
            self.movie_manager.movies_watched.remove(movie)
            self.movie_manager.movies_to_watch.append(movie)
            self.movie_manager.save_data()
            self.load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to un-watch!")

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x400")

        tk.Label(settings_window, text="Font Size:").pack(pady=self.ui_settings["element_spacing"])
        font_size_entry = tk.Entry(settings_window)
        font_size_entry.insert(0, self.ui_settings["font_size"])
        font_size_entry.pack(pady=self.ui_settings["element_spacing"])

        tk.Label(settings_window, text="Element Spacing:").pack(pady=self.ui_settings["element_spacing"])
        element_spacing_entry = tk.Entry(settings_window)
        element_spacing_entry.insert(0, self.ui_settings["element_spacing"])
        element_spacing_entry.pack(pady=self.ui_settings["element_spacing"])

        tk.Label(settings_window, text="Listbox Height:").pack(pady=self.ui_settings["element_spacing"])
        listbox_height_entry = tk.Entry(settings_window)
        listbox_height_entry.insert(0, self.ui_settings["listbox_height"])
        listbox_height_entry.pack(pady=self.ui_settings["element_spacing"])

        tk.Label(settings_window, text="Listbox Width:").pack(pady=self.ui_settings["element_spacing"])
        listbox_width_entry = tk.Entry(settings_window)
        listbox_width_entry.insert(0, self.ui_settings["listbox_width"])
        listbox_width_entry.pack(pady=self.ui_settings["element_spacing"])

        tk.Label(settings_window, text="Window Width:").pack(pady=self.ui_settings["element_spacing"])
        window_width_entry = tk.Entry(settings_window)
        window_width_entry.insert(0, self.ui_settings["window_width"])
        window_width_entry.pack(pady=self.ui_settings["element_spacing"])

        tk.Label(settings_window, text="Window Height:").pack(pady=self.ui_settings["element_spacing"])
        window_height_entry = tk.Entry(settings_window)
        window_height_entry.insert(0, self.ui_settings["window_height"])
        window_height_entry.pack(pady=self.ui_settings["element_spacing"])

        def save_settings():
            self.ui_settings["font_size"] = int(font_size_entry.get())
            self.ui_settings["element_spacing"] = int(element_spacing_entry.get())
            self.ui_settings["listbox_height"] = int(listbox_height_entry.get())
            self.ui_settings["listbox_width"] = int(listbox_width_entry.get())
            self.ui_settings["window_width"] = int(window_width_entry.get())
            self.ui_settings["window_height"] = int(window_height_entry.get())
            self.settings_manager.save_settings_to_file()
            self.update_ui()
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings have been updated.")

        save_button = tk.Button(settings_window, text="Save Settings", command=save_settings)
        save_button.pack(pady=self.ui_settings["element_spacing"])

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
            show_movie_poster(self.root, movie)
        elif selected_watched:
            movie = self.movie_manager.movies_watched[selected_watched[0]]
            show_movie_poster(self.root, movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view the poster!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
