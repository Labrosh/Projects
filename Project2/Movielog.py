import json
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

print("Your API key is set and ready to use.")

# Initialize movie lists
movies_to_watch = []
movies_watched = []

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
            movies_to_watch.append(selected_movie.get("title", "Unknown Title"))
            print(f"'{selected_movie.get('title', 'Unknown Title')}' has been added to your 'to watch' list!")
        else:
            print("Invalid choice.")

def add_movie():
    """Add a movie to the watched list."""
    movie = input("Enter the name of the movie you've watched: ").strip().lower()
    for m in movies_to_watch:
        if m.lower() == movie:
            movies_to_watch.remove(m)
            movies_watched.append(m)
            print(f"'{m}' has been moved to your 'watched' list!")
            break
    else:
        print(f"'{movie}' is not in your 'to watch' list.")

def remove_movie():
    """Remove a movie from the to watch or watched list."""
    print("\nMovies to Watch:")
    for i, movie in enumerate(movies_to_watch, 1):
        print(f"{i}. {movie}")
    print("\nMovies Watched:")
    for i, movie in enumerate(movies_watched, 1):
        print(f"{i + len(movies_to_watch)}. {movie}")
    
    choice = input("Enter the number of the movie to remove, or press Enter to skip: ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(movies_to_watch):
            movie = movies_to_watch.pop(index)
            print(f"'{movie}' has been removed from your 'to watch' list!")
        elif len(movies_to_watch) <= index < len(movies_to_watch) + len(movies_watched):
            movie = movies_watched.pop(index - len(movies_to_watch))
            print(f"'{movie}' has been removed from your 'watched' list!")
        else:
            print("Invalid choice.")
    else:
        print("No movie removed.")

def mark_as_watched():
    """Mark a movie as watched."""
    if not movies_to_watch:
        print("Your 'to watch' list is empty.")
        return

    print("\nMovies to Watch:")
    for i, movie in enumerate(movies_to_watch, 1):
        print(f"{i}. {movie}")

    choice = input("Enter the number of the movie you've watched, or press Enter to cancel: ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(movies_to_watch):
            movie = movies_to_watch.pop(index)
            movies_watched.append(movie)
            print(f"'{movie}' has been moved to your 'watched' list!")
        else:
            print("Invalid choice.")
    else:
        print("No movie marked as watched.")

def view_lists():
    """View the lists of movies to watch and watched movies."""
    print("\nMovies to Watch:")
    for movie in movies_to_watch:
        print(f"- {movie}")
    print("\nMovies Watched:")
    for movie in movies_watched:
        print(f"- {movie}")
    print()

def save_data():
    """Save the movie lists to a JSON file."""
    with open("movies.json", "w") as file:
        json.dump({"to_watch": movies_to_watch, "watched": movies_watched}, file)
    print("Your lists have been saved! Goodbye!")
    exit(0)

def load_data():
    """Load the movie lists from a JSON file."""
    global movies_to_watch, movies_watched
    try:
        with open("movies.json", "r") as file:
            data = json.load(file)
            movies_to_watch = data.get("to_watch", [])
            movies_watched = data.get("watched", [])
            print("Lists loaded successfully!")
    except FileNotFoundError:
        print("No saved data found. Starting fresh.")

def main():
    """Main function to run the movie log application."""
    load_data()
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a movie to 'to watch'")
        print("2. Mark a movie as 'watched'")
        print("3. View movie lists")
        print("4. Search for a movie (via TMDb)")
        print("5. Remove a movie from 'to watch' or 'watched'")
        print("6. Save and exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            mark_as_watched()
        elif choice == "3":
            view_lists()
        elif choice == "4":
            query = input("Enter the name of the movie to search: ").strip()
            search_movie(query)
        elif choice == "5":
            remove_movie()
        elif choice == "6":
            save_data()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()