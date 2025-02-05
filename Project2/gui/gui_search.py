import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import logging
from io import BytesIO
from api.tmdb_api import TMDbAPI
from models.movie import Movie
from gui.color_scheme import ColorSchemeManager

class MovieSearchGUI:
    def __init__(self, root, movie_manager):
        self.root = root
        self.movie_manager = movie_manager
        self.search_results = []
        self.temp_images = {}  # Store thumbnail images while window is open

    def search_movie(self, title=None):
        """Search for a movie using provided title"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Movies")
        search_window.geometry("1000x600")
        search_window.transient(self.root)
        search_window.grab_set()

        # Split into left and right panes
        left_frame = tk.Frame(search_window)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        right_frame = tk.Frame(search_window)
        right_frame.pack(side='right', fill='both', padx=5, pady=5)

        # Search controls
        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill='x', pady=5)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Use the provided title for search
        if title and title.strip():
            search_entry.insert(0, title.strip())
            search_window.after(100, lambda: perform_search())

        # Results area
        results_frame = tk.Frame(left_frame)
        results_frame.pack(fill='both', expand=True, pady=5)

        # Create canvas for scrollable results
        canvas = tk.Canvas(results_frame)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Preview area
        preview_label = tk.Label(right_frame, text="Movie Preview", font=('Helvetica', 12, 'bold'))
        preview_label.pack(pady=5)
        
        preview_poster = tk.Label(right_frame)
        preview_poster.pack(pady=5)
        
        preview_info = tk.Text(right_frame, wrap='word', height=10, width=40)
        preview_info.pack(pady=5, padx=5, fill='both', expand=True)

        def load_thumbnail(url):
            """Load a thumbnail from URL"""
            if not url:
                return None
            try:
                response = requests.get(f"https://image.tmdb.org/t/p/w92{url}")
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((92, 138))  # Maintain aspect ratio
                    return ImageTk.PhotoImage(img)
            except Exception as e:
                logging.error(f"Error loading thumbnail: {e}")
            return None

        def perform_search():
            # Clear previous results
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            self.temp_images.clear()

            query = search_entry.get().strip()
            if not query:
                messagebox.showwarning("Warning", "Please enter a movie title!")
                return

            try:
                results = TMDbAPI.search_movie(query)
                self.search_results = results

                if not results:
                    tk.Label(scrollable_frame, text="No results found").pack(pady=10)
                    return

                for movie in results:
                    # Create frame for result
                    result_frame = tk.Frame(scrollable_frame, relief='groove', bd=1)
                    result_frame.pack(fill='x', pady=2, padx=5)
                    
                    # Make the frame focusable
                    result_frame.configure(takefocus=1)
                    
                    # Load thumbnail if available
                    if movie.get('poster_path'):
                        img = load_thumbnail(movie['poster_path'])
                        if img:
                            self.temp_images[movie['id']] = img
                            tk.Label(result_frame, image=img).pack(side='left', padx=5, pady=5)
                    
                    # Add movie info
                    info_frame = tk.Frame(result_frame)
                    info_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
                    
                    title = movie['title']
                    if movie.get('release_date'):
                        title += f" ({movie['release_date'][:4]})"
                    label = tk.Label(info_frame, text=title, anchor='w', justify='left')
                    label.pack(fill='x')
                    
                    # Bind clicks to all widgets in the frame
                    for widget in [result_frame, info_frame, label]:
                        widget.bind('<Button-1>', lambda e, m=movie: show_preview(m))
                        widget.bind('<Double-Button-1>', lambda e, m=movie: select_and_close(m))

            except Exception as e:
                logging.error(f"Search error: {e}")
                messagebox.showerror("Error", "Failed to search movies")

        def show_preview(movie):
            preview_info.config(state='normal')
            preview_info.delete(1.0, tk.END)
            
            # Show title and year
            title = movie['title']
            if movie.get('release_date'):
                title += f" ({movie['release_date'][:4]})"
            preview_info.insert(tk.END, f"{title}\n\n")
            
            # Show overview
            if movie.get('overview'):
                preview_info.insert(tk.END, movie['overview'])
            
            preview_info.config(state='disabled')
            
            # Show poster if available
            if movie.get('poster_path'):
                img = load_thumbnail(movie['poster_path'])
                if img:
                    preview_poster.config(image=img)
                    preview_poster.image = img

        def select_and_close(movie_data):
            """Handle selection and window closing in one function"""
            try:
                # Get full details
                details = TMDbAPI.get_movie_details(movie_data["id"])
                if details:
                    movie_data.update(details)
                
                new_movie = Movie(
                    id=movie_data["id"],
                    title=movie_data["title"],
                    release_date=movie_data.get("release_date"),
                    poster_path=movie_data.get("poster_path"),
                    details=movie_data
                )
                new_movie.save_poster()
                self.movie_manager.add_movie(new_movie)
                
                # Force a refresh of the main window's movie list
                self.root.after(100, lambda: self.root.event_generate("<<RefreshMovieList>>"))
                
                search_window.destroy()
                return True

            except Exception as e:
                logging.error(f"Error selecting movie: {e}")
                messagebox.showerror("Error", "Failed to get movie details")
            return False

        def refresh_movie_list():
            # Implement this method to refresh the movie list in the main GUI
            pass

        # Pack scrolling components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add search button
        tk.Button(search_frame, text="Search", command=perform_search).pack(side='right', padx=5)
        
        # Update the Select Movie button to use select_and_close with the current selection
        select_button = tk.Button(search_window, text="Select Movie", 
                                command=lambda: next(
                                    (select_and_close(m) for m in self.search_results 
                                     if m.get('title') == preview_info.get("1.0", "end-3c").split("\n")[0].rsplit(" (", 1)[0]),
                                    None))
        select_button.pack(pady=10)
        
        # Bind enter key to search
        search_entry.bind('<Return>', lambda e: perform_search())
        
        # Do initial search if title provided
        if title:
            perform_search()

        # Clean up on window close
        search_window.protocol("WM_DELETE_WINDOW", lambda: [search_window.destroy(), self.temp_images.clear()])
