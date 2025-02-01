# Project1

## Overview
Project1 is a text-based dungeon game where players can explore rooms, pick up items, and navigate through a dungeon. The game features a graphical map display using `matplotlib`.

## Setup
1. Clone the repository.
2. Navigate to the `Project1` directory.
3. Ensure you have Python installed.

## Dependencies
The game requires the following Python packages:
- `matplotlib`

You can install the required packages using `pip`:
```bash
pip install matplotlib
```

### Optional: `tkinter`
The game uses `tkinter` for graphical display if available. If `tkinter` is not installed, the game will fall back to console output and non-interactive plotting.

#### Installing `tkinter`
- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install python3-tk
  ```
- **Fedora**:
  ```bash
  sudo dnf install python3-tkinter
  ```
- **macOS (using Homebrew)**:
  ```bash
  brew install python-tk
  ```

## How to Run
Run the following command to start the game:
```bash
python main.py
```

## Files
- `main.py`: Entry point of the application.
- `game.py`: Contains the `Game` class which handles the main game logic.
- `player.py`: Contains the `Player` class which represents the player.
- `room.py`: Contains the `Room` class which represents a room in the dungeon.
- `item.py`: Contains the `Item` class and the `items` dictionary.
- `dungeon.py`: Contains the `Dungeon` class which generates the dungeon.
- `__init__.py`: Marks the directory as a package.

## License
This project is licensed under the MIT License.