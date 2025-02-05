import tkinter as tk
from tkinter import ttk

class RatingDialog(tk.Toplevel):
    def __init__(self, parent, movie):
        super().__init__(parent)
        self.movie = movie
        self.result = None
        self.rating_frames = []
        
        # Configure window
        self.title(f"Rate Movie: {movie.title}")
        self.geometry("400x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Main container with padding
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)
        
        # Title label
        tk.Label(main_frame, text="Add Multiple Ratings", font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
        
        # Scrollable container
        scroll_container = tk.Frame(main_frame)
        scroll_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(scroll_container, height=250)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        
        # Create frame for ratings
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Add frame to canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=350)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, pady=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Add/Remove buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        tk.Button(button_frame, text="Add Rating", command=self._add_rating).pack(side="left", padx=5)
        tk.Button(button_frame, text="Remove Last", command=self._remove_last_rating).pack(side="left", padx=5)
        
        # Submit/Cancel buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill="x", pady=(10, 0))
        
        tk.Button(control_frame, text="Submit", command=self.submit).pack(side="right", padx=5)
        tk.Button(control_frame, text="Cancel", command=self.cancel).pack(side="right", padx=5)
        
        # Add first rating scale
        self._add_rating()
        
        # Center window
        self.center_window()
        
        # Add mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _add_rating(self):
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(fill="x", pady=5, padx=5)
        
        # Rating header with number
        tk.Label(frame, text=f"Rating {len(self.rating_frames) + 1}", 
                font=('Helvetica', 10, 'bold')).pack(pady=(5,0))
        
        # Scale frame
        scale_frame = tk.Frame(frame)
        scale_frame.pack(fill="x", pady=5)
        
        # Rating scale with number display
        rating_var = tk.StringVar(value="5")
        scale = ttk.Scale(
            scale_frame,
            from_=1,
            to=10,
            variable=rating_var,
            orient="horizontal"
        )
        scale.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        # Rating label
        rating_label = tk.Label(scale_frame, text="5/10", width=5)
        rating_label.pack(side="right")
        
        # Update label when scale moves
        scale.config(command=lambda *args: rating_label.config(
            text=f"{int(float(rating_var.get()))}/10"))
        
        # Store components
        self.rating_frames.append({
            'frame': frame,
            'scale': scale,
            'var': rating_var,
            'label': rating_label
        })
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _remove_last_rating(self):
        """Remove the last rating scale"""
        if len(self.rating_frames) > 1:  # Keep at least one rating scale
            frame_data = self.rating_frames.pop()
            frame_data['frame'].destroy()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def cancel(self):
        self.result = None
        self.destroy()
        
    def submit(self):
        # Collect all ratings
        self.result = [int(float(frame['var'].get())) for frame in self.rating_frames]
        self.destroy()
