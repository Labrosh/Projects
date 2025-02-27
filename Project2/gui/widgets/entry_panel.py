import tkinter as tk
from tkinter import messagebox  # Add this import
from gui.color_scheme import ColorSchemeManager

class EntryPanel(tk.Frame):
    def __init__(self, parent, movie_search_gui, movie_list_gui, ui_settings):
        super().__init__(parent, bg=ui_settings["background_color"])
        self.movie_search_gui = movie_search_gui
        self.movie_list_gui = movie_list_gui
        self.ui_settings = ui_settings
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        entry_style = {
            "font": (ui_settings["font_family"], ui_settings["font_size"]),
            "relief": tk.SOLID,
            "borderwidth": 1,
            "bg": ui_settings["entry_bg"],
            "fg": ui_settings["entry_fg"],
            "insertbackground": ui_settings["text_color"]
        }

        # Quick Add frame
        quick_add_frame = self._create_quick_add_frame(entry_style)
        quick_add_frame.grid(row=0, column=0, padx=5, sticky="ew")
        
        # TMDb Search frame
        tmdb_frame = self._create_tmdb_frame(entry_style)
        tmdb_frame.grid(row=0, column=1, padx=5, sticky="ew")

    def _create_quick_add_frame(self, entry_style):
        frame = tk.Frame(self, bg=self.ui_settings["background_color"])
        frame.grid_columnconfigure(1, weight=1)

        self.quick_add_btn = self._create_button(
            frame, 
            "Quick Add:", 
            lambda: self._handle_quick_add()
        )
        self.quick_add_btn.grid(row=0, column=0, padx=(0, 5))

        self.quick_add_entry = tk.Entry(frame, **entry_style)
        self.quick_add_entry.grid(row=0, column=1, sticky="ew")
        self.quick_add_entry.bind('<Return>', lambda e: self._handle_quick_add())

        return frame

    def _handle_quick_add(self):
        """Handle quick add functionality"""
        title = self.quick_add_entry.get().strip()
        if title:
            self.movie_list_gui.add_movie_to_watchlist(title)
            self.quick_add_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    def _create_tmdb_frame(self, entry_style):
        frame = tk.Frame(self, bg=self.ui_settings["background_color"])
        frame.grid_columnconfigure(1, weight=1)

        self.tmdb_btn = self._create_button(
            frame, 
            "TMDb Search:", 
            lambda: self._perform_search()
        )
        self.tmdb_btn.grid(row=0, column=0, padx=(0, 5))

        self.search_entry = tk.Entry(frame, **entry_style)
        self.search_entry.grid(row=0, column=1, sticky="ew")
        self.search_entry.bind('<Return>', lambda e: self._perform_search())

        return frame

    def _perform_search(self):
        search_text = self.search_entry.get().strip()
        if search_text:
            self.movie_search_gui.search_movie(search_text)
            self.search_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a movie title!")

    def _create_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.ui_settings["button_color"],
            fg=self.ui_settings["button_text_color"],
            font=(self.ui_settings["font_family"], self.ui_settings["font_size"]),
            relief=tk.FLAT,
            padx=10
        )
        ColorSchemeManager.setup_hover_animation(btn, self.ui_settings)
        return btn
