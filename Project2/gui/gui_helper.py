import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
from gui.gui_movie_list import MovieListGUI
from gui.gui_search import MovieSearchGUI

def update_listbox(listbox, items):
    listbox.delete(0, tk.END)
    for item in items:
        listbox.insert(tk.END, item.title)

def show_movie_poster(root, movie):
    poster_path = movie.poster_path
    if poster_path:
        if not poster_path.startswith("http"):
            poster_path = os.path.join("posters", os.path.basename(poster_path))
        if os.path.exists(poster_path):
            poster_window = tk.Toplevel(root)
            poster_window.title(movie.title)
            poster_image = Image.open(poster_path)
            poster_image = poster_image.resize((300, 450), Image.LANCZOS)
            poster_photo = ImageTk.PhotoImage(poster_image)
            poster_label = tk.Label(poster_window, image=poster_photo)
            poster_label.image = poster_photo
            poster_label.pack()
        else:
            messagebox.showwarning("Warning", "Poster not found.")

def show_movie_details(root, movie):
    details = movie.details
    if details:
        details_window = tk.Toplevel(root)
        details_window.title(movie.title)

        details_text = tk.Text(details_window, wrap=tk.WORD)
        details_text.pack(fill=tk.BOTH, expand=True)

        formatted_details = f"""
Title: {details.get('title', 'N/A')}
Release Date: {details.get('release_date', 'N/A')}
Genres: {', '.join([genre['name'] for genre in details.get('genres', [])])}
Overview: {details.get('overview', 'N/A')}
Runtime: {details.get('runtime', 'N/A')} minutes
Rating: {details.get('vote_average', 'N/A')} ({details.get('vote_count', 'N/A')} votes)
Homepage: {details.get('homepage', 'N/A')}
        """

        details_text.insert(tk.END, formatted_details)
    else:
        messagebox.showwarning("Warning", "Details not found.")

def create_widgets(app):
    main_frame = tk.Frame(app.root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    app.label_to_watch = tk.Label(main_frame, text="Movies to Watch", font=("Arial", app.ui_settings["font_size"]))
    app.label_to_watch.pack(pady=app.ui_settings["element_spacing"])

    app.to_watch_listbox = tk.Listbox(main_frame, height=app.ui_settings["listbox_height"], width=app.ui_settings["listbox_width"])
    app.to_watch_listbox.pack(pady=app.ui_settings["element_spacing"])

    app.label_watched = tk.Label(main_frame, text="Movies Watched", font=("Arial", app.ui_settings["font_size"]))
    app.label_watched.pack(pady=app.ui_settings["element_spacing"])

    app.watched_listbox = tk.Listbox(main_frame, height=app.ui_settings["listbox_height"], width=app.ui_settings["listbox_width"])
    app.watched_listbox.pack(pady=app.ui_settings["element_spacing"])

    movie_entry_frame = tk.Frame(main_frame)
    movie_entry_frame.pack(pady=app.ui_settings["element_spacing"])

    app.movie_entry = tk.Entry(movie_entry_frame, width=40)
    app.movie_entry.pack(side=tk.LEFT, padx=app.ui_settings["element_spacing"])

    movie_list_gui = MovieListGUI(app)
    add_button = tk.Button(movie_entry_frame, text="Add Movie", command=movie_list_gui.add_movie)
    add_button.pack(side=tk.LEFT, padx=app.ui_settings["element_spacing"])

    search_frame = tk.Frame(main_frame)
    search_frame.pack(pady=app.ui_settings["element_spacing"])

    app.search_entry = tk.Entry(search_frame, width=40)
    app.search_entry.pack(side=tk.LEFT, padx=app.ui_settings["element_spacing"])

    movie_search_gui = MovieSearchGUI(app)
    search_button = tk.Button(search_frame, text="Search & Add Movie", command=movie_search_gui.search_movie)
    search_button.pack(side=tk.LEFT, padx=app.ui_settings["element_spacing"])

    remove_button = tk.Button(main_frame, text="Remove Movie", command=movie_list_gui.remove_movie)
    remove_button.pack(pady=app.ui_settings["element_spacing"])

    watched_button = tk.Button(main_frame, text="Mark as Watched", command=movie_list_gui.mark_as_watched)
    watched_button.pack(pady=app.ui_settings["element_spacing"])

    unwatch_button = tk.Button(main_frame, text="Un-Watch", command=movie_list_gui.unwatch_movie)
    unwatch_button.pack(pady=app.ui_settings["element_spacing"])

    settings_button = tk.Button(main_frame, text="Settings", command=app.open_settings)
    settings_button.pack(pady=app.ui_settings["element_spacing"])

    view_details_button = tk.Button(main_frame, text="View Details", command=app.show_selected_movie_details)
    view_details_button.pack(pady=app.ui_settings["element_spacing"])

    view_poster_button = tk.Button(main_frame, text="View Poster", command=app.show_selected_movie_poster)
    view_poster_button.pack(pady=app.ui_settings["element_spacing"])

def open_settings(app):
    settings_window = tk.Toplevel(app.root)
    settings_window.title("Settings")
    settings_window.geometry("400x500")

    tk.Label(settings_window, text="Font Size:").pack(pady=app.ui_settings["element_spacing"])
    font_size_entry = tk.Entry(settings_window)
    font_size_entry.insert(0, app.ui_settings["font_size"])
    font_size_entry.pack(pady=app.ui_settings["element_spacing"])

    tk.Label(settings_window, text="Element Spacing:").pack(pady=app.ui_settings["element_spacing"])
    element_spacing_entry = tk.Entry(settings_window)
    element_spacing_entry.insert(0, app.ui_settings["element_spacing"])
    element_spacing_entry.pack(pady=app.ui_settings["element_spacing"])

    tk.Label(settings_window, text="Listbox Height (Number of Movies Displayed):").pack(pady=app.ui_settings["element_spacing"])
    listbox_height_entry = tk.Entry(settings_window)
    listbox_height_entry.insert(0, app.ui_settings["listbox_height"])
    listbox_height_entry.pack(pady=app.ui_settings["element_spacing"])

    tk.Label(settings_window, text="Listbox Width (Width of Movie List):").pack(pady=app.ui_settings["element_spacing"])
    listbox_width_entry = tk.Entry(settings_window)
    listbox_width_entry.insert(0, app.ui_settings["listbox_width"])
    listbox_width_entry.pack(pady=app.ui_settings["element_spacing"])

    tk.Label(settings_window, text="Window Width:").pack(pady=app.ui_settings["element_spacing"])
    window_width_entry = tk.Entry(settings_window)
    window_width_entry.insert(0, app.ui_settings["window_width"])
    window_width_entry.pack(pady=app.ui_settings["element_spacing"])

    tk.Label(settings_window, text="Window Height:").pack(pady=app.ui_settings["element_spacing"])
    window_height_entry = tk.Entry(settings_window)
    window_height_entry.insert(0, app.ui_settings["window_height"])
    window_height_entry.pack(pady=app.ui_settings["element_spacing"])

    def save_settings():
        new_settings = {
            "font_size": int(font_size_entry.get()),
            "element_spacing": int(element_spacing_entry.get()),
            "listbox_height": int(listbox_height_entry.get()),
            "listbox_width": int(listbox_width_entry.get()),
            "window_width": int(window_width_entry.get()),
            "window_height": int(window_height_entry.get())
        }
        app.settings_manager.update_settings(new_settings)
        app.update_ui()
        settings_window.destroy()
        messagebox.showinfo("Settings", "Settings have been updated.")

    save_button = tk.Button(settings_window, text="Save Settings", command=save_settings)
    save_button.pack(pady=app.ui_settings["element_spacing"])
