# Movielog

A desktop application to help organize and manage movie nights with friends. Built with Python and TMDb API integration.

## 🎯 Purpose

Created to simplify movie night organization by:
- Tracking which movies the group wants to watch
- Keeping record of watched movies and ratings
- Making it easy to find new movies through TMDb search
- Learning modern Python development practices

## 🚀 Features

- **Movie Management**
  - Search movies through TMDb's extensive database
  - Create watchlists for future movie nights
  - Track which movies you've watched
  - Rate and review watched movies

- **User Interface**
  - Modern, easy-to-use GUI
  - Movie poster previews
  - Quick search functionality
  - Customizable interface themes

- **Data Handling**
  - Automatic poster downloads
  - Local data storage
  - Backup system for saved data
  - TMDb API integration

## 🛠️ Technical Details

Built using:
- Python 3.12+
- TMDb API for movie data
- Tkinter for GUI
- JSON for data storage
- Requests for API communication

## 📦 Installation

### Option 1: Windows Users (Easiest)
1. Download the latest release
2. Run `Movielog.exe`
3. On first run, you'll be prompted to enter your TMDb API key

### Option 2: From Source
1. Ensure Python 3.12+ is installed
2. Clone the repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run `setup.bat` (Windows) or `setup.sh` (Linux/Mac)

## 🔑 Getting a TMDb API Key

1. Visit [TMDb's website](https://www.themoviedb.org/signup) and create an account
2. Go to your [API settings](https://www.themoviedb.org/settings/api)
3. Request an API key for non-commercial use
4. Copy your API key
5. You can enter the key in one of three ways:
   - Through the settings menu in the application
   - Using the setup script during first run
   - Setting the `TMDB_API_KEY` environment variable

## 🔒 API Key Security

Your TMDb API key is sensitive information. The application stores it securely:
- In your user home directory: `~/.movielog/settings.json`
- Or as an environment variable: `TMDB_API_KEY`

⚠️ Never:
- Commit your API key to version control
- Share your settings.json file
- Post your API key online

If you suspect your key is compromised:
1. Regenerate it on TMDb's website
2. Update it in the application settings

## 🌐 Offline Usage & No API Key

You can use Movielog without a TMDb API key, but with limited features:

### Available Offline Features
- View and manage existing movie lists
- Add movies manually
- Rate and review movies
- Use the backup system
- Manage saved posters

### Disabled Features Without API
- Movie search
- Automatic poster downloads
- Fetching movie details

To skip API setup and use offline mode:
1. Launch the application normally
2. Click "Skip" when prompted for API key
3. Or use `--offline` flag when launching: `./run.sh --offline`

💡 **Tip**: You can always add an API key later through the settings menu!

## 🎮 Usage

### First Time Setup
1. Launch the application:
   - Windows: Double-click `Movielog.exe` or `run.bat`
   - Linux/Mac: Run `./run.sh`
2. If no API key is found, you'll be prompted to enter it
3. The key will be saved for future use

### Basic Usage
1. Click "Search" to find movies
2. Use "+" to add movies to your watchlist
3. Rate movies after watching them
4. Use the backup feature to save your data
