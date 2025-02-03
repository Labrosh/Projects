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
            poster_file = os.path.join("data/posters", f"{self.title.replace(' ', '_')}.jpg")
            response = requests.get(self.poster_path, stream=True)
            if response.status_code == 200:
                with open(poster_file, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                self.poster_path = poster_file
            return poster_file
        return None

    def fetch_details(self):
        if TMDB_API_KEY:
            url = f"{BASE_URL}/movie/{self.movie_id}"
            response = requests.get(url, params={"api_key": TMDB_API_KEY})
            if response.status_code == 200:
                self.details = response.json()
        return self.details