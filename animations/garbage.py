import asyncio
import random
from main import COROUTINES

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


async def fly_garbage(canvas, column, garbage_frame: str, speed: float = 0.5):
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


async def fill_orbit_with_garbage(
    canvas,
    frames: list[str],
    screen_width: int,
    timeout: int = 10,
):
    while True:
        for _ in range(random.randint(1, timeout)):
            await asyncio.sleep(0)

        column = random.randint(1, screen_width)
        frame = random.choice(frames)
        coroutine = fly_garbage(canvas, column, frame)
        COROUTINES.append(coroutine)
