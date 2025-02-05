import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import logging
from api.tmdb_api import TMDbAPI
from models.movie import Movie
from models.manager import MovieManager

class MovieSearchGUI:
    def __init__(self, app):
        self.app = app
        self.movie_manager = app.movie_manager
        self.temp_images = {}  # Cache images temporarily

    def search_movie(self, title=None):
        """Open the search window and perform a movie search"""
        self.search_window = SearchWindow(self.app.root, self)
        self.search_window.title("Search Movies")
        self.search_window.geometry("1000x600")

        if title:
            self.search_window.search_entry.insert(0, title)
            self.search_window.do_search()

    def _get_thumbnail(self, poster_path, size=(50, 75)):
        """Retrieve and cache small thumbnail images for search results"""
        if not poster_path:
            return None
        
        try:
            if poster_path not in self.temp_images:
                url = f"https://image.tmdb.org/t/p/w92{poster_path}"
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    img = Image.open(response.raw)
                    img.thumbnail(size)
                    self.temp_images[poster_path] = ImageTk.PhotoImage(img)
            return self.temp_images[poster_path]
        except Exception as e:
            logging.error(f"Error loading thumbnail: {e}")
            return None

    def _get_preview_image(self, poster_path, size=(200, 300)):
        """Retrieve and cache large preview images for movie selection"""
        key = f"preview_{poster_path}"
        return self._get_thumbnail(poster_path, size=size)

class SearchWindow(tk.Toplevel):
    def __init__(self, parent, search_gui):
        super().__init__(parent)
        self.search_gui = search_gui
        self.title("Search Movies")
        self.geometry("1000x600")

        # Layout
        left_panel = tk.Frame(self)
        left_panel.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        right_panel = tk.Frame(self)
        right_panel.pack(side='right', fill='both', padx=5, pady=5)

        # Search Entry
        entry_frame = tk.Frame(left_panel)
        entry_frame.pack(fill='x', pady=5)
        
        self.search_entry = tk.Entry(entry_frame)
        self.search_entry.pack(side='left', fill='x', expand=True)

        search_button = tk.Button(entry_frame, text="Search", command=self.do_search)
        search_button.pack(side='right', padx=5)

        # Results Area
        results_frame = tk.Frame(left_panel)
        results_frame.pack(fill='both', expand=True)

        self.results_canvas = tk.Canvas(results_frame)
        scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.results_canvas.yview)
        self.scrollable_frame = tk.Frame(self.results_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )

        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=480)
        self.results_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.results_canvas.pack(side="left", fill="both", expand=True)

        # Preview Panel
        preview_label = tk.Label(right_panel, text="Movie Preview", font=('Helvetica', 12, 'bold'))
        preview_label.pack(pady=5)

        self.preview_frame = tk.Frame(right_panel, width=300)
        self.preview_frame.pack(fill='both', expand=True)

        self.preview_poster = tk.Label(self.preview_frame)
        self.preview_poster.pack(pady=5)

        self.preview_title = tk.Label(self.preview_frame, wraplength=280, justify='center')
        self.preview_title.pack(pady=5)

        self.preview_info = tk.Text(self.preview_frame, wrap='word', height=10, width=35)
        self.preview_info.pack(pady=5, padx=5)
        self.preview_info.config(state='disabled')

        # Select Button
        self.select_button = tk.Button(self, text="Select Movie", command=self.select_movie)
        self.select_button.pack(pady=10)

    def do_search(self):
        """Perform a search and display results"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.search_gui.temp_images.clear()

        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a movie name!")
            return

        try:
            results = TMDbAPI.search_movie(query)
            if not results:
                tk.Label(self.scrollable_frame, text="No results found").pack(pady=10)
                return

            self.search_results = results  # Store results for selection
            for movie in results:
                self.display_movie_result(movie)

        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def display_movie_result(self, movie):
        """Create a result entry in the search list"""
        result_frame = tk.Frame(self.scrollable_frame, relief='groove', borderwidth=1)
        result_frame.pack(fill='x', pady=2, padx=5)
        result_frame.grid_columnconfigure(1, weight=1)

        if movie.get('poster_path'):
            try:
                image = self.search_gui._get_thumbnail(movie['poster_path'])
                if image:
                    tk.Label(result_frame, image=image).grid(row=0, rowspan=2, column=0, padx=5, pady=5)
            except Exception as e:
                logging.error(f"Error loading thumbnail: {e}")

        title_text = f"{movie['title']}"
        if movie.get('release_date'):
            title_text += f" ({movie['release_date'][:4]})"
        title_label = tk.Label(result_frame, text=title_text, anchor='w', justify='left')
        title_label.grid(row=0, column=1, sticky='w', padx=5)

        result_frame.bind('<Button-1>', lambda e, m=movie: self.show_preview(m))
        result_frame.bind('<Double-Button-1>', lambda e, m=movie: self.select_movie(m))

    def show_preview(self, movie):
        """Display selected movie details in preview panel"""
        self.preview_title.config(text=f"{movie['title']}\n({movie.get('release_date', 'N/A')})")

        if movie.get('poster_path'):
            try:
                image = self.search_gui._get_preview_image(movie['poster_path'])
                if image:
                    self.preview_poster.config(image=image)
                    self.preview_poster.image = image  # Keep reference
            except Exception as e:
                self.preview_poster.config(image='')
                logging.error(f"Error loading preview: {e}")

        self.preview_info.config(state='normal')
        self.preview_info.delete(1.0, tk.END)
        if movie.get('overview'):
            self.preview_info.insert(tk.END, movie['overview'])
        self.preview_info.config(state='disabled')

    def select_movie(self, movie=None):
        """Select a movie and update the main app"""
        if not movie and self.search_results:
            movie = self.search_results[0]  # Default to first movie

        if not movie:
            return

        try:
            details = TMDbAPI.get_movie_details(movie["id"])
            movie.update(details)
            self.search_gui.app.movie_manager.add_movie(Movie(**movie))
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to select movie: {str(e)}")
