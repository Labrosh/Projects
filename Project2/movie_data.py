import json
import os
import requests
from api.tmdb_api import BASE_URL, TMDB_API_KEY
from models.movie import Movie

class MovieDataManager:
    def __init__(self):
        self.movies_to_watch = []
        self.movies_watched = []
        self.load_data()

    def add_movie(self, movie, poster_url=None):
        movie_title = movie.strip().lower()
        for m in self.movies_to_watch:
            if m['title'].lower() == movie_title:
                self.movies_to_watch.remove(m)
                self.movies_watched.append(m)
                print(f"'{m['title']}' has been moved to your 'watched' list!")
                break
        else:
            print(f"'{movie}' is not in your 'to watch' list.")

    def remove_movie(self):
        print("\nMovies to Watch:")
        for i, movie in enumerate(self.movies_to_watch, 1):
            print(f"{i}. {movie['title']}")
        print("\nMovies Watched:")
        for i, movie in enumerate(self.movies_watched, 1):
            print(f"{i + len(self.movies_to_watch)}. {movie['title']}")
        
        choice = input("Enter the number of the movie to remove, or press Enter to skip: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.movies_to_watch):
                movie = self.movies_to_watch.pop(index)
                print(f"'{movie['title']}' has been removed from your 'to watch' list!")
            elif len(self.movies_to_watch) <= index < len(self.movies_to_watch) + len(self.movies_watched):
                movie = self.movies_watched.pop(index - len(self.movies_to_watch))
                print(f"'{movie['title']}' has been removed from your 'watched' list!")
            else:
                print("Invalid choice.")
        else:
            print("No movie removed.")

    def mark_as_watched(self):
        if not self.movies_to_watch:
            print("Your 'to watch' list is empty.")
            return

        print("\nMovies to Watch:")
        for i, movie in enumerate(self.movies_to_watch, 1):
            print(f"{i}. {movie['title']}")

        choice = input("Enter the number of the movie you've watched, or press Enter to cancel: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.movies_to_watch):
                movie = self.movies_to_watch.pop(index)
                self.movies_watched.append(movie)
                print(f"'{movie['title']}' has been moved to your 'watched' list!")
            else:
                print("Invalid choice.")
        else:
            print("No movie marked as watched.")

    def view_lists(self):
        print("\nMovies to Watch:")
        for movie in self.movies_to_watch:
            print(f"- {movie['title']}")
        print("\nMovies Watched:")
        for movie in self.movies_watched:
            print(f"- {movie['title']}")
        print()

    def save_data(self):
        with open("movies.json", "w") as file:
            json.dump({"to_watch": self.movies_to_watch, "watched": self.movies_watched}, file)
        print("Your lists and details have been saved!")

    def load_data(self):
        try:
            with open("movies.json", "r") as file:
                data = json.load(file)
                self.movies_to_watch = data.get("to_watch", [])
                self.movies_watched = data.get("watched", [])
                print("Lists loaded successfully!")
        except FileNotFoundError:
            print("No saved data found. Starting fresh.")

    def save_poster(self, movie):
        return movie.save_poster()

    def save_movie_details(self, movie):
        return movie.fetch_details()

    def get_movie_details(self, movie_id):
        for movie in self.movies_to_watch + self.movies_watched:
            if movie['id'] == movie_id:
                return movie.get('details')
        return None
