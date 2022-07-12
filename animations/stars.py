import curses
import random

from animations.utils import sleep

BORDER_OFFSET = 1
TOTAL_STARS = 200
STAR_SYMBOLS = "+*.:"


def generate(
    screen_height: int,
    screen_width: int,
    total_stars: int = TOTAL_STARS,
    border_offset: int = BORDER_OFFSET,
    symbols: str = STAR_SYMBOLS,
) -> list[tuple]:
    stars = []
    for _ in range(total_stars):
        row = random.randint(border_offset, screen_height - 2 * border_offset)
        column = random.randint(border_offset, screen_width - border_offset)
        symbol = random.choice(symbols)
        stars.append((row, column, symbol))

    return stars


async def blink(canvas, row: int, column: int, symbol: str):
    while True:
        for _ in range(random.randint(1, 20)):
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await sleep()

        for _ in range(3):
            canvas.addstr(row, column, symbol)
            await sleep()

        for _ in range(5):
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await sleep()

        for _ in range(3):
            canvas.addstr(row, column, symbol)
            await sleep()
