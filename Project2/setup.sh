#!/bin/bash

echo "Welcome to Movielog Setup"
echo "========================"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Python 3.12+ is required but not found!"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Install requirements
echo "Installing dependencies..."
pip3 install -r requirements.txt

# API Key setup
if [ -z "$TMDB_API_KEY" ]; then
    echo
    echo "You'll need a TMDb API key to use all features."
    echo "Visit https://www.themoviedb.org/settings/api to get one."
    echo "Or you can skip this step to use offline features only."
    echo
    read -p "Enter your TMDb API key (or type 'skip'): " API_INPUT
    
    if [ "$API_INPUT" != "skip" ]; then
        TMDB_API_KEY=$API_INPUT
        echo "{\"tmdb_api_key\": \"$TMDB_API_KEY\"}" > gui/settings.json
    else
        echo "{\"offline_mode\": true}" > gui/settings.json
        echo "Setup complete in offline mode!"
    fi
fi

echo
echo "Setup complete! You can now run the application using ./run.sh"
