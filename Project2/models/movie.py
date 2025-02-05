# This file defines the Movie class. It encapsulates all logic and behavior for a single movie object.

import os
import requests
import logging
from api.tmdb_api import BASE_URL, TMDB_API_KEY

class Movie:
    def __init__(self, id, title, release_date, poster_path=None, details=None):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.poster_path = poster_path
        self.details = details
        self.user_ratings = []  # List of user ratings

    def __repr__(self):
        return f"<Movie {self.title}>"

    def save_poster(self):
        if self.poster_path and self.poster_path.startswith("http"):
            try:
                os.makedirs("data/posters", exist_ok=True)
                poster_filename = f"{self.title.replace(' ', '_')}.jpg"
                poster_file = os.path.join("data/posters", poster_filename)
                response = requests.get(self.poster_path, stream=True)
                if response.status_code == 200:
                    with open(poster_file, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    self.poster_path = poster_filename
                    return poster_file
            except Exception as e:
                logging.error(f"Failed to save poster: {e}")
        return None

    def fetch_details(self):
        # Fetch movie details from TMDb API
        url = f"{BASE_URL}/movie/{self.id}?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            self.details = response.json()
            return self.details
        return None

    def get_poster_path(self):
        if not self.poster_path:
            return None
        if self.poster_path.startswith("http"):
            return self.poster_path
        return os.path.join("data/posters", self.poster_path)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "poster_path": self.poster_path,
            "details": self.details,
            "user_ratings": self.user_ratings  # Add this line to save ratings
        }

    def add_rating(self, rating, user="default"):
        """Add a user rating (1-10)"""
        if 1 <= rating <= 10:
            self.user_ratings.append({"user": user, "rating": rating})
            return True
        return False

    def get_average_user_rating(self):
        """Get average user rating"""
        if not self.user_ratings:
            return None
        return sum(r["rating"] for r in self.user_ratings) / len(self.user_ratings)

    def clear_ratings(self):
        """Clear all user ratings"""
        self.user_ratings = []
        return True
