import tkinter as tk
from gui.color_scheme import ColorSchemeManager

class MovieListPanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Now we have access to all app components through self.app
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Create widgets
        title_style = {
            "font": (app.ui_settings["font_family"], app.ui_settings["font_size"] + 4, "bold"),
            "fg": app.ui_settings["title_color"],
            "bg": app.ui_settings["background_color"]
        }
        
        listbox_style = {
            "font": (app.ui_settings["font_family"], app.ui_settings["font_size"]),
            "selectmode": tk.SINGLE,
            "relief": tk.FLAT,
            "borderwidth": 0,
            "bg": app.ui_settings["listbox_bg"],
            "fg": app.ui_settings["listbox_fg"],
            "selectbackground": app.ui_settings["selection_bg"],
            "selectforeground": app.ui_settings["selection_fg"],
            "activestyle": "none"
        }

        # Create and grid widgets
        self.label_to_watch = tk.Label(self, text="Movies to Watch", **title_style)
        self.label_to_watch.grid(row=0, column=0, pady=5, sticky="ew")

        # Create listbox with scrollbar for to-watch
        to_watch_frame = tk.Frame(self)
        to_watch_frame.grid(row=1, column=0, pady=5, sticky="nsew")
        to_watch_frame.grid_columnconfigure(0, weight=1)
        to_watch_frame.grid_rowconfigure(0, weight=1)

        self.to_watch_listbox = tk.Listbox(to_watch_frame, **listbox_style)
        self.to_watch_listbox.grid(row=0, column=0, sticky="nsew")
        to_watch_scrollbar = tk.Scrollbar(to_watch_frame, orient="vertical")
        to_watch_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.to_watch_listbox.config(yscrollcommand=to_watch_scrollbar.set)
        to_watch_scrollbar.config(command=self.to_watch_listbox.yview)

        self.label_watched = tk.Label(self, text="Movies Watched", **title_style)
        self.label_watched.grid(row=2, column=0, pady=5, sticky="ew")

        # Create listbox with scrollbar for watched
        watched_frame = tk.Frame(self)
        watched_frame.grid(row=3, column=0, pady=5, sticky="nsew")
        watched_frame.grid_columnconfigure(0, weight=1)
        watched_frame.grid_rowconfigure(0, weight=1)

        self.watched_listbox = tk.Listbox(watched_frame, **listbox_style)
        self.watched_listbox.grid(row=0, column=0, sticky="nsew")
        watched_scrollbar = tk.Scrollbar(watched_frame, orient="vertical")
        watched_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.watched_listbox.config(yscrollcommand=watched_scrollbar.set)
        watched_scrollbar.config(command=self.watched_listbox.yview)

        ColorSchemeManager.apply_scheme(self, app.ui_settings)
        self._setup_drag_drop()


    def _setup_drag_drop(self):
        def start_drag(event, listbox):
            listbox.drag_start = event.y
            
        def do_drag(event, from_list, to_list):
            if hasattr(from_list, 'drag_start'):
                sel = from_list.curselection()
                if sel:
                    idx = from_list.nearest(event.y)
                    if idx != sel[0]:
                        text = from_list.get(sel)
                        from_list.delete(sel)
                        to_list.insert(idx, text)
                        
        # Enable drag between lists
        self.to_watch_listbox.bind('<Button-1>', lambda e: start_drag(e, self.to_watch_listbox))
        self.watched_listbox.bind('<Button-1>', lambda e: start_drag(e, self.watched_listbox))
        self.to_watch_listbox.bind('<B1-Motion>', lambda e: do_drag(e, self.to_watch_listbox, self.watched_listbox))
        self.watched_listbox.bind('<B1-Motion>', lambda e: do_drag(e, self.watched_listbox, self.to_watch_listbox))

    def _setup_context_menus(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.app.show_selected_movie_details)
        self.context_menu.add_command(label="View Poster", command=self.app.show_selected_movie_poster)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Mark as Watched", command=self.app.movie_list_gui.mark_as_watched)
        self.context_menu.add_command(label="Remove Movie", command=self.app.movie_list_gui.remove_movie)

        def show_context_menu(event, listbox):
            item = listbox.identify_row(event.y)
            if item:
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(item)
                self.context_menu.post(event.x_root, event.y_root)

        self.to_watch_listbox.bind("<Button-3>", lambda e: show_context_menu(e, self.to_watch_listbox))
        self.watched_listbox.bind("<Button-3>", lambda e: show_context_menu(e, self.watched_listbox))
