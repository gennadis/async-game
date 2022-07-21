import curses
from typing import Coroutine

import global_vars
import settings
from utils import sleep


async def fire(canvas, row: int, column: int) -> Coroutine:
    screen_height, screen_width = canvas.getmaxyx()
    rows_speed = settings.FIRE_ROW_SPEED
    columns_speed = settings.FIRE_COLUMN_SPEED

    canvas.addstr(round(row), round(column), "*")
    await sleep(1)

    canvas.addstr(round(row), round(column), "O")
    await sleep(1)

    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    max_row, max_column = screen_height - 1, screen_width - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await sleep(1)
        canvas.addstr(round(row), round(column), " ")

        for obstacle in global_vars.obstacles:
            if obstacle.has_collision(row, column):
                global_vars.obstacles_in_last_collision.append(obstacle)
                return

        row += rows_speed
        column += columns_speed
