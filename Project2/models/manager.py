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
        """Add a movie or update if it already exists"""
        # Check if movie exists in either list
        for existing in self.movies_to_watch + self.movies_watched:
            if existing.title.lower() == movie.title.lower():
                # If we're adding a movie with details to replace one without details
                if existing.needs_details and not movie.needs_details:
                    logging.debug(f"Replacing movie without details: {existing.title}")
                    # Remove from appropriate list
                    if existing in self.movies_to_watch:
                        self.movies_to_watch.remove(existing)
                    else:
                        self.movies_watched.remove(existing)
                    # Add new version to to_watch
                    self.movies_to_watch.append(movie)
                    self.save_data()
                    return True
                return False
        
        # If movie doesn't exist, add it normally
        self.movies_to_watch.append(movie)
        self.save_data()
        return True

    def remove_movie(self, movie):
        """Remove a specific movie from either list"""
        if movie in self.movies_to_watch:
            self.movies_to_watch.remove(movie)
        elif movie in self.movies_watched:
            self.movies_watched.remove(movie)
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
                json.dump(data, file, indent=2)
            return True
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
            raise

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                    # Handle to_watch movies
                    self.movies_to_watch = []
                    for movie_data in data.get("to_watch", []):
                        user_ratings = movie_data.pop('user_ratings', [])
                        needs_details = movie_data.pop('needs_details', True)
                        movie = Movie(
                            id=movie_data.get('id'),
                            title=movie_data['title'],
                            release_date=movie_data.get('release_date'),
                            poster_path=movie_data.get('poster_path'),
                            details=movie_data.get('details')
                        )
                        movie.user_ratings = user_ratings
                        movie.needs_details = needs_details
                        self.movies_to_watch.append(movie)
                    
                    # Handle watched movies (similar process)
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
                
                return True
        except Exception as e:
            logging.error(f"Error loading movies: {e}")
            raise
        return False

    def get_movie_details(self, movie_id):
        for movie in self.movies_to_watch + self.movies_watched:
            if movie.id == movie_id:
                return movie.details
        return None

    def update_movie(self, old_movie, new_movie):
        """Update an existing movie with new details"""
        logging.debug(f"Attempting to update movie: {old_movie.title} -> {new_movie.title}")
        
        # First try to find by exact object
        if old_movie in self.movies_to_watch:
            idx = self.movies_to_watch.index(old_movie)
            self.movies_to_watch[idx] = new_movie
            logging.debug("Updated movie in to_watch list (exact match)")
            self.save_movies()
            return True
            
        if old_movie in self.movies_watched:
            idx = self.movies_watched.index(old_movie)
            self.movies_watched[idx] = new_movie
            logging.debug("Updated movie in watched list (exact match)")
            self.save_movies()
            return True
            
        # If exact match fails, try matching by title
        for i, movie in enumerate(self.movies_to_watch):
            if movie.title.lower() == old_movie.title.lower():
                self.movies_to_watch[i] = new_movie
                logging.debug("Updated movie in to_watch list (title match)")
                self.save_movies()
                return True
                
        for i, movie in enumerate(self.movies_watched):
            if movie.title.lower() == old_movie.title.lower():
                self.movies_watched[i] = new_movie
                logging.debug("Updated movie in watched list (title match)")
                self.save_movies()
                return True
                
        logging.error(f"Failed to find movie to update: {old_movie.title}")
        return False
