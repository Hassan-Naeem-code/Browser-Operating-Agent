import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import io
import random

class BrowserOperatingAgent:
    def __init__(self):
        pass

    async def start(self):
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.goto('https://www.crazygames.com/game/block-champ')
            print('Navigated to Block Champ on CrazyGames')
            await self.page.wait_for_timeout(5000)
            title = await self.page.title()
            print(f'Page title: {title}')
            await self.page.screenshot(path="block_champ_screenshot.png")
            print('Screenshot saved as block_champ_screenshot.png')

            await self.page.wait_for_selector('iframe#game-iframe', timeout=15000)
            print('Block Champ iframe detected.')
            iframe_element = await self.page.query_selector('iframe#game-iframe')
            iframe = await iframe_element.content_frame()
            print('Switched context to game iframe.')
            await iframe.wait_for_timeout(5000)
            print('Waited 5 seconds for game content to load inside iframe.')
            nested_iframe_element = await iframe.query_selector('iframe[src*="block-champ/2/index.html"]')

            if nested_iframe_element:
                nested_game_frame = await nested_iframe_element.content_frame()
                print('Switched context to nested Block Champ game iframe.')
                await nested_game_frame.wait_for_timeout(5000)
                canvas = await nested_game_frame.query_selector('#gameCanvas')
                if canvas:
                    canvas_box = await canvas.bounding_box()
                    print(f'Canvas bounding box: {canvas_box}')
                    iframe_box = await nested_iframe_element.bounding_box()
                    print(f'Nested iframe bounding box: {iframe_box}')
                    for move_num in range(5):
                        source_x = iframe_box['x'] + canvas_box['x'] + canvas_box['width'] / 2
                        source_y = iframe_box['y'] + canvas_box['y'] + canvas_box['height'] * 0.85
                        target_x = iframe_box['x'] + canvas_box['x'] + random.uniform(canvas_box['width'] * 0.2, canvas_box['width'] * 0.8)
                        target_y = iframe_box['y'] + canvas_box['y'] + random.uniform(canvas_box['height'] * 0.2, canvas_box['height'] * 0.8)

                        # Move mouse to start position
                        await self.page.mouse.move(source_x, source_y)
                        await asyncio.sleep(0.05)
                        await self.page.mouse.down()
                        # Smooth drag to target
                        steps = 40
                        for i in range(steps):
                            intermediate_x = source_x + (target_x - source_x) * (i / steps)
                            intermediate_y = source_y + (target_y - source_y) * (i / steps)
                            await self.page.mouse.move(intermediate_x, intermediate_y)
                            await asyncio.sleep(0.01)
                        await self.page.mouse.move(target_x, target_y)
                        await asyncio.sleep(0.05)
                        await self.page.mouse.up()
                        print(f'Move {move_num+1}: Dragged from ({source_x}, {source_y}) to ({target_x}, {target_y})')
                        await self.page.screenshot(path=f"block_champ_drag_{move_num+1}.png")
                        print(f'Screenshot after move {move_num+1} saved as block_champ_drag_{move_num+1}.png')
                        img_bytes = await canvas.screenshot()
                        img = Image.open(io.BytesIO(img_bytes))
                        img.save(f"block_champ_canvas_{move_num+1}.png")
                        print(f'Canvas image for move {move_num+1} saved as block_champ_canvas_{move_num+1}.png')
                        board_state = self.analyze_board(img)
                        print(f'Board state after move {move_num+1}: {board_state}')
                        await asyncio.sleep(1)
                else:
                    print('Game canvas (#gameCanvas) not found in nested iframe.')
            else:
                print('Nested Block Champ game iframe not found.')
            # await self.browser.close()  # Commented out to keep browser open after automation

    def analyze_board(self, img):
        img = img.convert('RGB')
        width, height = img.size
        pixels = img.load()
        empty_count = 0
        filled_count = 0
        grid_size = 10
        cell_w = width // grid_size
        cell_h = height // grid_size
        threshold = 220  # consider cells with all RGB > 220 as empty
        for gx in range(grid_size):
            for gy in range(grid_size):
                px = gx * cell_w + cell_w // 2
                py = gy * cell_h + cell_h // 2
                r, g, b = pixels[px, py]
                if r > threshold and g > threshold and b > threshold:
                    empty_count += 1
                else:
                    filled_count += 1
        return {
            'size': img.size,
            'empty_cells': empty_count,
            'filled_cells': filled_count,
            'percent_filled': round(100 * filled_count / (grid_size * grid_size), 2)
        }

    def choose_best_move(self, board_state):
        # Placeholder for future logic
        return None, None

if __name__ == '__main__':
    asyncio.run(BrowserOperatingAgent().start())