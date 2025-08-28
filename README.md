# Browser Operating Agent

## Overview
This project is an autonomous browser agent built with Python and Playwright. It operates on the Block Champ puzzle game, automating gameplay and analyzing the board using image processing (Pillow).

## Features
- Launches and controls a browser instance
- Navigates to Block Champ on CrazyGames
- Automates drag-and-drop block moves
- Captures and analyzes the game board using screenshots
- Uses image processing to detect filled/empty cells
- Extensible for intelligent gameplay and decision logic

## Project Structure
- `main.py`: Main agent logic and board analysis
- `.gitignore`: Excludes Python, VS Code, and image files
- `README.md`: Project documentation and usage

## Getting Started
1. Ensure Python 3.12+ is installed.
2. Install dependencies:
   ```bash
   pip install playwright Pillow
   python -m playwright install
   ```
3. Run the agent:
   ```bash
   python main.py
   ```

## How It Works
1. The agent launches a browser and navigates to Block Champ.
2. It locates the game canvas inside nested iframes.
3. Performs automated drag-and-drop moves on the board.
4. Captures screenshots and analyzes the board using Pillow.
5. Prints board state (filled/empty cells) after each move.

## Customization & Next Steps
- Adjust the number of moves or drag logic in `main.py`.
- Improve board analysis for smarter gameplay.
- Implement decision logic in `choose_best_move`.
- Integrate advanced image processing for optimal moves.

## Industry-Standard Practices
- Uses `.gitignore` for Python, VS Code, and generated files
- Modular code structure with clear separation of logic
- Extensible for future features and intelligent agents
