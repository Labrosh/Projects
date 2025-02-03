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
        data = {
            "to_watch": [movie.to_dict() for movie in self.movies_to_watch],
            "watched": [movie.to_dict() for movie in self.movies_watched]
        }
        with open(self.data_file, "w") as file:
            json.dump(data, file)

    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.movies_to_watch = [Movie(**movie) for movie in data.get("to_watch", [])]
                self.movies_watched = [Movie(**movie) for movie in data.get("watched", [])]
        except FileNotFoundError:
            pass

    def get_movie_details(self, movie_id):
        for movie in self.movies_to_watch + self.movies_watched:
            if movie.id == movie_id:
                return movie.details
        return None
