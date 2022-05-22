import asyncio
import curses
import random
import time

TIC_TIMEOUT = 0.1
BORDER_OFFSET = 3
TOTAL_STARS = 200
STAR_SYMBOLS = "+*.:"


def create_stars(
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


async def blink(canvas, row, column, symbol="*"):
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


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    screen_height, screen_width = curses.window.getmaxyx(canvas)

    stars = create_stars(
        total_stars=TOTAL_STARS,
        screen_height=screen_height,
        screen_width=screen_width,
        border_offset=BORDER_OFFSET,
        symbols=STAR_SYMBOLS,
    )
    coroutines = [blink(canvas, row, column, symbol) for row, column, symbol in stars]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)

        if len(coroutines) == 0:
            break


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
