import tkinter as tk
from tkinter import ttk

class Theme:
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

    def apply(self, widget):
        """Apply theme to widget and all its children"""
        if not widget:
            return

        # Configure root and Toplevel windows first
        if isinstance(widget, (tk.Tk, tk.Toplevel)):
            widget.configure(bg=self.colors["background_color"])
            widget.option_add("*Background", self.colors["background_color"])
            widget.option_add("*Foreground", self.colors["text_color"])
            widget.option_add("*selectBackground", self.colors["selection_bg"])
            widget.option_add("*selectForeground", self.colors["selection_fg"])

        # Configure the widget itself
        if isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget.configure(
                bg=self.colors["background_color"],
                highlightthickness=0,
                bd=0
            )
        elif isinstance(widget, tk.Label):
            widget.configure(
                bg=self.colors["background_color"],
                fg=self.colors["text_color"],
                highlightthickness=0
            )
        elif isinstance(widget, tk.Button):
            widget.configure(
                bg=self.colors["button_color"],
                fg=self.colors["button_text_color"],
                activebackground=self.colors["button_hover_color"],
                activeforeground=self.colors["button_text_color"],
                relief=tk.FLAT,
                borderwidth=0,
                highlightthickness=0
            )
        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=self.colors["entry_bg"],
                fg=self.colors["entry_fg"],
                insertbackground=self.colors["text_color"],
                relief=tk.FLAT,
                highlightthickness=1,
                highlightcolor=self.colors["button_color"],
                highlightbackground=self.colors["secondary_bg"],
                selectbackground=self.colors["selection_bg"],
                selectforeground=self.colors["selection_fg"]
            )
        elif isinstance(widget, tk.Listbox):
            widget.configure(
                bg=self.colors["listbox_bg"],
                fg=self.colors["listbox_fg"],
                selectbackground=self.colors["selection_bg"],
                selectforeground=self.colors["selection_fg"],
                relief=tk.FLAT,
                borderwidth=0,
                highlightthickness=1,
                highlightcolor=self.colors["button_color"],
                highlightbackground=self.colors["secondary_bg"],
                activestyle="none"
            )
        elif isinstance(widget, tk.Text):
            widget.configure(
                bg=self.colors["listbox_bg"],
                fg=self.colors["listbox_fg"],
                insertbackground=self.colors["text_color"],
                relief=tk.FLAT,
                borderwidth=0,
                highlightthickness=1,
                highlightcolor=self.colors["button_color"],
                highlightbackground=self.colors["secondary_bg"],
                selectbackground=self.colors["selection_bg"],
                selectforeground=self.colors["selection_fg"]
            )

        # Configure scrollbars if they exist
        if hasattr(widget, 'yview'):
            parent = widget.master
            parent.grid_columnconfigure(0, weight=1)
            parent.grid_columnconfigure(1, weight=0)
            
            style = ttk.Style()
            style.configure(
                "Custom.Vertical.TScrollbar",
                background=self.colors["button_color"],
                troughcolor=self.colors["background_color"],
                borderwidth=0,
                arrowcolor=self.colors["text_color"]
            )
            
            scrollbar = ttk.Scrollbar(
                parent,
                style="Custom.Vertical.TScrollbar",
                command=widget.yview
            )
            if 'row' in widget.grid_info():
                scrollbar.grid(row=widget.grid_info()['row'], column=1, sticky="ns")
                widget.configure(yscrollcommand=scrollbar.set)

        # Apply theme to all children
        for child in widget.winfo_children():
            self.apply(child)

        # Force update
        widget.update_idletasks()

    def setup_hover_animation(self, button):
        """Create smooth hover animation for buttons"""
        def on_enter(e):
            button.configure(bg=self.colors["button_hover_color"])
        
        def on_leave(e):
            button.configure(bg=self.colors["button_color"])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

class ThemeManager:
    THEMES = {
        "Dark Purple": Theme("Dark Purple", {
            "background_color": "#1E1E2E",
            "secondary_bg": "#2A2A3C",
            "button_color": "#45458C",
            "button_hover_color": "#565699",
            "button_text_color": "#E1E1F2",
            "text_color": "#D1D1E0",
            "title_color": "#9D7CD8",
            "listbox_bg": "#2A2A3C",
            "listbox_fg": "#D1D1E0",
            "entry_bg": "#2A2A3C",
            "entry_fg": "#D1D1E0",
            "selection_bg": "#565699",
            "selection_fg": "#FFFFFF",
        }),
        "True Dark": Theme("True Dark", {
            "background_color": "#0A0A0A",
            "secondary_bg": "#1A1A1A",
            "button_color": "#2A2A2A",
            "button_hover_color": "#404040",
            "button_text_color": "#D0D0D0",
            "text_color": "#C0C0C0",
            "title_color": "#9B6BFF",
            "listbox_bg": "#1A1A1A",
            "listbox_fg": "#D0D0D0",
            "entry_bg": "#1A1A1A",
            "entry_fg": "#D0D0D0",
            "selection_bg": "#404040",
            "selection_fg": "#FFFFFF",
        }),
        "Cyberpunk": Theme("Cyberpunk", {
            "background_color": "#0C0C14",
            "secondary_bg": "#1A1A2E",
            "button_color": "#FF0055",
            "button_hover_color": "#FF3377",
            "button_text_color": "#00FFFF",
            "text_color": "#00FF9F",
            "title_color": "#FF00FF",
            "listbox_bg": "#1A1A2E",
            "listbox_fg": "#00FF9F",
            "entry_bg": "#1A1A2E",
            "entry_fg": "#00FFFF",
            "selection_bg": "#FF0055",
            "selection_fg": "#00FFFF",
        }),
        "Forest": Theme("Forest", {
            "background_color": "#1A2F1A",
            "secondary_bg": "#2A472A",
            "button_color": "#3B5E3B",
            "button_hover_color": "#4C704C",
            "button_text_color": "#C1E3C1",
            "text_color": "#A5C9A5",
            "title_color": "#7FFF7F",
            "listbox_bg": "#2A472A",
            "listbox_fg": "#C1E3C1",
            "entry_bg": "#2A472A",
            "entry_fg": "#C1E3C1",
            "selection_bg": "#4C704C",
            "selection_fg": "#FFFFFF",
        }),
        "Ocean": Theme("Ocean", {
            "background_color": "#0A192F",
            "secondary_bg": "#172A45",
            "button_color": "#2A4365",
            "button_hover_color": "#3B5E8C",
            "button_text_color": "#8BE9FD",
            "text_color": "#64FFDA",
            "title_color": "#00B4D8",
            "listbox_bg": "#172A45",
            "listbox_fg": "#8BE9FD",
            "entry_bg": "#172A45",
            "entry_fg": "#64FFDA",
            "selection_bg": "#3B5E8C",
            "selection_fg": "#FFFFFF",
        }),
        "Sunset": Theme("Sunset", {
            "background_color": "#2D1B2D",
            "secondary_bg": "#432D3D",
            "button_color": "#FF6B6B",
            "button_hover_color": "#FF8E8E",
            "button_text_color": "#FFE66D",
            "text_color": "#FFB997",
            "title_color": "#FF8E8E",
            "listbox_bg": "#432D3D",
            "listbox_fg": "#FFB997",
            "entry_bg": "#432D3D",
            "entry_fg": "#FFB997",
            "selection_bg": "#FF6B6B",
            "selection_fg": "#FFE66D",
        })
    }

    @staticmethod
    def get_theme(theme_name):
        """Get a Theme object for a specific theme"""
        return ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES["Dark Purple"])

    @staticmethod
    def get_available_themes():
        """Get list of available theme names"""
        return list(ThemeManager.THEMES.keys())

    @staticmethod
    def apply_theme(widget, settings):
        """Apply the current theme to a widget"""
        theme = ThemeManager.get_theme(settings["current_theme"])
        theme.apply(widget)

    @staticmethod
    def create_themed_toplevel(parent, settings, title=""):
        window = tk.Toplevel(parent)
        window.title(title)
        theme = ThemeManager.get_theme(settings["current_theme"])
        theme.apply(window)
        
        # Center the window
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        
        return window

    @staticmethod
    def setup_hover_animation(button, settings):
        """Create smooth hover animation for buttons"""
        theme = ThemeManager.get_theme(settings["current_theme"])
        theme.setup_hover_animation(button)
