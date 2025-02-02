import tkinter as tk
from tkinter import messagebox
import movie_data  # Import movie functions
import tmdb_api  # Import TMDb API functions

def run_gui():
    """Initialize the GUI window."""
    root = tk.Tk()
    root.title("Movielog - Movie Tracker")
    root.geometry("600x900")

    # Label - "To Watch" List
    label_to_watch = tk.Label(root, text="Movies to Watch", font=("Arial", 16))
    label_to_watch.pack(pady=5)

    # Movie Listbox - "To Watch"
    to_watch_listbox = tk.Listbox(root, height=10, width=50)
    to_watch_listbox.pack(pady=5)

    # Label - "Watched" List
    label_watched = tk.Label(root, text="Movies Watched", font=("Arial", 16))
    label_watched.pack(pady=5)

    # Movie Listbox - "Watched"
    watched_listbox = tk.Listbox(root, height=10, width=50)
    watched_listbox.pack(pady=5)

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
    movie_entry = tk.Entry(root, width=40)
    movie_entry.pack(pady=5)

    def add_movie():
        movie = movie_entry.get().strip()
        if movie:
            movie_data.movies_to_watch.append(movie)
            movie_data.save_data()
            load_movies()
            movie_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Movie name cannot be empty!")

    add_button = tk.Button(root, text="Add Movie", command=add_movie)
    add_button.pack(pady=5)

    # Search Bar + Button
    search_entry = tk.Entry(root, width=40)
    search_entry.pack(pady=5)

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

        result_listbox = tk.Listbox(search_window, height=10, width=50)
        result_listbox.pack(pady=5)

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
        add_result_button.pack(pady=5)

    search_button = tk.Button(root, text="Search & Add Movie", command=search_movie)
    search_button.pack(pady=5)

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

    remove_button = tk.Button(root, text="Remove Movie", command=remove_movie)
    remove_button.pack(pady=5)

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

    watched_button = tk.Button(root, text="Mark as Watched", command=mark_as_watched)
    watched_button.pack(pady=5)

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

    unwatch_button = tk.Button(root, text="Un-Watch", command=unwatch_movie)
    unwatch_button.pack(pady=5)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    run_gui()
