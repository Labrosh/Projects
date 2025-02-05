import tkinter as tk
from tkinter import ttk
import re

class BulkImportDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        
        # Configure window
        self.title("Bulk Import Movies")
        self.geometry("600x900")  # Even bigger initial size
        self.minsize(500, 700)    # Larger minimum size
        self.resizable(True, True) # Allow resizing
        
        # Main container with padding
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Instructions (now in a scrollable text widget)
        instruction_frame = tk.Frame(main_frame)
        instruction_frame.pack(fill="x", pady=5)
        instruction_label = tk.Label(instruction_frame, text="Paste your movie list in any format:",
                                   anchor="w", justify=tk.LEFT)
        instruction_label.pack(fill="x")
        
        # Examples in a separate frame
        example_text = """Examples:
1. The Matrix
2. Inception
* Lord of the Rings
- Star Wars
Avatar (2009)
"""
        example_frame = tk.LabelFrame(main_frame, text="Supported Formats")
        example_frame.pack(fill="x", pady=5)
        tk.Label(example_frame, text=example_text, justify=tk.LEFT).pack(padx=5, pady=5)
        
        # Text area for movies (make it bigger)
        self.text_area = tk.Text(main_frame, width=60, height=25)  # Increased height
        self.text_area.pack(fill="both", expand=True, pady=5)
        
        # Preview area (make it bigger and scrollable)
        preview_frame = ttk.LabelFrame(main_frame, text="Preview of detected movies")
        preview_frame.pack(fill="both", expand=True, pady=5)
        
        preview_scroll = ttk.Scrollbar(preview_frame)
        preview_scroll.pack(side="right", fill="y")
        
        self.preview_area = tk.Text(preview_frame, width=60, height=10, 
                                  yscrollcommand=preview_scroll.set)
        self.preview_area.pack(fill="both", expand=True)
        preview_scroll.config(command=self.preview_area.yview)
        
        # Update preview as user types
        self.text_area.bind('<KeyRelease>', self._update_preview)
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=(20, 10))  # More top padding
        
        tk.Button(button_frame, text="Import", command=self.submit).pack(side="right", padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="right", padx=5)
        
        self.center_window()
        
    def _clean_title(self, line):
        """Clean a line to extract just the movie title"""
        # More precise pattern for list markers
        # Handle numbered lists (1., 1), bullet points (*, -, •), and other markers
        line = re.sub(r'^\s*(?:\d+[\.\)]|\*|\-|•|○|◦|▪︎|>|\.|)\s*', '', line)
        # Remove trailing year if present
        line = re.sub(r'\s*\(\d{4}\)\s*$', '', line)
        # Remove any remaining leading/trailing whitespace and dots
        line = line.strip(' .')
        return line if line else None

    def _parse_text(self, text):
        """Parse text into list of movie titles"""
        lines = text.split('\n')
        movies = []
        for line in lines:
            title = self._clean_title(line)
            if title:  # Only add non-empty, non-None titles
                movies.append(title)  # Removed debug print
        return movies

    def _update_preview(self, event=None):
        """Update preview area with detected movies"""
        text = self.text_area.get("1.0", "end-1c")
        movies = self._parse_text(text)
        
        self.preview_area.config(state='normal')
        self.preview_area.delete("1.0", "end")
        preview_text = f"Found {len(movies)} movies:\n\n"
        preview_text += "\n".join(movies)  # Show all movies, not just first 5
        self.preview_area.insert("1.0", preview_text)
        self.preview_area.config(state='disabled')
        
    def submit(self):
        text = self.text_area.get("1.0", "end-1c")
        movies = self._parse_text(text)
        if movies:
            self.result = movies
        self.destroy()
        
    def cancel(self):
        self.result = None
        self.destroy()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
