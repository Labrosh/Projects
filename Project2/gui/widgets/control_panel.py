import tkinter as tk
from gui.color_scheme import ColorSchemeManager
from gui.widgets.about_dialog import AboutDialog

class ControlPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        button_style = {
            "font": (app.ui_settings["font_family"], app.ui_settings["font_size"]),
            "bg": app.ui_settings["button_color"],
            "fg": app.ui_settings["button_text_color"],
            "relief": tk.FLAT,
            "width": 15  # Fixed width for consistent appearance
        }

        # Create buttons - separate display text from shortcuts
        buttons = [
            ("Mark as Watched", self.app.movie_list_gui.mark_as_watched, "Move selected movie to watched list (Ctrl+W)"),
            ("Un-Watch", self.app.movie_list_gui.unwatch_movie, "Move selected movie back to watch list"),
            ("Remove Movie", self.app.movie_list_gui.remove_movie, "Remove selected movie from any list (Ctrl+R)"),
            ("View Details", self.app.show_selected_movie_details, "Show detailed information about selected movie (Ctrl+D)"),
            ("View Poster", self.app.show_selected_movie_poster, "Display movie poster in new window (Ctrl+P)"),
            ("Fetch Details", self.app.movie_list_gui.fetch_details, "Search TMDb to get movie details"),
            ("Settings", self.app.open_settings, "Configure application settings (Ctrl+,)"),
            ("About", self.show_about, "About Movie Tracker and credits")
        ]

        for text, command, tooltip in buttons:
            btn = tk.Button(self, text=text, command=command, **button_style)
            btn.pack(pady=5, padx=5, fill=tk.X, expand=True)
            ColorSchemeManager.setup_hover_animation(btn, app.ui_settings)
            btn.bind("<Enter>", lambda e, b=btn, t=tooltip: app.gui_helper.tooltip_manager.show_tooltip(b, t))
            btn.bind("<Leave>", app.gui_helper.tooltip_manager.hide_tooltip)

        ColorSchemeManager.apply_scheme(self, app.ui_settings)

    def show_about(self):
        """Show the about dialog"""
        AboutDialog(self)
