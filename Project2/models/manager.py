# This file defines the MovieManager class. It handles loading, saving, and managing lists of movies.

import json
import os
from models.movie import Movie

class MovieManager:
    def __init__(self, data_file="data/movies.json"):
        self.data_file = data_file
        self.movies_to_watch = []
        self.movies_watched = []
        self.load_data()

    def add_movie(self, movie):
        if not any(m.movie_id == movie.movie_id for m in self.movies_to_watch + self.movies_watched):
            self.movies_to_watch.append(movie)
            self.save_data()

    def remove_movie(self, movie):
        self.movies_to_watch = [m for m in self.movies_to_watch if m.movie_id != movie.movie_id]
        self.movies_watched = [m for m in self.movies_watched if m.movie_id != movie.movie_id]
        self.save_data()

    def mark_as_watched(self, movie):
        if movie in self.movies_to_watch:
            self.movies_to_watch.remove(movie)
            self.movies_watched.append(movie)
            self.save_data()

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump({
                "to_watch": [m.__dict__ for m in self.movies_to_watch],
                "watched": [m.__dict__ for m in self.movies_watched]
            }, file, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.movies_to_watch = [Movie(**m) for m in data.get("to_watch", [])]
                self.movies_watched = [Movie(**m) for m in data.get("watched", [])]