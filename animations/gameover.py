from typing import Coroutine

from curses_tools import draw_frame, get_frame_size
from utils import sleep


async def show_gameover(canvas, gameover_frame: str) -> Coroutine:
    screen_height, screen_width = canvas.getmaxyx()
    frame_height, frame_width = get_frame_size(gameover_frame)

    frame_start_row = screen_height // 2 - frame_height // 2
    frame_start_column = screen_width // 2 - frame_width // 2

    while True:
        draw_frame(canvas, frame_start_row, frame_start_column, gameover_frame)
        await sleep(1)
