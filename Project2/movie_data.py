import json
import os
import requests
from tmdb_api import BASE_URL, TMDB_API_KEY

movies_to_watch = []
movies_watched = []

def add_movie(movie, poster_url=None):
    movie_title = movie.strip().lower()
    for m in movies_to_watch:
        if m['title'].lower() == movie_title:
            movies_to_watch.remove(m)
            movies_watched.append(m)
            print(f"'{m['title']}' has been moved to your 'watched' list!")
            break
    else:
        print(f"'{movie}' is not in your 'to watch' list.")

def remove_movie():
    print("\nMovies to Watch:")
    for i, movie in enumerate(movies_to_watch, 1):
        print(f"{i}. {movie['title']}")
    print("\nMovies Watched:")
    for i, movie in enumerate(movies_watched, 1):
        print(f"{i + len(movies_to_watch)}. {movie['title']}")
    
    choice = input("Enter the number of the movie to remove, or press Enter to skip: ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(movies_to_watch):
            movie = movies_to_watch.pop(index)
            print(f"'{movie['title']}' has been removed from your 'to watch' list!")
        elif len(movies_to_watch) <= index < len(movies_to_watch) + len(movies_watched):
            movie = movies_watched.pop(index - len(movies_to_watch))
            print(f"'{movie['title']}' has been removed from your 'watched' list!")
        else:
            print("Invalid choice.")
    else:
        print("No movie removed.")

def mark_as_watched():
    if not movies_to_watch:
        print("Your 'to watch' list is empty.")
        return

    print("\nMovies to Watch:")
    for i, movie in enumerate(movies_to_watch, 1):
        print(f"{i}. {movie['title']}")

    choice = input("Enter the number of the movie you've watched, or press Enter to cancel: ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(movies_to_watch):
            movie = movies_to_watch.pop(index)
            movies_watched.append(movie)
            print(f"'{movie['title']}' has been moved to your 'watched' list!")
        else:
            print("Invalid choice.")
    else:
        print("No movie marked as watched.")

def view_lists():
    print("\nMovies to Watch:")
    for movie in movies_to_watch:
        print(f"- {movie['title']}")
    print("\nMovies Watched:")
    for movie in movies_watched:
        print(f"- {movie['title']}")
    print()

def save_data():
    with open("movies.json", "w") as file:
        json.dump({"to_watch": movies_to_watch, "watched": movies_watched}, file)
    print("Your lists and details have been saved!")

def load_data():
    global movies_to_watch, movies_watched
    try:
        with open("movies.json", "r") as file:
            data = json.load(file)
            movies_to_watch = data.get("to_watch", [])
            movies_watched = data.get("watched", [])
            print("Lists loaded successfully!")
    except FileNotFoundError:
        print("No saved data found. Starting fresh.")

def save_poster(movie):
    poster_url = movie.get('poster_path')
    if poster_url:
        os.makedirs("posters", exist_ok=True)
        poster_path = os.path.join("posters", f"{movie['title'].replace(' ', '_')}.jpg")
        response = requests.get(poster_url, stream=True)
        if response.status_code == 200:
            with open(poster_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return poster_path
    return None

def save_movie_details(movie):
    movie_id = movie.get('id')
    if movie_id:
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            details = response.json()
            for m in movies_to_watch + movies_watched:
                if m['id'] == movie_id:
                    m['details'] = details
                    break
            save_data()
            return details
    return None

def get_movie_details(movie_id):
    for movie in movies_to_watch + movies_watched:
        if movie['id'] == movie_id:
            return movie.get('details')
    return None
