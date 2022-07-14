import asyncio
from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls

SHIP_FRAME_1 = "animations/ship_frame_1.txt"
SHIP_FRAME_2 = "animations/ship_frame_2.txt"


def load_frames(frames_filepath: list = [SHIP_FRAME_1, SHIP_FRAME_2]) -> list[str]:
    frames = []
    for frame_filepath in frames_filepath:
        with open(frame_filepath, "r") as file:
            frame = file.read()
            frames.extend([frame, frame])

    return frames


async def fly_ship(
    canvas,
    row: int,
    column: int,
    frames: list[str],
    screen_height: int,
    screen_width: int,
    border_offset: int = 1,
) -> None:
    frame_height, frame_width = get_frame_size(frames[0])
    row, column = row + 1, column - frame_width // 2
    available_movement_height = screen_height - frame_height - border_offset
    available_movement_width = screen_width - frame_width - border_offset

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
