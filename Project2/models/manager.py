# This file defines the MovieManager class. It handles loading, saving, and managing lists of movies.

import json
import os
import logging
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

    def save_movies(self):
        """Save movies to JSON file (alias for save_data for consistency)"""
        return self.save_data()

    def save_data(self):
        """Save movies to JSON file"""
        try:
            data = {
                "to_watch": [movie.to_dict() for movie in self.movies_to_watch],
                "watched": [movie.to_dict() for movie in self.movies_watched]
            }
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w") as file:
                json.dump(data, file)
            return True
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
            return False

    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
                
                # Handle to_watch movies
                for movie_data in data.get("to_watch", []):
                    user_ratings = movie_data.pop('user_ratings', [])  # Remove and store ratings
                    movie = Movie(
                        id=movie_data['id'],
                        title=movie_data['title'],
                        release_date=movie_data['release_date'],
                        poster_path=movie_data['poster_path'],
                        details=movie_data['details']
                    )
                    movie.user_ratings = user_ratings  # Set ratings after creation
                    self.movies_to_watch.append(movie)
                
                # Handle watched movies
                for movie_data in data.get("watched", []):
                    user_ratings = movie_data.pop('user_ratings', [])  # Remove and store ratings
                    movie = Movie(
                        id=movie_data['id'],
                        title=movie_data['title'],
                        release_date=movie_data['release_date'],
                        poster_path=movie_data['poster_path'],
                        details=movie_data['details']
                    )
                    movie.user_ratings = user_ratings  # Set ratings after creation
                    self.movies_watched.append(movie)
        except FileNotFoundError:
            pass

    def get_movie_details(self, movie_id):
        for movie in self.movies_to_watch + self.movies_watched:
            if movie.id == movie_id:
                return movie.details
        return None
