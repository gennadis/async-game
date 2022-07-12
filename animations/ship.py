import asyncio
from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size

SHIP_FRAME_1 = "animations/ship_frame_1.txt"
SHIP_FRAME_2 = "animations/ship_frame_2.txt"


def load_frames(frames_filepath: list = [SHIP_FRAME_1, SHIP_FRAME_2]) -> list[str]:
    frames = []
    for frame_filepath in frames_filepath:
        with open(frame_filepath, "r") as file:
            frame = file.read()
            frames.append(frame)

    return frames


def calculate_coordinate(
    current_coordinate: int,
    max_coordinate: int,
    direction: int,
    frame_size: int,
):
    # top and left screen sides handling
    if current_coordinate <= 1 and direction == -1:
        next_coordinate = 1

    # bottom and right screen sides handling
    elif max_coordinate - (current_coordinate + frame_size) <= direction:
        next_coordinate = max_coordinate - frame_size - 1

    else:
        next_coordinate = current_coordinate + direction

    return next_coordinate


async def fly(
    canvas,
    row: int,
    column: int,
    frame_1: str,
    frame_2: str,
    screen_height: int,
    screen_width: int,
) -> None:
    frame_height, frame_width = get_frame_size(frame_1)

    for frame in cycle([frame_1, frame_2]):
        rows_direction, columns_direction, _ = read_controls(canvas)

        if rows_direction:
            row = calculate_coordinate(row, screen_height, rows_direction, frame_height)
        if columns_direction:
            column = calculate_coordinate(
                column, screen_width, columns_direction, frame_width
            )

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, True)
