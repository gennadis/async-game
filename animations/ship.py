import asyncio
from itertools import cycle

from curses_tools import draw_frame

SHIP_FRAME_1 = "animations/ship_frame_1.txt"
SHIP_FRAME_2 = "animations/ship_frame_2.txt"


def load_frames(
    frame_1_filepath: str = SHIP_FRAME_1, frame_2_filepath: str = SHIP_FRAME_2
) -> tuple[str]:
    with open(frame_1_filepath, "r") as file_1:
        frame_1 = file_1.read()
    with open(frame_2_filepath, "r") as file_2:
        frame_2 = file_2.read()

    return frame_1, frame_2


async def fly(
    canvas, row: int, column: int, frame_1: list[str], frame_2: list[str]
) -> None:
    frame = cycle([frame_1, frame_2])

    while True:
        current_frame = next(frame)
        draw_frame(canvas, row, column, current_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, current_frame, negative=True)
