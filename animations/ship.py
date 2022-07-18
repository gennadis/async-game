import asyncio
from itertools import cycle

import settings
from curses_tools import draw_frame, get_frame_size, read_controls
from physics import update_speed
from animations.gun import fire
from animations.gameover import show_gameover


async def fly_ship(
    canvas,
    row: int,
    column: int,
    frames: list[str],
    screen_height: int,
    screen_width: int,
    gameover_frame: str,
) -> None:
    frame_height, frame_width = get_frame_size(frames[0])
    row, column = row + 1, column - frame_width // 2
    available_movement_height = screen_height - frame_height - settings.BORDER_OFFSET
    available_movement_width = screen_width - frame_width - settings.BORDER_OFFSET
    row_speed, column_speed = (0, 0)

    for frame in cycle(frames):
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

        if space_pressed:
            settings.COROUTINES.append(
                fire(
                    canvas,
                    row=row,
                    column=column + 2,  # gun barrel sprite correction
                    screen_height=screen_height,
                    screen_width=screen_width,
                )
            )
        for obstacle in settings.OBSTACLES:
            if obstacle.has_collision(row, column, frame_height, frame_width):
                await show_gameover(canvas, row, column, frame=gameover_frame)

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, True)
