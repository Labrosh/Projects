import tkinter as tk
from tkinter import messagebox
import logging
from gui.color_scheme import ColorSchemeManager
from gui.widgets.thumbnail_listbox import ThumbnailListbox
from gui.widgets.rating_dialog import RatingDialog
from gui.widgets.bulk_import_dialog import BulkImportDialog
from models.movie import Movie  # Add this import

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
        
        # Add bulk import button
        button_frame = tk.Frame(filter_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Bulk Import", 
                 command=self._show_bulk_import).pack(side=tk.RIGHT)
        
        # Initial population of genre menu
        self.update_genre_menu()
        
        # Bind genre selection
        self.genre_var.trace('w', self._on_genre_filter)

        ColorSchemeManager.apply_scheme(self, app.ui_settings)
        self._setup_drag_drop()
        self._setup_context_menus()  # Add this line to initialize context menus

    def _on_genre_filter(self, *args):
        """Handle genre filter selection"""
        genre = self.genre_var.get()
        if (genre == "All Genres"):
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
        self.context_menu.add_command(label="Fetch Details", command=self._fetch_details)  # Add this
        self.context_menu.add_command(label="Rate Movie", command=self._rate_selected_movie)
        self.context_menu.add_command(label="Clear Ratings", command=self._clear_ratings)  # Add this line
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Mark as Watched", command=self.app.movie_list_gui.mark_as_watched)
        self.context_menu.add_command(label="Remove Movie", command=self.app.movie_list_gui.remove_movie)

        def show_context_menu(event, listbox):
            # Calculate which item was clicked using canvas coordinates
            y = listbox.canvasy(event.y)
            clicked_index = int(y // listbox.item_height)
            
            if 0 <= clicked_index < len(listbox.items):
                listbox.selected_index = clicked_index
                listbox._redraw()
                listbox.event_generate('<<ListboxSelect>>')
                self.context_menu.post(event.x_root, event.y_root)

        self.to_watch_listbox.bind("<Button-3>", lambda e: show_context_menu(e, self.to_watch_listbox))
        self.watched_listbox.bind("<Button-3>", lambda e: show_context_menu(e, self.watched_listbox))

    def _rate_selected_movie(self):
        """Show rating dialog for selected movie"""
        selected_movie = self.app.get_selected_movie()
        
        if not selected_movie:
            messagebox.showwarning("Warning", "Please select a movie to rate")
            return
            
        try:
            dialog = RatingDialog(self, selected_movie)
            self.wait_window(dialog)
            
            if dialog.result:
                # Add each rating from the dialog
                for rating in dialog.result:
                    selected_movie.add_rating(rating)
                
                # Refresh lists with movies from manager
                self.app.gui_helper.update_listbox(self.to_watch_listbox, self.app.movie_manager.movies_to_watch)
                self.app.gui_helper.update_listbox(self.watched_listbox, self.app.movie_manager.movies_watched)
                self.app.movie_manager.save_data()
                self.app.gui_helper.show_status(
                    f"Added {len(dialog.result)} ratings for {selected_movie.title}"
                )
                
        except Exception as e:
            logging.error(f"Error rating movie: {e}")
            messagebox.showerror("Error", f"Failed to add ratings: {str(e)}")

    def _clear_ratings(self):
        """Clear all ratings for the selected movie"""
        selected_movie = self.app.get_selected_movie()
        
        if not selected_movie:
            messagebox.showwarning("Warning", "Please select a movie to clear ratings")
            return
            
        if messagebox.askyesno("Confirm", f"Clear all ratings for {selected_movie.title}?"):
            try:
                selected_movie.clear_ratings()
                # Refresh lists
                self.app.gui_helper.update_listbox(self.to_watch_listbox, self.app.movie_manager.movies_to_watch)
                self.app.gui_helper.update_listbox(self.watched_listbox, self.app.movie_manager.movies_watched)
                self.app.movie_manager.save_data()
                self.app.gui_helper.show_status(f"Cleared ratings for {selected_movie.title}")
            except Exception as e:
                logging.error(f"Error clearing ratings: {e}")
                messagebox.showerror("Error", f"Failed to clear ratings: {str(e)}")

    def _show_bulk_import(self):
        """Show bulk import dialog"""
        dialog = BulkImportDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            added_count = 0
            skipped = []
            
            # Process each movie title
            for title in dialog.result:
                if title and title.strip():
                    clean_title = title.strip()
                    try:
                        # Create and add the movie
                        movie = Movie(title=clean_title)
                        movie.needs_details = True
                        if self.app.movie_manager.add_movie(movie):
                            added_count += 1
                        else:
                            skipped.append(title)
                    except Exception as e:
                        logging.error(f"Failed to add movie {title}: {e}")
                        skipped.append(f"{title} (Error)")
            
            # Update display
            self.app.movie_manager.save_data()
            self.app.gui_helper.update_listbox(self.to_watch_listbox, 
                                             self.app.movie_manager.movies_to_watch)
            
            # Show status
            status = f"Added {added_count} movies"
            if skipped:
                status += f" (skipped {len(skipped)} duplicates)"
            self.app.gui_helper.show_status(status)
            
            if skipped:
                messagebox.showinfo("Import Results", 
                    f"Added {added_count} movies\n\n" + 
                    f"Skipped {len(skipped)} movies:\n" + 
                    "\n".join(skipped[:5]) + 
                    ("\n..." if len(skipped) > 5 else ""))

    def _fetch_details(self):
        """Fetch TMDB details for selected movie"""
        selected_movie = self.app.get_selected_movie()
        if selected_movie and selected_movie.needs_details:
            # Show search dialog to find correct movie
            try:
                self.app.movie_search_gui.search_movie(selected_movie.title)
                self.app.gui_helper.update_listbox(self.to_watch_listbox, 
                                                 self.app.movie_manager.movies_to_watch)
                self.app.gui_helper.update_listbox(self.watched_listbox, 
                                                 self.app.movie_manager.movies_watched)
            except Exception as e:
                logging.error(f"Error fetching details: {e}")
                messagebox.showerror("Error", "Failed to fetch movie details")

    def _redraw_current_list(self):
        """Redraw the current listbox to show updated ratings"""
        current_genre = self.genre_var.get()
        self._on_genre_filter()
        self._on_genre_filter()

