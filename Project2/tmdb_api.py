import os
import requests

# Constants
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
TMDB_ATTRIBUTION = """
Powered by TMDb
This product uses the TMDb API but is not endorsed or certified by TMDb.
"""

# Check for API key
if not TMDB_API_KEY:
    print("Error: TMDb API key not found. Set it as an environment variable and try again.")
    exit(1)

def search_movie(query):
    """Search for a movie using the TMDb API and return a list of results."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []  # Return empty list if API fails

    data = response.json()
    results = data.get("results", [])

    return [f"{movie.get('title', 'Unknown Title')} ({movie.get('release_date', 'Unknown Release Date')})" 
            for movie in results[:5]]  # Return top 5 results as a list
