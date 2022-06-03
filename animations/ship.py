import asyncio
from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size

SHIP_FRAME_1 = "animations/ship_frame_1.txt"
SHIP_FRAME_2 = "animations/ship_frame_2.txt"


def load_frames(
    frame_1_filepath: str = SHIP_FRAME_1,
    frame_2_filepath: str = SHIP_FRAME_2,
) -> tuple[str]:
    with open(frame_1_filepath, "r") as file_1:
        frame_1 = file_1.read()

    with open(frame_2_filepath, "r") as file_2:
        frame_2 = file_2.read()

    return frame_1, frame_2


async def fly(
    canvas,
    row: int,
    column: int,
    frame_1: str,
    frame_2: str,
    screen_height: int,
    screen_width: int,
    border_offset: int = 1,
) -> None:
    frame_height, frame_width = get_frame_size(frame_1)
    row, column = row + 1, column - frame_width // 2
    available_movement_height = screen_height - frame_height - border_offset
    available_movement_width = screen_width - frame_width - border_offset

    while True:
        for frame in cycle([frame_1, frame_2]):
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
            draw_frame(canvas, row, column, frame, negative=True)
