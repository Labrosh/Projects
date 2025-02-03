import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import os

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
