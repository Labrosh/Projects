import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from api.tmdb_api import TMDbAPI
from models.movie import Movie
from movie_data import MovieDataManager

def search_movie(app):
    app.movie_search_gui.search_movie()

def display_search_results(app, results):
    app.movie_search_gui.display_search_results(results)

class MovieSearchGUI:
    def __init__(self, app):
        self.app = app
        self.movie_data_manager = MovieDataManager()

    def search_movie(self):
        query = self.app.search_entry.get().strip()
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
        search_window = tk.Toplevel(self.app.root)
        search_window.title("Search Results")
        search_window.geometry("400x300")

        result_listbox = tk.Listbox(search_window, height=self.app.ui_settings["listbox_height"], width=self.app.ui_settings["listbox_width"])
        result_listbox.pack(pady=self.app.ui_settings["element_spacing"])

        for movie in results:
            result_listbox.insert(tk.END, f"{movie['title']} ({movie['release_date']})")

        def add_selected_movie():
            selected = result_listbox.curselection()
            if selected:
                movie_data = results[selected[0]]
                movie = Movie(movie_data["id"], movie_data["title"], movie_data["release_date"], movie_data["poster_path"])
                poster_path = movie.save_poster()
                details = TMDbAPI.get_movie_details(movie.id)
                movie.details = details
                self.movie_data_manager.add_movie(movie)
                self.app.load_movies()
                search_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a movie!")

        def show_movie_poster(event):
            selected = result_listbox.curselection()
            if selected:
                movie = results[selected[0]]
                if movie['poster_path']:
                    poster_window = tk.Toplevel(self.app.root)
                    poster_window.title(movie['title'])
                    poster_image = Image.open(requests.get(movie['poster_path'], stream=True).raw)
                    poster_image = poster_image.resize((300, 450), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)
                    poster_label = tk.Label(poster_window, image=poster_photo)
                    poster_label.image = poster_photo
                    poster_label.pack()

        result_listbox.bind('<<ListboxSelect>>', show_movie_poster)

        add_result_button = tk.Button(search_window, text="Add Selected Movie", command=add_selected_movie)
        add_result_button.pack(pady=self.app.ui_settings["element_spacing"])
