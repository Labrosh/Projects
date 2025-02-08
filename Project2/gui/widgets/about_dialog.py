import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
import os
import logging
from gui.color_scheme import ColorSchemeManager

class AboutDialog(tk.Toplevel):
    LOGO_CACHE_PATH = "data/cache/tmdb_logo.png"
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Movie Tracker")
        self.geometry("500x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Configure colors
        self.tmdb_colors = {
            'primary': '#0d253f',    # Dark blue
            'secondary': '#01b4e4',   # Light blue
            'tertiary': '#90cea1'     # Light green
        }

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # App title
        app_title = ttk.Label(main_frame, text="Movie Tracker", 
                            font=('Helvetica', 16, 'bold'))
        app_title.pack(pady=(0, 20))

        # Load and display TMDB logo
        self.load_tmdb_logo()
        if hasattr(self, 'logo_image'):
            logo_label = ttk.Label(main_frame, image=self.logo_image)
            logo_label.pack(pady=(0, 10))
        else:
            # Fallback text if logo can't be loaded
            fallback_text = ttk.Label(main_frame, 
                                    text="Powered by TMDB",
                                    font=('Helvetica', 14))
            fallback_text.pack(pady=(0, 10))

        # Attribution text
        attribution = ttk.Label(main_frame, 
                              text="This product uses the TMDB API but is not endorsed or certified by TMDB.",
                              wraplength=400)
        attribution.pack(pady=(0, 20))

        # Close button
        close_btn = ttk.Button(main_frame, text="Close", command=self.destroy)
        close_btn.pack(pady=(10, 0))

        self.center_window()

    def load_tmdb_logo(self):
        """Load TMDB logo from cache"""
        try:
            # Create cache directory if it doesn't exist
            os.makedirs(os.path.dirname(self.LOGO_CACHE_PATH), exist_ok=True)
            
            # Load from cache
            if os.path.exists(self.LOGO_CACHE_PATH):
                logging.debug("Loading TMDB logo from cache")
                self.logo_image = ImageTk.PhotoImage(Image.open(self.LOGO_CACHE_PATH))
            else:
                logging.error("TMDB logo not found in cache")
                self.logo_image = None
                
        except Exception as e:
            logging.error(f"Failed to handle TMDB logo: {e}")
            self.logo_image = None

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
