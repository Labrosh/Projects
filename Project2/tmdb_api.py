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
    """Search for a movie using the TMDb API."""
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Error: Failed to fetch data from TMDb.")
        return None

    data = response.json()
    results = data.get("results", [])
    
    if not results:
        print("No results found.")
        return None

    print("\nSearch Results:")
    for i, movie in enumerate(results[:5], 1):  # Show top 5 results
        title = movie.get("title", "Unknown Title")
        release_date = movie.get("release_date", "Unknown Release Date")
        print(f"{i}. {title} ({release_date})")

    # Let the user pick a movie to add to the watchlist
    choice = input("\nEnter the number of the movie to add to your 'to watch' list, or press Enter to skip: ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(results):
            selected_movie = results[index]
            return selected_movie.get("title", "Unknown Title")
        else:
            print("Invalid choice.")
    return None
