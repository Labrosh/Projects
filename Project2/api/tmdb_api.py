import os
import requests
import logging

# Constants
TESTING_OFFLINE = True  # Toggle this for testing
TMDB_API_KEY = None if TESTING_OFFLINE else os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_ATTRIBUTION = """
Powered by TMDb
This product uses the TMDb API but is not endorsed or certified by TMDb.
"""

# Use logging instead of print
if not TMDB_API_KEY:
    logging.info("No TMDb API key found - starting in offline mode")

class TMDbAPI:
    @staticmethod
    def set_api_key(key):
        global TMDB_API_KEY
        TMDB_API_KEY = key

    @staticmethod
    def validate_api_key(key):
        """Test if an API key is valid"""
        url = f"{BASE_URL}/authentication/token/new"
        params = {"api_key": key}
        try:
            response = requests.get(url, params=params)
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def search_movie(query):
        """Search for a movie using the TMDb API and return a list of results."""
        if not TMDB_API_KEY:
            logging.debug("Search attempted without API key")
            return []  # Return an empty list if no API key is present

        url = f"{BASE_URL}/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": query}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return []  # Return empty list if API fails

        data = response.json()
        results = data.get("results", [])

        return [{
            "id": movie.get('id'),
            "title": movie.get('title', 'Unknown Title'),
            "release_date": movie.get('release_date', 'Unknown Release Date'),
            "poster_path": f"{IMAGE_BASE_URL}{movie.get('poster_path')}" if movie.get('poster_path') else None
        } for movie in results[:5]]  # Return top 5 results as a list

    @staticmethod
    def get_movie_details(movie_id):
        """Fetch detailed information for a movie."""
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ConnectionError("Failed to fetch movie details.")

        return response.json()
        return response.json()

