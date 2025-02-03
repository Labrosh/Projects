# This file defines the Movie class. It encapsulates all logic and behavior for a single movie object.

import os
import requests
from api.tmdb_api import BASE_URL, TMDB_API_KEY

class Movie:
    def __init__(self, id, title, release_date, poster_path=None, details=None):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.poster_path = poster_path
        self.details = details

    def __repr__(self):
        return f"<Movie {self.title}>"

    def save_poster(self):
        if self.poster_path and self.poster_path.startswith("http"):
            os.makedirs("data/posters", exist_ok=True)
            poster_filename = f"{self.title.replace(' ', '_')}.jpg"
            poster_file = os.path.join("data/posters", poster_filename)
            response = requests.get(self.poster_path, stream=True)
            if response.status_code == 200:
                with open(poster_file, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                self.poster_path = poster_filename  # Save only the filename
            return poster_file
        return None

    def get_poster_path(self):
        if self.poster_path and not os.path.isabs(self.poster_path):
            return os.path.join("data/posters", self.poster_path)
        return self.poster_path

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "poster_path": self.poster_path,
            "details": self.details,
        }
