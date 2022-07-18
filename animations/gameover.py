import asyncio

import settings
from curses_tools import draw_frame, get_frame_size
from utils import load_frames


async def show_gameover(canvas, rows, columns, frame):
    frame_size_row, frame_size_column = get_frame_size(frame)
    row, column = (rows / 2) - (frame_size_row / 2), (columns / 2) - (
        frame_size_column / 2
    )
    while True:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame)
