# Movielog

An elegant desktop application for organizing movie nights with friends. Track your watchlist, rate movies, and discover new films through TMDb integration.

## 🎬 Quick Start

```bash
# Install from PyPI
pip install movielog

# Or install from source
git clone https://github.com/yourusername/movielog.git
cd movielog
pip install -e .

# Run the application
movielog
```

## ✨ Features

### Movie Management
- Search TMDb's extensive movie database
- Maintain watchlist and watched movies
- Rate and review watched films
- Automatic poster downloads

### User Experience
- Modern, customizable interface
- Dark and light themes
- Offline mode support
- Secure API key storage

### Data Handling
- Local data storage in `~/.movielog/`
- Automatic backup system
- Poster caching
- Safe settings management

## 🔧 Development Setup

### Prerequisites
- Python 3.12+
- git
- pip

### Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python -m unittest discover tests
```

## 🔑 API Configuration

### Getting a TMDb API Key
1. Create account: [TMDb Signup](https://www.themoviedb.org/signup)
2. Get API key: [API Settings](https://www.themoviedb.org/settings/api)
3. Set key via:
   - Application settings menu
   - Environment variable: `TMDB_API_KEY`
   - First-run setup

### Security Notes
- API key stored in `~/.movielog/settings.json`
- Directory permissions: 700 (user-only)
- Settings file permissions: 600 (user-only)

## 🌐 Offline Mode

Enable offline mode by:
- Skipping API key entry
- Using `--offline` flag
- Through settings menu

Limitations:
- No movie search
- No poster downloads
- No new movie details

## 📁 Project Structure

```
movielog/
├── api/          # TMDb API integration
├── gui/          # User interface components
│   └── widgets/  # Reusable UI elements
├── models/       # Data models
└── utils/        # Helper utilities
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [TMDb](https://www.themoviedb.org/) for their excellent API
- Python tkinter community
- All contributors and users
