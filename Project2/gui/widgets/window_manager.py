import tkinter as tk
from PIL import Image, ImageTk
from gui.color_scheme import ColorSchemeManager

class WindowManager:
    def __init__(self, app):
        self.app = app

    def show_poster_window(self, movie, poster_path):
        poster_window = ColorSchemeManager.create_themed_toplevel(self.app.root, self.app.ui_settings)
        poster_window.title(movie.title)
        poster_image = Image.open(poster_path)
        poster_image = poster_image.resize((300, 450), Image.LANCZOS)
        poster_photo = ImageTk.PhotoImage(poster_image)
        poster_label = tk.Label(poster_window, image=poster_photo)
        poster_label.image = poster_photo
        poster_label.pack(padx=10, pady=10)
        ColorSchemeManager.apply_scheme(poster_window, self.app.ui_settings)
        self._center_window(poster_window)

    def show_details_window(self, movie):
        details_window = ColorSchemeManager.create_themed_toplevel(self.app.root, self.app.ui_settings)
        details_window.title(movie.title)

        details_text = tk.Text(details_window, wrap=tk.WORD)
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        formatted_details = f"""
Title: {movie.details.get('title', 'N/A')}
Release Date: {movie.details.get('release_date', 'N/A')}
Genres: {', '.join([genre['name'] for genre in movie.details.get('genres', [])])}
Overview: {movie.details.get('overview', 'N/A')}
Runtime: {movie.details.get('runtime', 'N/A')} minutes
Rating: {movie.details.get('vote_average', 'N/A')} ({movie.details.get('vote_count', 'N/A')} votes)
Homepage: {movie.details.get('homepage', 'N/A')}
        """

        details_text.insert(tk.END, formatted_details)
        details_text.configure(state='disabled')
        ColorSchemeManager.apply_scheme(details_window, self.app.ui_settings)
        self._center_window(details_window)

    def show_settings_window(self):
        settings_window = ColorSchemeManager.create_themed_toplevel(
            self.app.root, 
            self.app.ui_settings, 
            "Settings"
        )
        settings_window.geometry("600x800")
        self._create_settings_content(settings_window)
        self._center_window(settings_window)

    def _create_settings_content(self, window):
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        main_frame = tk.Frame(window, bg=self.app.ui_settings["background_color"])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)

        theme_var = self._create_theme_selection(main_frame)
        settings_entries = self._create_settings_inputs(main_frame)
        self._create_save_button(main_frame, theme_var, settings_entries)
        
        ColorSchemeManager.apply_scheme(window, self.app.ui_settings)

    def _create_theme_selection(self, parent):
        theme_frame = tk.LabelFrame(
            parent,
            text="Theme Selection",
            bg=self.app.ui_settings["background_color"],
            fg=self.app.ui_settings["text_color"]
        )
        theme_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        theme_frame.grid_columnconfigure(0, weight=1)

        theme_var = tk.StringVar(value=self.app.ui_settings.get("current_scheme", "Dark Purple"))
        for theme in self.app.settings_manager.get_available_schemes():
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
        
        return theme_var

    def _create_settings_inputs(self, parent):
        settings_frame = tk.LabelFrame(
            parent,
            text="Application Settings",
            bg=self.app.ui_settings["background_color"],
            fg=self.app.ui_settings["text_color"]
        )
        settings_frame.grid(row=1, column=0, sticky="ew")
        settings_frame.grid_columnconfigure(1, weight=1)

        settings = [
            ("Font Size:", "font_size"),
            ("Element Spacing:", "element_spacing"),
            ("Listbox Height:", "listbox_height"),
            ("Listbox Width:", "listbox_width"),
            ("Window Width:", "window_width"),
            ("Window Height:", "window_height")
        ]

        entries = {}
        for i, (label_text, setting_key) in enumerate(settings):
            tk.Label(
                settings_frame,
                text=label_text,
                bg=self.app.ui_settings["background_color"],
                fg=self.app.ui_settings["text_color"]
            ).grid(row=i, column=0, sticky="w", padx=20, pady=10)
            
            entry = tk.Entry(
                settings_frame,
                bg=self.app.ui_settings["entry_bg"],
                fg=self.app.ui_settings["entry_fg"],
                insertbackground=self.app.ui_settings["text_color"]
            )
            entry.insert(0, str(self.app.ui_settings[setting_key]))
            entry.grid(row=i, column=1, sticky="ew", padx=20)
            entries[setting_key] = entry

        return entries

    def _create_save_button(self, parent, theme_var, settings_entries):
        def save_settings():
            try:
                new_settings = {
                    "current_scheme": theme_var.get(),
                    "font_size": int(settings_entries["font_size"].get()),
                    "element_spacing": int(settings_entries["element_spacing"].get()),
                    "listbox_height": int(settings_entries["listbox_height"].get()),
                    "listbox_width": int(settings_entries["listbox_width"].get()),
                    "window_width": int(settings_entries["window_width"].get()),
                    "window_height": int(settings_entries["window_height"].get())
                }
                self.app.settings_manager.update_settings(new_settings)
                self.app.update_ui()
                ColorSchemeManager.apply_scheme(self.app.root, self.app.settings_manager.ui_settings)
                parent.master.destroy()
                tk.messagebox.showinfo("Settings", "Settings have been updated.")
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter valid numbers for all settings.")

        save_button = tk.Button(
            parent,
            text="Save Settings",
            command=save_settings,
            bg=self.app.ui_settings["button_color"],
            fg=self.app.ui_settings["button_text_color"]
        )
        save_button.grid(row=2, column=0, pady=20, sticky="ew")

    def _center_window(self, window):
        # Withdraw window temporarily
        window.withdraw()
        
        # Wait for window to be ready
        window.update_idletasks()
        
        # Get window size
        width = window.winfo_width()
        height = window.winfo_height()
        
        # Get primary screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position (ensuring window is fully visible on primary monitor)
        x = max(0, int((screen_width - width) / 2))
        y = max(0, int((screen_height - height) / 2))
        
        # Set position
        window.geometry(f'+{x}+{y}')
        
        # Make window visible and bring to front
        window.deiconify()
        window.lift()
        window.attributes('-topmost', True)
        window.update()
        window.attributes('-topmost', False)
