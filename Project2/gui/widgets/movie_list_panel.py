import tkinter as tk
from gui.color_scheme import ColorSchemeManager
from gui.widgets.thumbnail_listbox import ThumbnailListbox  # Import the new widget

class MovieListPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Now we have access to all app components through self.app
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create widgets
        title_style = {
            "font": (app.ui_settings["font_family"], app.ui_settings["font_size"] + 4, "bold"),
            "fg": app.ui_settings["title_color"],
            "bg": app.ui_settings["background_color"]
        }
        
        listbox_style = {
            "font": (app.ui_settings["font_family"], app.ui_settings["font_size"]),
            "selectmode": tk.SINGLE,
            "relief": tk.FLAT,
            "borderwidth": 0,
            "bg": app.ui_settings["listbox_bg"],
            "fg": app.ui_settings["listbox_fg"],
            "selectbackground": app.ui_settings["selection_bg"],
            "selectforeground": app.ui_settings["selection_fg"],
            "activestyle": "none"
        }

        # Create and grid widgets
        self.label_to_watch = tk.Label(self, text="Movies to Watch", **title_style)
        self.label_to_watch.grid(row=0, column=0, pady=5, sticky="ew")

        # Create listbox with scrollbar for to-watch
        to_watch_frame = tk.Frame(self)
        to_watch_frame.grid(row=1, column=0, pady=5, sticky="nsew")
        to_watch_frame.grid_columnconfigure(0, weight=1)
        to_watch_frame.grid_rowconfigure(0, weight=1)

        self.to_watch_listbox = ThumbnailListbox(to_watch_frame, **listbox_style)  # Use ThumbnailListbox
        self.to_watch_listbox.grid(row=0, column=0, sticky="nsew")
        to_watch_scrollbar = tk.Scrollbar(to_watch_frame, orient="vertical")
        to_watch_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.to_watch_listbox.config(yscrollcommand=to_watch_scrollbar.set)
        to_watch_scrollbar.config(command=self.to_watch_listbox.yview)

        self.label_watched = tk.Label(self, text="Movies Watched", **title_style)
        self.label_watched.grid(row=2, column=0, pady=5, sticky="ew")

        # Create listbox with scrollbar for watched
        watched_frame = tk.Frame(self)
        watched_frame.grid(row=3, column=0, pady=5, sticky="nsew")
        watched_frame.grid_columnconfigure(0, weight=1)
        watched_frame.grid_rowconfigure(0, weight=1)

        self.watched_listbox = ThumbnailListbox(watched_frame, **listbox_style)  # Use ThumbnailListbox
        self.watched_listbox.grid(row=0, column=0, sticky="nsew")
        watched_scrollbar = tk.Scrollbar(watched_frame, orient="vertical")
        watched_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.watched_listbox.config(yscrollcommand=watched_scrollbar.set)
        watched_scrollbar.config(command=self.watched_listbox.yview)

        # Add genre filter with proper initialization
        self.genre_var = tk.StringVar()
        self.genre_var.set("All Genres")
        
        filter_frame = tk.Frame(self)
        filter_frame.grid(row=4, column=0, pady=5, sticky="ew")
        
        tk.Label(filter_frame, text="Filter by genre:", **title_style).pack(side=tk.LEFT, padx=5)
        self.genre_menu = tk.OptionMenu(filter_frame, self.genre_var, "All Genres")
        self.genre_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Initial population of genre menu
        self.update_genre_menu()
        
        # Bind genre selection
        self.genre_var.trace('w', self._on_genre_filter)

        ColorSchemeManager.apply_scheme(self, app.ui_settings)
        self._setup_drag_drop()

    def _on_genre_filter(self, *args):
        """Handle genre filter selection"""
        genre = self.genre_var.get()
        if genre == "All Genres":
            # Show all movies
            self.app.gui_helper.update_listbox(self.to_watch_listbox, self.app.movie_manager.movies_to_watch)
            self.app.gui_helper.update_listbox(self.watched_listbox, self.app.movie_manager.movies_watched)
        else:
            # Filter both listboxes by selected genre
            to_watch_filtered = [movie for movie in self.app.movie_manager.movies_to_watch
                               if any(g['name'] == genre for g in movie.details.get('genres', []))]
            watched_filtered = [movie for movie in self.app.movie_manager.movies_watched
                              if any(g['name'] == genre for g in movie.details.get('genres', []))]
            
            self.app.gui_helper.update_listbox(self.to_watch_listbox, to_watch_filtered)
            self.app.gui_helper.update_listbox(self.watched_listbox, watched_filtered)

    def update_genre_menu(self):
        """Update genre menu with all available genres"""
        genres = set()
        all_movies = self.app.movie_manager.movies_to_watch + self.app.movie_manager.movies_watched
        
        for movie in all_movies:
            if hasattr(movie, 'details') and movie.details:
                for genre in movie.details.get('genres', []):
                    genres.add(genre['name'])
        
        # Update menu
        menu = self.genre_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="All Genres", 
                        command=lambda: self.genre_var.set("All Genres"))
        
        for genre in sorted(genres):
            menu.add_command(label=genre, 
                           command=lambda g=genre: self.genre_var.set(g))

    def _setup_drag_drop(self):
        # Remove single-click bindings for drag-drop
        # Add double-click bindings for moving items
        def on_double_click(event, from_list, to_list):
            sel = from_list.curselection()
            if sel:
                movie = from_list.items[sel[0]]
                if from_list == self.to_watch_listbox:
                    self.app.movie_manager.mark_as_watched(movie)
                else:
                    self.app.movie_manager.unwatch_movie(movie)
                
                # Update the listboxes
                self.app.gui_helper.update_listbox(self.to_watch_listbox, self.app.movie_manager.movies_to_watch)
                self.app.gui_helper.update_listbox(self.watched_listbox, self.app.movie_manager.movies_watched)
                
                # Update genre menu after moving movies
                self.update_genre_menu()

        # Bind double-click events
        self.to_watch_listbox.bind('<Double-Button-1>', 
            lambda e: on_double_click(e, self.to_watch_listbox, self.watched_listbox))
        self.watched_listbox.bind('<Double-Button-1>', 
            lambda e: on_double_click(e, self.watched_listbox, self.to_watch_listbox))

        # Ensure selection event is handled
        self.to_watch_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.watched_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

    def on_listbox_select(self, event):
        """Handle listbox selection event"""
        selected_movie = self.app.get_selected_movie()
        if selected_movie:
            # Perform any additional actions needed when a movie is selected
            pass

    def _setup_context_menus(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.app.show_selected_movie_details)
        self.context_menu.add_command(label="View Poster", command=self.app.show_selected_movie_poster)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Mark as Watched", command=self.app.movie_list_gui.mark_as_watched)
        self.context_menu.add_command(label="Remove Movie", command=self.app.movie_list_gui.remove_movie)

        def show_context_menu(event, listbox):
            item = listbox.identify_row(event.y)
            if item:
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(item)
                self.context_menu.post(event.x_root, event.y_root)

        self.to_watch_listbox.bind("<Button-3>", lambda e: show_context_menu(e, self.to_watch_listbox))
        self.watched_listbox.bind("<Button-3>", lambda e: show_context_menu(e, self.watched_listbox))
