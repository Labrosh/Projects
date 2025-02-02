import os
from tmdb_api import search_movie
from movie_data import add_movie, mark_as_watched, view_lists, save_data, load_data

# Check for API key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    print("Error: TMDb API key not found. Set it as an environment variable and try again.")
    exit(1)

print("Your API key is set and ready to use.")

def main():
    """Main function to run the movie log application."""
    load_data()
    while True:
        print("\nMenu:")
        print("1. Search for a movie")
        print("2. Mark a movie as watched")
        print("3. View movie lists")
        print("4. Save and exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            query = input("Enter the movie name to search: ").strip()
            movie = search_movie(query)
            if movie:
                add_movie(movie)
        elif choice == "2":
            mark_as_watched()
        elif choice == "3":
            view_lists()
        elif choice == "4":
            save_data()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()