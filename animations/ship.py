from itertools import cycle
from typing import Coroutine

import settings
import global_vars
from animations.gameover import show_gameover
from animations.gun import fire
from curses_tools import draw_frame, get_frame_size, read_controls
from physics import update_speed
from utils import load_frames, sleep


async def fly_ship(canvas, row: int, column: int) -> Coroutine:
    screen_height, screen_width = canvas.getmaxyx()
    gameover_frame = load_frames(settings.GAMEOVER_FRAME)[0]
    ship_frames = load_frames(settings.SHIP_FRAMES, double=True)

    frame_height, frame_width = get_frame_size(ship_frames[0])
    row, column = row + 1, column - frame_width // 2
    available_movement_height = screen_height - frame_height - settings.BORDER_OFFSET
    available_movement_width = screen_width - frame_width - settings.BORDER_OFFSET
    row_speed, column_speed = (0, 0)

    for frame in cycle(ship_frames):
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        row_speed, column_speed = update_speed(
            row_speed=row_speed,
            column_speed=column_speed,
            rows_direction=rows_direction,
            columns_direction=columns_direction,
        )

        row = (
            min(row + rows_direction, available_movement_height)
            if rows_direction > 0
            else max(row + rows_direction, 1)
        )
        column = (
            min(column + columns_direction, available_movement_width)
            if columns_direction > 0
            else max(column + columns_direction, 1)
        )

        row += row_speed
        column += column_speed

        if space_pressed and global_vars.YEAR >= 2020:
            global_vars.COROUTINES.append(
                fire(canvas, row=row, column=column + 2)  # gun barrel sprite correction
            )

        for obstacle in global_vars.OBSTACLES:
            if obstacle.has_collision(row, column, frame_height, frame_width):
                await show_gameover(canvas, gameover_frame)

        draw_frame(canvas, row, column, frame)
        await sleep(1)
        draw_frame(canvas, row, column, frame, True)
