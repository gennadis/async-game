import asyncio
from itertools import cycle

import settings
from curses_tools import draw_frame, get_frame_size, read_controls


async def fly_ship(
    canvas,
    row: int,
    column: int,
    frames: list[str],
    screen_height: int,
    screen_width: int,
) -> None:
    frame_height, frame_width = get_frame_size(frames[0])
    row, column = row + 1, column - frame_width // 2
    available_movement_height = screen_height - frame_height - settings.BORDER_OFFSET
    available_movement_width = screen_width - frame_width - settings.BORDER_OFFSET

    for frame in cycle(frames):
        rows_direction, columns_direction, _ = read_controls(canvas)

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

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, True)
