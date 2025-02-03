import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import logging
from gui.theme import ThemeManager

class GUIHelper:
    def __init__(self, app):
        self.app = app

    def update_listbox(self, listbox, items):
        logging.debug(f"Updating listbox with {len(items)} items")
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, item.title)
        listbox.update()  # Force update

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def show_movie_poster(self, movie):
        poster_path = movie.get_poster_path()
        if poster_path:
            if not poster_path.startswith("http"):
                poster_path = os.path.join("data/posters", os.path.basename(poster_path))
            if os.path.exists(poster_path):
                poster_window = ThemeManager.create_themed_toplevel(self.app.root, self.app.ui_settings)
                poster_window.title(movie.title)
                poster_image = Image.open(poster_path)
                poster_image = poster_image.resize((300, 450), Image.LANCZOS)
                poster_photo = ImageTk.PhotoImage(poster_image)
                poster_label = tk.Label(poster_window, image=poster_photo)
                poster_label.image = poster_photo
                poster_label.pack(padx=10, pady=10)
                ThemeManager.apply_theme(poster_window, self.app.ui_settings)
                self.center_window(poster_window)  # Center the window
            else:
                messagebox.showwarning("Warning", "Poster not found.")

    def show_movie_details(self, movie):
        details = movie.details
        if details:
            details_window = ThemeManager.create_themed_toplevel(self.app.root, self.app.ui_settings)
            details_window.title(movie.title)

            details_text = tk.Text(details_window, wrap=tk.WORD)
            details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            formatted_details = f"""
Title: {details.get('title', 'N/A')}
Release Date: {details.get('release_date', 'N/A')}
Genres: {', '.join([genre['name'] for genre in details.get('genres', [])])}
Overview: {details.get('overview', 'N/A')}
Runtime: {details.get('runtime', 'N/A')} minutes
Rating: {details.get('vote_average', 'N/A')} ({details.get('vote_count', 'N/A')} votes)
Homepage: {details.get('homepage', 'N/A')}
            """

            details_text.insert(tk.END, formatted_details)
            details_text.configure(state='disabled')  # Make read-only
            ThemeManager.apply_theme(details_window, self.app.ui_settings)
            self.center_window(details_window)  # Center the window
        else:
            messagebox.showwarning("Warning", "Details not found.")

    def create_widgets(self):
        # Configure root window style
        ThemeManager.apply_theme(self.app.root, self.app.ui_settings)
        
        # Make the root window responsive
        self.app.root.grid_rowconfigure(0, weight=1)
        self.app.root.grid_columnconfigure(0, weight=1)
        
        # Main container
        main_frame = tk.Frame(self.app.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)  # Make center column expand
        main_frame.grid_rowconfigure(0, weight=1)     # Make row expand
        ThemeManager.apply_theme(main_frame, self.app.ui_settings)

        # Left panel for buttons
        left_panel = tk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky="ns", padx=10)
        ThemeManager.apply_theme(left_panel, self.app.ui_settings)
        logging.debug("Applied theme to left_panel")

        # Center panel for lists
        center_panel = tk.Frame(main_frame)
        center_panel.grid(row=0, column=1, sticky="nsew")
        center_panel.grid_columnconfigure(0, weight=1)  # Make lists expand horizontally
        center_panel.grid_rowconfigure(1, weight=1)     # Make to_watch list expand
        center_panel.grid_rowconfigure(3, weight=1)     # Make watched list expand
        ThemeManager.apply_theme(center_panel, self.app.ui_settings)

        # Title styling
        title_style = {
            "font": (self.app.ui_settings["font_family"], self.app.ui_settings["font_size"] + 4, "bold"),
            "fg": self.app.ui_settings["title_color"],
            "bg": self.app.ui_settings["background_color"]
        }
        
        # Listbox styling
        listbox_style = {
            "font": (self.app.ui_settings["font_family"], self.app.ui_settings["font_size"]),
            "selectmode": tk.SINGLE,
            "relief": tk.FLAT,                                    # Flatter appearance
            "borderwidth": 0,                                     # Remove border
            "bg": self.app.ui_settings["listbox_bg"],
            "fg": self.app.ui_settings["listbox_fg"],
            "selectbackground": self.app.ui_settings["selection_bg"],  # New selection color
            "selectforeground": self.app.ui_settings["selection_fg"],  # New selection text color
            "activestyle": "none"                                # Remove dotted line around selected item
        }

        # Entry styling
        entry_style = {
            "font": (self.app.ui_settings["font_family"], self.app.ui_settings["font_size"]),
            "relief": tk.SOLID,
            "borderwidth": 1,
            "bg": self.app.ui_settings["entry_bg"],
            "fg": self.app.ui_settings["entry_fg"],
            "insertbackground": self.app.ui_settings["text_color"]  # Cursor color
        }

        # Button styling
        button_style = {
            "font": (self.app.ui_settings["font_family"], self.app.ui_settings["font_size"]),
            "bg": self.app.ui_settings["button_color"],
            "fg": self.app.ui_settings["button_text_color"],
            "relief": tk.FLAT,
            "width": self.app.ui_settings["button_width"]
        }

        # Add controls to left panel with app reference
        for i, (text, command) in enumerate([
            ("Add Movie", lambda: self.app.movie_list_gui.add_movie()),
            ("Search Movie", lambda: self.app.movie_search_gui.search_movie()),
            ("Mark as Watched", self.app.movie_list_gui.mark_as_watched),
            ("Un-Watch", self.app.movie_list_gui.unwatch_movie),
            ("Remove Movie", self.app.movie_list_gui.remove_movie),
            ("View Details", self.app.show_selected_movie_details),
            ("View Poster", self.app.show_selected_movie_poster),
            ("Settings", self.app.open_settings)
        ]):
            btn = tk.Button(left_panel, text=text, command=command, **button_style)
            btn.pack(pady=5, padx=5, fill=tk.X, expand=True)
            btn.app = self.app
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_hover_leave(b))
            logging.debug(f"Applied theme to button: {text}")

        # Center panel content
        self.app.label_to_watch = tk.Label(center_panel, text="Movies to Watch", **title_style)
        self.app.label_to_watch.grid(row=0, column=0, pady=5, sticky="ew")

        self.app.to_watch_listbox = tk.Listbox(center_panel, **listbox_style)
        self.app.to_watch_listbox.grid(row=1, column=0, pady=5, sticky="nsew")

        self.app.label_watched = tk.Label(center_panel, text="Movies Watched", **title_style)
        self.app.label_watched.grid(row=2, column=0, pady=5, sticky="ew")

        self.app.watched_listbox = tk.Listbox(center_panel, **listbox_style)
        self.app.watched_listbox.grid(row=3, column=0, pady=5, sticky="nsew")

        # Entry fields at the bottom of center panel - replace the existing entry_frame section with this:
        entry_frame = tk.Frame(center_panel, bg=self.app.ui_settings["background_color"])
        entry_frame.grid(row=4, column=0, pady=10, sticky="ew")
        entry_frame.grid_columnconfigure(0, weight=1)
        entry_frame.grid_columnconfigure(1, weight=1)

        # Quick Add frame (left side)
        quick_add_frame = tk.Frame(entry_frame, bg=self.app.ui_settings["background_color"])
        quick_add_frame.grid(row=0, column=0, padx=5, sticky="ew")
        quick_add_frame.grid_columnconfigure(1, weight=1)

        quick_add_label = tk.Label(
            quick_add_frame, 
            text="Quick Add:", 
            fg=self.app.ui_settings["text_color"],
            bg=self.app.ui_settings["background_color"],
            font=(self.app.ui_settings["font_family"], self.app.ui_settings["font_size"])
        )
        quick_add_label.grid(row=0, column=0, padx=(0, 5))

        self.app.movie_entry = tk.Entry(quick_add_frame, **entry_style)
        self.app.movie_entry.grid(row=0, column=1, sticky="ew")
        self.app.movie_entry.app = self.app  # Add app reference

        # TMDb Search frame (right side)
        tmdb_frame = tk.Frame(entry_frame, bg=self.app.ui_settings["background_color"])
        tmdb_frame.grid(row=0, column=1, padx=5, sticky="ew")
        tmdb_frame.grid_columnconfigure(1, weight=1)

        tmdb_label = tk.Label(
            tmdb_frame, 
            text="TMDb Search:", 
            fg=self.app.ui_settings["text_color"],
            bg=self.app.ui_settings["background_color"],
            font=(self.app.ui_settings["font_family"], self.app.ui_settings["font_size"])
        )
        tmdb_label.grid(row=0, column=0, padx=(0, 5))

        self.app.search_entry = tk.Entry(tmdb_frame, **entry_style)
        self.app.search_entry.grid(row=0, column=1, sticky="ew")
        self.app.search_entry.app = self.app  # Add app reference

        # Add tooltips
        self.app.movie_entry.bind("<Enter>", lambda e: self.show_tooltip(self.app.movie_entry, "Quickly add a movie without TMDb details"))
        self.app.search_entry.bind("<Enter>", lambda e: self.show_tooltip(self.app.search_entry, "Search TMDb for movie details and poster"))
        self.app.movie_entry.bind("<Leave>", self.hide_tooltip)
        self.app.search_entry.bind("<Leave>", self.hide_tooltip)

        # Apply theme to everything at once
        ThemeManager.apply_theme(main_frame, self.app.ui_settings)

        # Set up hover animations for all buttons
        for widget in main_frame.winfo_children():
            if isinstance(widget, tk.Button):
                ThemeManager.setup_hover_animation(widget, self.app.ui_settings)

    def on_hover_enter(self, button):
        """Lighten button color on hover"""
        button.configure(bg=button.app.ui_settings["button_hover_color"])

    def on_hover_leave(self, button):
        """Restore original button color"""
        button.configure(bg=button.app.ui_settings["button_color"])

    def open_settings(self):
        settings_window = ThemeManager.create_themed_toplevel(self.app.root, self.app.ui_settings, "Settings")
        settings_window.geometry("600x800")  # Larger initial size
        
        # Make the settings window responsive
        settings_window.grid_rowconfigure(0, weight=1)
        settings_window.grid_columnconfigure(0, weight=1)

        # Main container frame
        main_frame = tk.Frame(settings_window, bg=self.app.ui_settings["background_color"])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        # Theme selection frame
        theme_frame = tk.LabelFrame(main_frame, text="Theme Selection", 
                                  bg=self.app.ui_settings["background_color"],
                                  fg=self.app.ui_settings["text_color"])
        theme_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        theme_frame.grid_columnconfigure(0, weight=1)

        theme_var = tk.StringVar(value=self.app.ui_settings.get("current_theme", "Dark Purple"))
        for theme in self.app.settings_manager.get_available_themes():
            rb = tk.Radiobutton(
                theme_frame, 
                text=theme,
                variable=theme_var,
                value=theme,
                bg=self.app.ui_settings["background_color"],
                fg=self.app.ui_settings["text_color"],
                selectcolor=self.app.ui_settings["button_color"],
                activebackground=self.app.ui_settings["background_color"],
                activeforeground=self.app.ui_settings["text_color"]
            )
            rb.pack(anchor=tk.W, padx=20, pady=5)

        # Settings frame
        settings_frame = tk.LabelFrame(main_frame, text="Application Settings",
                                     bg=self.app.ui_settings["background_color"],
                                     fg=self.app.ui_settings["text_color"])
        settings_frame.grid(row=1, column=0, sticky="ew")
        settings_frame.grid_columnconfigure(1, weight=1)

        # Helper function to create setting rows
        def create_setting_row(parent, label_text, default_value, row):
            tk.Label(parent, text=label_text,
                    bg=self.app.ui_settings["background_color"],
                    fg=self.app.ui_settings["text_color"]).grid(row=row, column=0, 
                                                         sticky="w", padx=20, pady=10)
            entry = tk.Entry(parent,
                            bg=self.app.ui_settings["entry_bg"],
                            fg=self.app.ui_settings["entry_fg"],
                            insertbackground=self.app.ui_settings["text_color"])
            entry.insert(0, str(default_value))
            entry.grid(row=row, column=1, sticky="ew", padx=20)
            return entry

        # Create settings entries
        settings_entries = {
            "font_size": create_setting_row(settings_frame, "Font Size:", 
                                          self.app.ui_settings["font_size"], 0),
            "element_spacing": create_setting_row(settings_frame, "Element Spacing:", 
                                               self.app.ui_settings["element_spacing"], 1),
            "listbox_height": create_setting_row(settings_frame, "Listbox Height:", 
                                              self.app.ui_settings["listbox_height"], 2),
            "listbox_width": create_setting_row(settings_frame, "Listbox Width:", 
                                             self.app.ui_settings["listbox_width"], 3),
            "window_width": create_setting_row(settings_frame, "Window Width:", 
                                            self.app.ui_settings["window_width"], 4),
            "window_height": create_setting_row(settings_frame, "Window Height:", 
                                             self.app.ui_settings["window_height"], 5)
        }

        def save_settings():
            try:
                new_settings = {
                    "current_theme": theme_var.get(),
                    "font_size": int(settings_entries["font_size"].get()),
                    "element_spacing": int(settings_entries["element_spacing"].get()),
                    "listbox_height": int(settings_entries["listbox_height"].get()),
                    "listbox_width": int(settings_entries["listbox_width"].get()),
                    "window_width": int(settings_entries["window_width"].get()),
                    "window_height": int(settings_entries["window_height"].get())
                }
                self.app.settings_manager.update_settings(new_settings)
                self.app.update_ui()
                ThemeManager.apply_theme(self.app.root, self.app.settings_manager.ui_settings)
                settings_window.destroy()
                messagebox.showinfo("Settings", "Settings have been updated.")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for all settings.")

        # Save button at the bottom
        save_button = tk.Button(main_frame, text="Save Settings",
                              command=save_settings,
                              bg=self.app.ui_settings["button_color"],
                              fg=self.app.ui_settings["button_text_color"])
        save_button.grid(row=2, column=0, pady=20, sticky="ew")

        # Apply theme to all widgets
        ThemeManager.apply_theme(settings_window, self.app.ui_settings)
        self.center_window(settings_window)  # Center the window

    def show_tooltip(self, widget, text):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20

        # Create a toplevel window with theme
        tooltip = ThemeManager.create_themed_toplevel(widget, self.app.ui_settings)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tooltip, text=text, justify=tk.LEFT,
                         relief=tk.SOLID, borderwidth=1,
                         font=("Helvetica", "10", "normal"))
        label.pack()
        
        ThemeManager.apply_theme(tooltip, self.app.ui_settings)
        widget.tooltip = tooltip

    def hide_tooltip(self, event):
        widget = event.widget
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
            widget.tooltip = None
