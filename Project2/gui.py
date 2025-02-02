import tkinter as tk
from tkinter import messagebox
import json
import movie_data  # Import movie functions
import tmdb_api  # Import TMDb API functions

# UI Settings
ui_settings = {
    "font_size": 16,
    "element_spacing": 5,
    "listbox_height": 10,
    "listbox_width": 50,
    "window_width": 600,
    "window_height": 900
}

# Load settings from file
def load_settings():
    global ui_settings
    try:
        with open("settings.json", "r") as file:
            ui_settings.update(json.load(file))
    except FileNotFoundError:
        pass

# Save settings to file
def save_settings_to_file():
    with open("settings.json", "w") as file:
        json.dump(ui_settings, file)

load_settings()

def run_gui():
    """Initialize the GUI window."""
    root = tk.Tk()
    root.title("Movielog - Movie Tracker")
    root.geometry(f"{ui_settings['window_width']}x{ui_settings['window_height']}")

    # Main Frame
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Label - "To Watch" List
    label_to_watch = tk.Label(main_frame, text="Movies to Watch", font=("Arial", ui_settings["font_size"]))
    label_to_watch.pack(pady=ui_settings["element_spacing"])

    # Movie Listbox - "To Watch"
    to_watch_listbox = tk.Listbox(main_frame, height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
    to_watch_listbox.pack(pady=ui_settings["element_spacing"])

    # Label - "Watched" List
    label_watched = tk.Label(main_frame, text="Movies Watched", font=("Arial", ui_settings["font_size"]))
    label_watched.pack(pady=ui_settings["element_spacing"])

    # Movie Listbox - "Watched"
    watched_listbox = tk.Listbox(main_frame, height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
    watched_listbox.pack(pady=ui_settings["element_spacing"])

    # Load movies from movie_data.py
    def load_movies():
        to_watch_listbox.delete(0, tk.END)
        watched_listbox.delete(0, tk.END)
        for movie in movie_data.movies_to_watch:
            to_watch_listbox.insert(tk.END, movie)
        for movie in movie_data.movies_watched:
            watched_listbox.insert(tk.END, movie)

    movie_data.load_data()  # Load from JSON
    load_movies()  # Display in GUI

    # Add Movie Entry + Button
    movie_entry_frame = tk.Frame(main_frame)
    movie_entry_frame.pack(pady=ui_settings["element_spacing"])

    movie_entry = tk.Entry(movie_entry_frame, width=40)
    movie_entry.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

    def add_movie():
        movie = movie_entry.get().strip()
        if movie:
            movie_data.movies_to_watch.append(movie)
            movie_data.save_data()
            load_movies()
            movie_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    add_button = tk.Button(movie_entry_frame, text="Add Movie", command=add_movie)
    add_button.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

    # Search Bar + Button
    search_frame = tk.Frame(main_frame)
    search_frame.pack(pady=ui_settings["element_spacing"])

    search_entry = tk.Entry(search_frame, width=40)
    search_entry.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

    def search_movie():
        query = search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a movie name to search!")
            return

        results = tmdb_api.search_movie(query)
        if not results:
            messagebox.showinfo("Info", "No results found.")
            return

        # Create a selection window for results
        search_window = tk.Toplevel(root)
        search_window.title("Search Results")
        search_window.geometry("400x300")

        result_listbox = tk.Listbox(search_window, height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
        result_listbox.pack(pady=ui_settings["element_spacing"])

        for movie in results:
            result_listbox.insert(tk.END, movie)

        def add_selected_movie():
            selected = result_listbox.curselection()
            if selected:
                movie = result_listbox.get(selected[0])
                movie_data.movies_to_watch.append(movie)
                movie_data.save_data()
                load_movies()
                search_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a movie!")

        add_result_button = tk.Button(search_window, text="Add Selected Movie", command=add_selected_movie)
        add_result_button.pack(pady=ui_settings["element_spacing"])

    search_button = tk.Button(search_frame, text="Search & Add Movie", command=search_movie)
    search_button.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

    # Remove Movie Button
    def remove_movie():
        selected_to_watch = to_watch_listbox.curselection()
        selected_watched = watched_listbox.curselection()

        if selected_to_watch:
            movie = to_watch_listbox.get(selected_to_watch[0])
            movie_data.movies_to_watch.remove(movie)
            movie_data.save_data()
            load_movies()
        elif selected_watched:
            movie = watched_listbox.get(selected_watched[0])
            movie_data.movies_watched.remove(movie)
            movie_data.save_data()
            load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to remove!")

    remove_button = tk.Button(main_frame, text="Remove Movie", command=remove_movie)
    remove_button.pack(pady=ui_settings["element_spacing"])

    # Mark as Watched Button
    def mark_as_watched():
        selected = to_watch_listbox.curselection()
        if selected:
            movie = to_watch_listbox.get(selected[0])
            movie_data.movies_to_watch.remove(movie)
            movie_data.movies_watched.append(movie)
            movie_data.save_data()
            load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to mark as watched!")

    watched_button = tk.Button(main_frame, text="Mark as Watched", command=mark_as_watched)
    watched_button.pack(pady=ui_settings["element_spacing"])

    # Un-Watch Button
    def unwatch_movie():
        selected = watched_listbox.curselection()
        if selected:
            movie = watched_listbox.get(selected[0])
            movie_data.movies_watched.remove(movie)
            movie_data.movies_to_watch.append(movie)
            movie_data.save_data()
            load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to un-watch!")

    unwatch_button = tk.Button(main_frame, text="Un-Watch", command=unwatch_movie)
    unwatch_button.pack(pady=ui_settings["element_spacing"])

    # Settings Button
    def open_settings():
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")
        settings_window.geometry("400x400")

        tk.Label(settings_window, text="Font Size:").pack(pady=ui_settings["element_spacing"])
        font_size_entry = tk.Entry(settings_window)
        font_size_entry.insert(0, ui_settings["font_size"])
        font_size_entry.pack(pady=ui_settings["element_spacing"])

        tk.Label(settings_window, text="Element Spacing:").pack(pady=ui_settings["element_spacing"])
        element_spacing_entry = tk.Entry(settings_window)
        element_spacing_entry.insert(0, ui_settings["element_spacing"])
        element_spacing_entry.pack(pady=ui_settings["element_spacing"])

        tk.Label(settings_window, text="Listbox Height:").pack(pady=ui_settings["element_spacing"])
        listbox_height_entry = tk.Entry(settings_window)
        listbox_height_entry.insert(0, ui_settings["listbox_height"])
        listbox_height_entry.pack(pady=ui_settings["element_spacing"])

        tk.Label(settings_window, text="Listbox Width:").pack(pady=ui_settings["element_spacing"])
        listbox_width_entry = tk.Entry(settings_window)
        listbox_width_entry.insert(0, ui_settings["listbox_width"])
        listbox_width_entry.pack(pady=ui_settings["element_spacing"])

        tk.Label(settings_window, text="Window Width:").pack(pady=ui_settings["element_spacing"])
        window_width_entry = tk.Entry(settings_window)
        window_width_entry.insert(0, ui_settings["window_width"])
        window_width_entry.pack(pady=ui_settings["element_spacing"])

        tk.Label(settings_window, text="Window Height:").pack(pady=ui_settings["element_spacing"])
        window_height_entry = tk.Entry(settings_window)
        window_height_entry.insert(0, ui_settings["window_height"])
        window_height_entry.pack(pady=ui_settings["element_spacing"])

        def save_settings():
            ui_settings["font_size"] = int(font_size_entry.get())
            ui_settings["element_spacing"] = int(element_spacing_entry.get())
            ui_settings["listbox_height"] = int(listbox_height_entry.get())
            ui_settings["listbox_width"] = int(listbox_width_entry.get())
            ui_settings["window_width"] = int(window_width_entry.get())
            ui_settings["window_height"] = int(window_height_entry.get())
            save_settings_to_file()
            update_ui()
            settings_window.destroy()
            messagebox.showinfo("Settings", "Settings have been updated.")

        save_button = tk.Button(settings_window, text="Save Settings", command=save_settings)
        save_button.pack(pady=ui_settings["element_spacing"])

    settings_button = tk.Button(main_frame, text="Settings", command=open_settings)
    settings_button.pack(pady=ui_settings["element_spacing"])

    # Update UI elements in real-time
    def update_ui():
        root.geometry(f"{ui_settings['window_width']}x{ui_settings['window_height']}")
        label_to_watch.config(font=("Arial", ui_settings["font_size"]))
        label_watched.config(font=("Arial", ui_settings["font_size"]))
        to_watch_listbox.config(height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
        watched_listbox.config(height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
        add_button.config(pady=ui_settings["element_spacing"])
        search_button.config(pady=ui_settings["element_spacing"])
        remove_button.config(pady=ui_settings["element_spacing"])
        watched_button.config(pady=ui_settings["element_spacing"])
        unwatch_button.config(pady=ui_settings["element_spacing"])
        settings_button.config(pady=ui_settings["element_spacing"])

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    run_gui()
