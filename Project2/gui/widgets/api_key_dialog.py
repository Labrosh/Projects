import tkinter as tk
from tkinter import ttk
from api.tmdb_api import TMDbAPI

class APIKeyDialog(tk.Toplevel):
    def __init__(self, parent, settings_manager):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.result = None
        
        self.title("TMDb API Key Setup")
        self.geometry("400x200")
        
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        ttk.Label(main_frame, text="Enter your TMDb API key:").pack(pady=10)
        
        # API key entry
        self.api_key = tk.StringVar()
        self.entry = ttk.Entry(main_frame, textvariable=self.api_key, width=40)
        self.entry.pack(pady=10)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save_key).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Skip (Offline Mode)", command=self.enable_offline).pack(side=tk.LEFT, padx=5)
        
        self.transient(parent)
        self.grab_set()
        
    def save_key(self):
        key = self.api_key.get().strip()
        if key and TMDbAPI.validate_api_key(key):
            self.settings_manager.set_api_key(key)
            TMDbAPI.set_api_key(key)
            self.result = "api_key"
            self.destroy()
        else:
            tk.messagebox.showerror("Invalid Key", "Please enter a valid TMDb API key")
            
    def enable_offline(self):
        self.settings_manager.enable_offline_mode()
        self.result = "offline"
        self.destroy()
