import asyncio
import curses

import settings


async def fire(
    canvas, row: int, column: int, screen_height: int, screen_width: int
) -> None:
    rows_speed = settings.FIRE_ROW_SPEED
    columns_speed = settings.FIRE_COLUMN_SPEED

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

        for obstacle in settings.OBSTACLES:
            if obstacle.has_collision(row, column):
                settings.OBSTACLES_IN_LAST_COLLISIONS.append(obstacle)
                return

        row += rows_speed
        column += columns_speed
