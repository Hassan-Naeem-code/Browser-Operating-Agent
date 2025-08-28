# Browser Operating Agent

## Overview
 
# Browser Operating Agent

This project is a browser automation agent that operates its own browser, designed to automate and analyze the Block Champ game on CrazyGames.

## Features
- Launches a Chromium browser and navigates to Block Champ
- Detects nested iframes and game canvas
- Automates drag-and-drop moves with smooth motion
- Captures screenshots and analyzes the board using Pillow
- Extensible for smarter move logic

## Setup
1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the agent:
   ```bash
   python -m browser_agent.main
   ```

## Project Structure
```
BrowserOperatingAgent/
├── browser_agent/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_agent.py
```


## Notes
- The agent currently performs random drag-and-drop moves. Board analysis is basic and can be improved for smarter gameplay.
- Screenshots and canvas images are saved after each move for debugging and analysis in the `game_screenshot/` folder.
- The browser closes automatically after the script finishes. To keep it open, comment out the browser close line or add a sleep at the end of the script.
