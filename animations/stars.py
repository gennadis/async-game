import curses
import random

from utils import sleep


def generate(canvas, total_stars: int, border_offset: int, symbols: str) -> list[tuple]:
    screen_height, screen_width = canvas.getmaxyx()
    stars = []
    for _ in range(total_stars):
        row = random.randint(border_offset, screen_height - 2 * border_offset)
        column = random.randint(border_offset, screen_width - 2 * border_offset)
        symbol = random.choice(symbols)
        stars.append((row, column, symbol))

    return stars


async def blink(canvas, row: int, column: int, symbol: str):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(random.randint(1, 20))

        canvas.addstr(row, column, symbol)
        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)
