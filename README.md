# Browser Operating Agent

A Python agent that drives its own browser — no DOM shortcuts, no hidden state. Just Playwright + PIL, navigating nested iframes, dragging the mouse like a human, and reading the game board from pixel data.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Chromium-45ba4b?logo=playwright&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## What it does

The agent opens `crazygames.com/game/block-champ`, finds the game canvas through two levels of iframes, and plays by screenshotting the board and performing humanlike drag-and-drop moves.

It is intentionally restricted to what a person with only a mouse and a screen could do. That constraint is the point — the techniques generalize to any canvas-based web app where the DOM can't help you: design tools, in-browser IDEs, CAD apps, games, legacy internal tools.

## Why it's interesting

Most "browser agents" assume the app cooperates — queryable buttons, labeled inputs, readable HTML. Real-world apps often don't. Four things make this project technically non-trivial:

1. **Nested iframes.** The game lives inside a CrazyGames wrapper iframe, which contains the actual game iframe. Each has its own DOM and coordinate system.
2. **Canvas rendering.** The board is drawn into an HTML5 `<canvas>` element — opaque to the DOM. State has to be read from pixels.
3. **Global coordinate math.** `bounding_box()` gives frame-local positions. The mouse API expects page-global coordinates. Every nested iframe stacks another offset.
4. **Humanlike mouse dynamics.** Teleported drags don't register in Block Champ. The agent interpolates ~40 intermediate mouse positions across a drag to produce natural motion.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Playwright (Chromium)                                      │
│  └── crazygames page                                        │
│      └── iframe#game-iframe                                 │
│          └── iframe[src*="block-champ/2/index.html"]        │
│              └── canvas#gameCanvas                          │
└─────────────────────────────────────────────────────────────┘
            │
            ├── screenshot(canvas) ──► PIL ──► grid sample ──► board state
            └── mouse.move + down + interpolated moves + up ──► drag action
```

## Quick start

```bash
git clone https://github.com/Hassan-Naeem-code/Browser-Operating-Agent.git
cd Browser-Operating-Agent

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

python -m browser_agent.main
```

The browser opens visibly, makes 5 moves, saves screenshots after each, and prints the inferred board state:

```
Navigated to Block Champ on CrazyGames
Block Champ iframe detected.
Switched context to game iframe.
Switched context to nested Block Champ game iframe.
Canvas bounding box: {'x': 34, 'y': 88, 'width': 412, 'height': 628}
Move 1: Dragged from (...) to (...)
Board state after move 1: {'size': (412, 628), 'empty_cells': 67, 'filled_cells': 33, 'percent_filled': 33.0}
...
```

## Key techniques (copy-friendly)

**Traverse nested iframes**

```python
await page.wait_for_selector('iframe#game-iframe', timeout=15000)
outer = await (await page.query_selector('iframe#game-iframe')).content_frame()
inner = await (await outer.query_selector('iframe[src*="block-champ"]')).content_frame()
```

**Compute page-global coordinates**

```python
canvas_box = await canvas.bounding_box()
iframe_box = await nested_iframe_element.bounding_box()
global_x = iframe_box['x'] + canvas_box['x'] + canvas_box['width'] / 2
global_y = iframe_box['y'] + canvas_box['y'] + canvas_box['height'] * 0.85
```

**Humanlike drag (~400 ms)**

```python
steps = 40
for i in range(steps):
    x = src_x + (tgt_x - src_x) * (i / steps)
    y = src_y + (tgt_y - src_y) * (i / steps)
    await page.mouse.move(x, y)
    await asyncio.sleep(0.01)
```

**Read a canvas via pixel sampling**

```python
img_bytes = await canvas.screenshot()
img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
# 10x10 grid, sample center of each cell, classify by brightness
```

## Project structure

```
.
├── browser_agent/
│   ├── __init__.py
│   └── main.py           # BrowserOperatingAgent class
├── tests/
│   └── test_agent.py
├── requirements.txt
└── README.md
```

## Roadmap

- [ ] Replace random moves with a smarter move-selection policy
- [ ] Send the board state to an LLM and let it pick moves
- [ ] Classify filled-cell shapes with a small vision model instead of brightness
- [ ] Headless scheduled runs with score tracking

## License

MIT
