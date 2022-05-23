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


async def blink(
    canvas,
    row: int,
    column: int,
    symbol: str = "*",
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


async def fire(
    canvas,
    start_row: int,
    start_column: int,
    screen_height: int,
    screen_width: int,
    rows_speed: float = -0.3,
    columns_speed: int = 0,
) -> None:
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    max_row, max_column = screen_height - 1, screen_width - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    screen_height, screen_width = curses.window.getmaxyx(canvas)

    stars_animation = create_stars(
        total_stars=TOTAL_STARS,
        screen_height=screen_height,
        screen_width=screen_width,
        border_offset=BORDER_OFFSET,
        symbols=STAR_SYMBOLS,
    )
    fire_animation = fire(
        canvas,
        start_row=screen_height / 2,
        start_column=screen_width / 2,
        screen_height=screen_height,
        screen_width=screen_width,
        rows_speed=-0.3,
        columns_speed=0,
    )

    coroutines = [
        blink(canvas, row, column, symbol) for row, column, symbol in stars_animation
    ]
    coroutines.append(fire_animation)

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
