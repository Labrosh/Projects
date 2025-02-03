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
        if not any(m.id == movie.id for m in self.movies_to_watch + self.movies_watched):
            self.movies_to_watch.append(movie)
            self.save_data()

    def remove_movie(self, movie):
        self.movies_to_watch = [m for m in self.movies_to_watch if m.id != movie.id]
        self.movies_watched = [m for m in self.movies_watched if m.id != movie.id]
        self.save_data()

    def mark_as_watched(self, movie):
        if movie in self.movies_to_watch:
            self.movies_to_watch.remove(movie)
            self.movies_watched.append(movie)
            self.save_data()

    def unwatch_movie(self, movie):
        if movie in self.movies_watched:
            self.movies_watched.remove(movie)
            self.movies_to_watch.append(movie)
            self.save_data()

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump({
                "to_watch": [m.to_dict() for m in self.movies_to_watch],
                "watched": [m.to_dict() for m in self.movies_watched],
            }, file, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.movies_to_watch = [Movie(**m) for m in data.get("to_watch", [])]
                self.movies_watched = [Movie(**m) for m in data.get("watched", [])]
        else:
            self.movies_to_watch = []
            self.movies_watched = []
