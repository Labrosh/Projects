import json

# Initialize movie lists
movies_to_watch = []
movies_watched = []

def add_movie():
    movie = input("Enter the name of the movie: ").strip()
    movies_to_watch.append(movie)
    print(f"'{movie}' has been added to your 'to watch' list!")

def mark_as_watched():
    movie = input("Enter the name of the movie you've watched: ").strip()
    if movie in movies_to_watch:
        movies_to_watch.remove(movie)
        movies_watched.append(movie)
        print(f"'{movie}' has been moved to your 'watched' list!")
    else:
        print(f"'{movie}' is not in your 'to watch' list.")

def view_lists():
    print("\nMovies to Watch:")
    for movie in movies_to_watch:
        print(f"- {movie}")
    print("\nMovies Watched:")
    for movie in movies_watched:
        print(f"- {movie}")
    print()

def save_data():
    with open("movies.json", "w") as file:
        json.dump({"to_watch": movies_to_watch, "watched": movies_watched}, file)
    print("Your lists have been saved!")

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

def main():
    load_data()
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a movie to 'to watch'")
        print("2. Mark a movie as 'watched'")
        print("3. View movie lists")
        print("4. Save and exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            mark_as_watched()
        elif choice == "3":
            view_lists()
        elif choice == "4":
            save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()