import tkinter as tk
from PIL import Image, ImageTk
import os

class ThumbnailListbox(tk.Canvas):
    def __init__(self, parent, **kwargs):
        # Store style options before creating canvas
        self.font = kwargs.pop('font', ('Helvetica', 10))
        self.fg = kwargs.pop('fg', 'black')
        self.bg = kwargs.pop('bg', 'white')
        self.selectbackground = kwargs.pop('selectbackground', '#0078D7')
        self.selectforeground = kwargs.pop('selectforeground', 'white')
        
        # Remove other Listbox-specific options that Canvas doesn't support
        kwargs.pop('selectmode', None)
        kwargs.pop('activestyle', None)
        
        # Initialize canvas with remaining kwargs
        super().__init__(parent, **kwargs)
        
        self.configure(bg=self.bg)  # Set canvas background
        
        self.items = []
        self.images = {}  # Store PhotoImage references
        self.selected_index = None
        self.item_height = 70  # Height for each item
        self.thumbnail_size = (40, 60)  # Width, Height for thumbnails
        
        # Bindings for selection
        self.bind('<Button-1>', self._on_click)
        
        # Scrolling
        self.configure(scrollregion=(0, 0, 0, 0))
        self._total_height = 0
        
        # Modify mousewheel binding to use proper scroll region
        self.bind_all('<MouseWheel>', self._on_mousewheel)
        self.bind('<Configure>', self._on_configure)

    def delete(self, first, last=None):
        """Clear all items"""
        self.items.clear()
        self.images.clear()
        self.selected_index = None
        super().delete('all')  # Use parent class's delete method instead of calling self.delete

    def insert(self, index, movie):
        """Insert a movie at specified index"""
        if index == tk.END:
            index = len(self.items)  # Convert END to actual index
        self.items.insert(index, movie)
        self._redraw()

    def curselection(self):
        """Return current selection for compatibility with tk.Listbox"""
        return (self.selected_index,) if self.selected_index is not None else ()

    def get(self, index):
        """Get item at index"""
        try:
            index = int(index)  # Ensure index is an integer
            if 0 <= index < len(self.items):
                if hasattr(self.items[index], 'title'):
                    return self.items[index].title
                return str(self.items[index])
        except (ValueError, TypeError):
            pass
        return None

    def _create_thumbnail(self, poster_path):
        """Create thumbnail from poster path"""
        if not poster_path or not os.path.exists(poster_path):
            return None
            
        try:
            image = Image.open(poster_path)
            image.thumbnail(self.thumbnail_size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None

    def _redraw(self):
        """Redraw all items"""
        super().delete('all')
        y = 5
        
        for i, movie in enumerate(self.items):
            # Background rectangle
            item_area = self.create_rectangle(
                5, y, self.winfo_width()-5, y+self.item_height-5,
                fill=self._get_item_color(i),
                width=0,
                tags=f'item_{i}'
            )
            
            # Poster thumbnail and title area
            x_offset = 15
            if hasattr(movie, 'get_poster_path') and movie.get_poster_path():
                if movie not in self.images:
                    self.images[movie] = self._create_thumbnail(movie.get_poster_path())
                if self.images[movie]:
                    self.create_image(x_offset, y+5, anchor='nw', 
                                   image=self.images[movie],
                                   tags=f'item_{i}')
            
            # Movie title and rating
            text_color = self.selectforeground if i == self.selected_index else self.fg
            title = movie.title if hasattr(movie, 'title') else str(movie)
            
            rating_text = ""
            if hasattr(movie, 'details') and movie.details:
                rating = movie.details.get('vote_average')
                if rating:
                    rating_text = f" ★ {rating:.1f}"
            
            self.create_text(
                x_offset + 55, y + 20,  # Moved up to make room for genres
                text=title + rating_text,
                anchor='w',
                font=self.font,
                fill=text_color,
                tags=f'item_{i}'
            )
            
            # Add genre tags
            if hasattr(movie, 'details') and movie.details and 'genres' in movie.details:
                genre_text = ' • '.join(g['name'] for g in movie.details['genres'][:3])  # Limit to 3 genres
                self.create_text(
                    x_offset + 55, y + self.item_height - 20,  # Position below title
                    text=genre_text,
                    anchor='w',
                    font=(self.font[0], int(self.font[1] * 0.9)),  # Slightly smaller font
                    fill='#666666',  # Subdued color for genres
                    tags=f'item_{i}'
                )
            
            y += self.item_height
        
        # Update scroll region
        self._total_height = y
        self.configure(scrollregion=(0, 0, self.winfo_width(), self._total_height))

    def _get_item_color(self, index):
        """Get background color for item"""
        if index == self.selected_index:
            return self.selectbackground
        return self.bg

    def _on_click(self, event):
        """Handle mouse click for selection only"""
        y = self.canvasy(event.y)
        clicked_index = int(y // self.item_height)
        
        if 0 <= clicked_index < len(self.items):
            self._select_item(clicked_index)

    def _select_item(self, index):
        """Handle item selection"""
        if 0 <= index < len(self.items):
            self.selected_index = index
            self._redraw()
            self.event_generate('<<ListboxSelect>>')

    def _on_configure(self, event):
        """Handle resize"""
        self._redraw()

    def _on_mousewheel(self, event):
        """Improved mousewheel scrolling"""
        if self._total_height > self.winfo_height():
            self.yview_scroll(int(-1*(event.delta/120)), "units")

    def yview_scroll(self, number, what):
        """Override scroll to ensure proper movement"""
        if what == "units":
            delta = number * self.item_height
        else:
            delta = number * self.winfo_height()
        
        current = self.yview()[0]
        self.yview_moveto(current + (delta / self._total_height))

    def filter_by_genre(self, genre):
        """Filter items to show only movies with specified genre"""
        if not genre:  # If no genre specified, show all
            return self.items
        
        filtered = []
        for movie in self.items:
            if (hasattr(movie, 'details') and movie.details 
                and 'genres' in movie.details):
                genres = [g['name'].lower() for g in movie.details['genres']]
                if genre.lower() in genres:
                    filtered.append(movie)
        return filtered
