import tkinter as tk
from tkinter import ttk, messagebox
from api.tmdb_api import TMDbAPI

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, settings_manager):
        super().__init__(parent)
        self.settings_manager = settings_manager
        
        self.title("Settings")
        self.geometry("500x600")  # Made taller to accommodate more settings
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # API Settings Tab
        api_frame = self.create_api_tab(notebook)
        notebook.add(api_frame, text="API Settings")
        
        # Window Settings Tab
        window_frame = self.create_window_tab(notebook)
        notebook.add(window_frame, text="Window")
        
        # UI Settings Tab
        ui_frame = self.create_ui_tab(notebook)
        notebook.add(ui_frame, text="Interface")
        
        # Theme Tab
        theme_frame = self.create_theme_tab(notebook)
        notebook.add(theme_frame, text="Theme")
        
        # Save/Close buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save All", command=self.save_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        self.transient(parent)
        self.grab_set()
        
    def create_api_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        
        ttk.Label(frame, text="TMDb API Key:").pack(pady=(0,5))
        
        self.api_key_var = tk.StringVar(value=self.settings_manager.get_api_key() or '')
        api_key_entry = ttk.Entry(frame, textvariable=self.api_key_var, width=40)
        api_key_entry.pack(pady=5)
        
        ttk.Button(frame, text="Validate & Save Key", command=self.save_api_key).pack(pady=5)
        
        if self.settings_manager.is_offline_mode():
            ttk.Label(frame, 
                     text="Currently in offline mode.\nAdd an API key to enable online features.",
                     justify='center').pack(pady=20)
        
        return frame
        
    def create_window_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        
        # Window size settings
        size_frame = ttk.LabelFrame(frame, text="Window Size", padding=10)
        size_frame.pack(fill='x', pady=5)
        
        # Minimum dimensions
        ttk.Label(size_frame, text="Minimum Width:").grid(row=0, column=0, padx=5, pady=5)
        self.min_width_var = tk.StringVar(value=self.settings_manager.ui_settings["minimum_width"])
        ttk.Entry(size_frame, textvariable=self.min_width_var, width=10).grid(row=0, column=1)
        
        ttk.Label(size_frame, text="Minimum Height:").grid(row=1, column=0, padx=5, pady=5)
        self.min_height_var = tk.StringVar(value=self.settings_manager.ui_settings["minimum_height"])
        ttk.Entry(size_frame, textvariable=self.min_height_var, width=10).grid(row=1, column=1)
        
        return frame
        
    def create_ui_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        
        # Font settings
        font_frame = ttk.LabelFrame(frame, text="Font Settings", padding=10)
        font_frame.pack(fill='x', pady=5)
        
        ttk.Label(font_frame, text="Font Family:").grid(row=0, column=0, padx=5, pady=5)
        self.font_family_var = tk.StringVar(value=self.settings_manager.ui_settings["font_family"])
        ttk.Entry(font_frame, textvariable=self.font_family_var).grid(row=0, column=1)
        
        ttk.Label(font_frame, text="Font Size:").grid(row=1, column=0, padx=5, pady=5)
        self.font_size_var = tk.StringVar(value=self.settings_manager.ui_settings["font_size"])
        ttk.Entry(font_frame, textvariable=self.font_size_var, width=5).grid(row=1, column=1)
        
        # Element settings
        element_frame = ttk.LabelFrame(frame, text="UI Elements", padding=10)
        element_frame.pack(fill='x', pady=5)
        
        ttk.Label(element_frame, text="Button Width:").grid(row=0, column=0, padx=5, pady=5)
        self.button_width_var = tk.StringVar(value=self.settings_manager.ui_settings["button_width"])
        ttk.Entry(element_frame, textvariable=self.button_width_var, width=5).grid(row=0, column=1)
        
        return frame
        
    def create_theme_tab(self, parent):
        frame = ttk.Frame(parent, padding=20)
        
        ttk.Label(frame, text="Color Scheme:").pack(pady=(0,5))
        schemes = self.settings_manager.get_available_schemes()
        current_scheme = self.settings_manager.ui_settings.get("current_scheme")
        
        self.scheme_var = tk.StringVar(value=current_scheme)
        scheme_combo = ttk.Combobox(frame, 
                                  textvariable=self.scheme_var,
                                  values=schemes,
                                  state='readonly')
        scheme_combo.pack(pady=5)
        
        return frame
    
    def save_api_key(self):
        key = self.api_key_var.get().strip()
        if not key:
            if messagebox.askyesno("Enable Offline Mode", 
                                 "No API key entered. Enable offline mode?"):
                self.settings_manager.enable_offline_mode()
                messagebox.showinfo("Success", "Offline mode enabled")
            return
            
        if TMDbAPI.validate_api_key(key):
            self.settings_manager.set_api_key(key)
            TMDbAPI.set_api_key(key)
            messagebox.showinfo("Success", "API key saved successfully!")
        else:
            messagebox.showerror("Invalid Key", "Please enter a valid TMDb API key")
            
    def save_all(self):
        """Save all settings"""
        new_settings = {
            "minimum_width": int(self.min_width_var.get()),
            "minimum_height": int(self.min_height_var.get()),
            "font_family": self.font_family_var.get(),
            "font_size": int(self.font_size_var.get()),
            "button_width": int(self.button_width_var.get()),
            "current_scheme": self.scheme_var.get()
        }
        
        self.settings_manager.update_settings(new_settings)
        messagebox.showinfo("Success", "Settings saved successfully!")
