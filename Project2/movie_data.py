import json

movies_to_watch = []
movies_watched = []

def add_movie(movie):
    """Add a movie to the watched list."""
    movie = movie.strip().lower()
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
