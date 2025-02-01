# Dungeon Game

Welcome to the Dungeon Game! This is a text-based adventure game where you explore a dungeon, collect items, and try to find the exit.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Gameplay](#gameplay)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Dungeon Game is a text-based adventure game developed by [Labrosh](https://github.com/Labrosh). The game generates a dungeon with multiple rooms, items, and locked doors. Your goal is to explore the dungeon, collect items, and find the exit.

## Features

- Randomly generated dungeon with multiple rooms
- Items to collect and use
- Locked doors that require keys to open
- Clues to help you find the exit phrase
- Interactive map of the dungeon

## Requirements

- Python 3.8 or higher

## Installation

To install the Dungeon Game, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/Labrosh/Project1.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Project1
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start the game, run the following command:
```sh
python main.py
```

### Commands

- `look`: Describe the current room
- `inventory` or `inv`: Show your inventory
- `north` or `n`, `south` or `s`, `east` or `e`, `west` or `w`: Move in the specified direction
- `pick [item name]`: Pick up an item
- `examine`: Examine items in your inventory
- `map`: Show the dungeon map
- `quit`, `q`, or `exit`: Quit the game

## Gameplay

In Dungeon Game, you will navigate through a series of rooms in a dungeon. Each room may contain items, clues, and locked doors. Your objective is to find the exit by collecting keys and solving clues. Use the commands to interact with the game and explore the dungeon.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
