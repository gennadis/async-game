import asyncio
import curses
import random


def generate(
    total_stars: int,
    screen_height: int,
    screen_width: int,
    border_offset: int,
    symbols: str,
) -> list[tuple]:
    stars = []
    for _ in range(total_stars):
        x_coordinate = random.randint(border_offset, screen_height - border_offset)
        y_coordinate = random.randint(border_offset, screen_width - border_offset)
        symbol = random.choice(symbols)
        stars.append((x_coordinate, y_coordinate, symbol))

    return stars


async def blink(
    canvas,
    row: int,
    column: int,
    symbol: str,
):
    while True:
        for _ in range(random.randint(1, 20)):
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await asyncio.sleep(0)

        for _ in range(3):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)

        for _ in range(5):
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await asyncio.sleep(0)

        for _ in range(3):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)
