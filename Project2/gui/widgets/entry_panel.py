import tkinter as tk
from gui.color_scheme import ColorSchemeManager

class EntryPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.ui_settings["background_color"])
        self.app = app
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        entry_style = {
            "font": (app.ui_settings["font_family"], app.ui_settings["font_size"]),
            "relief": tk.SOLID,
            "borderwidth": 1,
            "bg": app.ui_settings["entry_bg"],
            "fg": app.ui_settings["entry_fg"],
            "insertbackground": app.ui_settings["text_color"]
        }

        # Quick Add frame
        quick_add_frame = self._create_quick_add_frame(entry_style)
        quick_add_frame.grid(row=0, column=0, padx=5, sticky="ew")
        
        # TMDb Search frame
        tmdb_frame = self._create_tmdb_frame(entry_style)
        tmdb_frame.grid(row=0, column=1, padx=5, sticky="ew")

    def _create_quick_add_frame(self, entry_style):
        frame = tk.Frame(self, bg=self.app.ui_settings["background_color"])
        frame.grid_columnconfigure(1, weight=1)

        self.quick_add_btn = self._create_button(
            frame, 
            "Quick Add:", 
            lambda: self.app.movie_list_gui.add_movie()
        )
        self.quick_add_btn.grid(row=0, column=0, padx=(0, 5))

        self.quick_add_entry = tk.Entry(frame, **entry_style)
        self.quick_add_entry.grid(row=0, column=1, sticky="ew")
        self.quick_add_entry.bind('<Return>', lambda e: self.app.movie_list_gui.add_movie())

        return frame

    def _create_tmdb_frame(self, entry_style):
        frame = tk.Frame(self, bg=self.app.ui_settings["background_color"])
        frame.grid_columnconfigure(1, weight=1)

        self.tmdb_btn = self._create_button(
            frame, 
            "TMDb Search:", 
            lambda: self.app.movie_search_gui.search_movie()
        )
        self.tmdb_btn.grid(row=0, column=0, padx=(0, 5))

        self.search_entry = tk.Entry(frame, **entry_style)
        self.search_entry.grid(row=0, column=1, sticky="ew")
        self.search_entry.bind('<Return>', lambda e: self.app.movie_search_gui.search_movie())

        return frame

    def _create_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.app.ui_settings["button_color"],
            fg=self.app.ui_settings["button_text_color"],
            font=(self.app.ui_settings["font_family"], self.app.ui_settings["font_size"]),
            relief=tk.FLAT,
            padx=10
        )
        ColorSchemeManager.setup_hover_animation(btn, self.app.ui_settings)
        return btn
