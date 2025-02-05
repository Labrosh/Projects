@echo off
echo Welcome to Movielog Setup
echo ========================

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.12+ is required but not found!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: API Key setup
if not defined TMDB_API_KEY (
    echo.
    echo You'll need a TMDb API key to use all features.
    echo Visit https://www.themoviedb.org/settings/api to get one.
    echo Or you can skip this step to use offline features only.
    echo.
    set /p API_INPUT="Enter your TMDb API key (or type 'skip'): "
    
    if /i not "%API_INPUT%"=="skip" (
        set TMDB_API_KEY=%API_INPUT%
        echo {"tmdb_api_key": "%TMDB_API_KEY%"} > gui/settings.json
    ) else (
        echo {"offline_mode": true} > gui/settings.json
        echo Setup complete in offline mode!
    )
)

echo.
echo Setup complete! You can now run the application using run.bat
pause
