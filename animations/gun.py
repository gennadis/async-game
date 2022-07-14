import asyncio
import curses

FIRE_ROW_SPEED = -1
FIRE_COLUMN_SPEED = 0


async def fire(
    canvas,
    row: int,
    column: int,
    screen_height: int,
    screen_width: int,
    rows_speed: float = FIRE_ROW_SPEED,
    columns_speed: float = FIRE_COLUMN_SPEED,
) -> None:
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
