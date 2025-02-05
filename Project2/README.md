# Project2

## Overview
This project is a movie logging application that allows users to search for movies using the TMDb API, add them to a watchlist, mark them as watched, and view their lists. The project features a modern graphical user interface (GUI) with customizable settings.

## Project Structure
```
Project2/
├── api/
│   └── tmdb_api.py          # TMDb API integration
├── data/
│   ├── movies.json          # User's movie data
│   ├── settings.json        # Application settings
│   └── posters/             # Downloaded movie posters
├── gui/
│   ├── widgets/             # Custom GUI widgets
│   ├── color_scheme.py      # UI theming
│   ├── gui.py               # Main GUI implementation
│   ├── gui_helper.py        # GUI utility functions
│   ├── gui_movie_list.py    # Movie list view
│   ├── gui_search.py        # Search interface
│   └── gui_settings.py      # Settings interface
├── models/
│   ├── manager.py           # Data management
│   └── movie.py             # Movie data model
└── requirements.txt         # Project dependencies
```

## Dependencies
Install required packages using:
```bash
pip install -r requirements.txt
```

## Configuration
1. Set up your TMDb API key:
   - Create an account on TMDb and get your API key
   - Set the `TMDB_API_KEY` environment variable
   - Or configure it through the settings interface

## Usage
Run the application:
```bash
python -m gui.gui
```

## Features
- Movie search with TMDb integration
- Watchlist management
- Movie progress tracking
- Customizable interface
- Poster downloads and caching
- Settings persistence

## Data Storage
- Movie data is stored in `data/movies.json`
- Application settings in `data/settings.json`
- Movie posters are cached in `data/posters/`
