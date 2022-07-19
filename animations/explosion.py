import asyncio
import curses
from typing import Coroutine

import settings
from curses_tools import draw_frame, get_frame_size
from utils import load_frames


async def explode(canvas, center_row: int, center_column: int) -> Coroutine:
    explosion_frames = load_frames(settings.EXPLOSION_FRAMES)
    rows, columns = get_frame_size(explosion_frames[0])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()

    for frame in explosion_frames:
        draw_frame(canvas, corner_row, corner_column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await asyncio.sleep(0)
