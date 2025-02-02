# Project2

## Overview
This project is a movie logging application that allows users to search for movies using the TMDb API, add them to a watchlist, mark them as watched, and view their lists. The project includes a graphical user interface (GUI) and an optional command-line interface (CLI).

## Project Structure
```
Project2/
│── gui.py
│── tmdb_api.py
│── movie_data.py
│── tests/
│   ├── test_movie_data.py
│   ├── test_tmdb_api.py
│   ├── test_gui.py (optional, later)
│── README.md
│── settings.json (generated after first run)
```

## Files
- **gui.py**: Script for the graphical user interface.
- **tmdb_api.py**: Script to interact with the TMDb API.
- **movie_data.py**: Script to manage movie lists.
- **tests/**: Directory containing test scripts.

## Setup
1. Clone the repository.
2. Install the required packages.
3. Set the `TMDB_API_KEY` environment variable with your TMDb API key.

## Usage
Run the GUI script to start the application:
```bash
python gui.py
```

## Running Tests
To run the tests, use the following command:
```bash
python -m unittest discover -s tests
```
