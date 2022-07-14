import asyncio

from curses_tools import draw_frame

DUCK_FRAME = "animations/sprites/duck.txt"
LAMP_FRAME = "animations/sprites/lamp.txt"
HUBBLE_FRAME = "animations/sprites/hubble.txt"
TRASH_SMALL_FRAME = "animations/sprites/trash_small.txt"
TRASH_LARGE_FRAME = "animations/sprites/trash_large.txt"
TRASH_HUGE_FRAME = "animations/sprites/trash_huge.txt"


def load_frames(
    frames_filepath: list = [
        DUCK_FRAME,
        LAMP_FRAME,
        HUBBLE_FRAME,
        TRASH_HUGE_FRAME,
        TRASH_LARGE_FRAME,
        TRASH_SMALL_FRAME,
    ]
) -> list[str]:
    frames = []
    for frame_filepath in frames_filepath:
        with open(frame_filepath, "r") as file:
            frame = file.read()
            frames.append(frame)

    return frames


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
