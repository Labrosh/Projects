import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os
import json
import movie_data
import tmdb_api

# UI Settings
ui_settings = {
    "font_size": 16,
    "element_spacing": 5,
    "listbox_height": 10,
    "listbox_width": 50,
    "window_width": 600,
    "window_height": 900
}

def load_settings():
    global ui_settings
    try:
        with open("settings.json", "r") as file:
            ui_settings.update(json.load(file))
    except FileNotFoundError:
        pass

def save_settings_to_file():
    with open("settings.json", "w") as file:
        json.dump(ui_settings, file)

load_settings()

def run_gui():
    root = tk.Tk()
    root.title("Movielog - Movie Tracker")
    root.geometry(f"{ui_settings['window_width']}x{ui_settings['window_height']}")

    movie_data.load_data()

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    label_to_watch = tk.Label(main_frame, text="Movies to Watch", font=("Arial", ui_settings["font_size"]))
    label_to_watch.pack(pady=ui_settings["element_spacing"])

    to_watch_listbox = tk.Listbox(main_frame, height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
    to_watch_listbox.pack(pady=ui_settings["element_spacing"])

    label_watched = tk.Label(main_frame, text="Movies Watched", font=("Arial", ui_settings["font_size"]))
    label_watched.pack(pady=ui_settings["element_spacing"])

    watched_listbox = tk.Listbox(main_frame, height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
    watched_listbox.pack(pady=ui_settings["element_spacing"])

    def load_movies():
        to_watch_listbox.delete(0, tk.END)
        watched_listbox.delete(0, tk.END)
        for movie in movie_data.movies_to_watch:
            to_watch_listbox.insert(tk.END, movie['title'])
        for movie in movie_data.movies_watched:
            watched_listbox.insert(tk.END, movie['title'])

    movie_data.load_data()
    load_movies()

    movie_entry_frame = tk.Frame(main_frame)
    movie_entry_frame.pack(pady=ui_settings["element_spacing"])

    movie_entry = tk.Entry(movie_entry_frame, width=40)
    movie_entry.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

    def add_movie():
        movie = movie_entry.get().strip()
        if movie:
            movie_data.movies_to_watch.append({"title": movie, "release_date": "", "poster_path": "", "details": None})
            movie_data.save_data()
            load_movies()
            movie_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    add_button = tk.Button(movie_entry_frame, text="Add Movie", command=add_movie)
    add_button.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

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

        search_window = tk.Toplevel(root)
        search_window.title("Search Results")
        search_window.geometry("400x300")

        result_listbox = tk.Listbox(search_window, height=ui_settings["listbox_height"], width=ui_settings["listbox_width"])
        result_listbox.pack(pady=ui_settings["element_spacing"])

        for movie in results:
            result_listbox.insert(tk.END, f"{movie['title']} ({movie['release_date']})")

        def add_selected_movie():
            selected = result_listbox.curselection()
            if selected:
                movie = results[selected[0]]
                poster_path = movie_data.save_poster(movie)
                details = movie_data.save_movie_details(movie)
                movie_data.movies_to_watch.append({
                    "id": movie['id'],
                    "title": movie['title'],
                    "release_date": movie['release_date'],
                    "poster_path": poster_path or movie['poster_path'],
                    "details": details
                })
                movie_data.save_data()
                load_movies()
                search_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a movie!")

        def show_movie_poster(event):
            selected = result_listbox.curselection()
            if selected:
                movie = results[selected[0]]
                if movie['poster_path']:
                    poster_window = tk.Toplevel(root)
                    poster_window.title(movie['title'])
                    poster_image = Image.open(requests.get(movie['poster_path'], stream=True).raw)
                    poster_image = poster_image.resize((300, 450), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)
                    poster_label = tk.Label(poster_window, image=poster_photo)
                    poster_label.image = poster_photo
                    poster_label.pack()

        result_listbox.bind('<<ListboxSelect>>', show_movie_poster)

        add_result_button = tk.Button(search_window, text="Add Selected Movie", command=add_selected_movie)
        add_result_button.pack(pady=ui_settings["element_spacing"])

    search_button = tk.Button(search_frame, text="Search & Add Movie", command=search_movie)
    search_button.pack(side=tk.LEFT, padx=ui_settings["element_spacing"])

    def remove_movie():
        selected_to_watch = to_watch_listbox.curselection()
        selected_watched = watched_listbox.curselection()

        if selected_to_watch:
            movie = movie_data.movies_to_watch[selected_to_watch[0]]
            movie_data.movies_to_watch.remove(movie)
            movie_data.save_data()
            load_movies()
        elif selected_watched:
            movie = movie_data.movies_watched[selected_watched[0]]
            movie_data.movies_watched.remove(movie)
            movie_data.save_data()
            load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to remove!")

    remove_button = tk.Button(main_frame, text="Remove Movie", command=remove_movie)
    remove_button.pack(pady=ui_settings["element_spacing"])

    def mark_as_watched():
        selected = to_watch_listbox.curselection()
        if selected:
            movie = movie_data.movies_to_watch[selected[0]]
            movie_data.movies_to_watch.remove(movie)
            movie_data.movies_watched.append(movie)
            movie_data.save_data()
            load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to mark as watched!")

    watched_button = tk.Button(main_frame, text="Mark as Watched", command=mark_as_watched)
    watched_button.pack(pady=ui_settings["element_spacing"])

    def unwatch_movie():
        selected = watched_listbox.curselection()
        if selected:
            movie = movie_data.movies_watched[selected[0]]
            movie_data.movies_watched.remove(movie)
            movie_data.movies_to_watch.append(movie)
            movie_data.save_data()
            load_movies()
        else:
            messagebox.showwarning("Warning", "Please select a movie to un-watch!")

    unwatch_button = tk.Button(main_frame, text="Un-Watch", command=unwatch_movie)
    unwatch_button.pack(pady=ui_settings["element_spacing"])

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

    def show_movie_poster(movie):
        poster_path = movie['poster_path']
        if poster_path:
            if not poster_path.startswith("http"):
                poster_path = os.path.join("posters", os.path.basename(poster_path))
            if os.path.exists(poster_path):
                poster_window = tk.Toplevel(root)
                poster_window.title(movie['title'])
                poster_image = Image.open(poster_path)
                poster_image = poster_image.resize((300, 450), Image.LANCZOS)
                poster_photo = ImageTk.PhotoImage(poster_image)
                poster_label = tk.Label(poster_window, image=poster_photo)
                poster_label.image = poster_photo
                poster_label.pack()
            else:
                messagebox.showwarning("Warning", "Poster not found.")

    def show_movie_details(movie):
        details = movie_data.get_movie_details(movie['id'])
        if details:
            details_window = tk.Toplevel(root)
            details_window.title(movie['title'])

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

    def show_selected_movie_details():
        selected_to_watch = to_watch_listbox.curselection()
        selected_watched = watched_listbox.curselection()

        if selected_to_watch:
            movie = movie_data.movies_to_watch[selected_to_watch[0]]
            show_movie_details(movie)
        elif selected_watched:
            movie = movie_data.movies_watched[selected_watched[0]]
            show_movie_details(movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view the details!")

    view_details_button = tk.Button(main_frame, text="View Details", command=show_selected_movie_details)
    view_details_button.pack(pady=ui_settings["element_spacing"])

    def show_selected_movie_poster():
        selected_to_watch = to_watch_listbox.curselection()
        selected_watched = watched_listbox.curselection()

        if selected_to_watch:
            movie = movie_data.movies_to_watch[selected_to_watch[0]]
            show_movie_poster(movie)
        elif selected_watched:
            movie = movie_data.movies_watched[selected_watched[0]]
            show_movie_poster(movie)
        else:
            messagebox.showwarning("Warning", "Please select a movie to view the poster!")

    view_poster_button = tk.Button(main_frame, text="View Poster", command=show_selected_movie_poster)
    view_poster_button.pack(pady=ui_settings["element_spacing"])

    root.mainloop()

if __name__ == "__main__":
    run_gui()
