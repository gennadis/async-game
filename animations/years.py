import curses
from typing import Coroutine

import settings
from utils import sleep


async def go(canvas, game_time_speed: int) -> Coroutine:
    year_window = canvas.derwin(3, 6, 0, 0)
    while True:
        year_window.border()
        year_window.addstr(1, 1, str(settings.YEAR), curses.A_BOLD)

        if settings.YEAR in settings.EVENTS:
            canvas.addstr(1, 7, settings.EVENTS[settings.YEAR], curses.A_BOLD)

        year_window.refresh()
        await sleep(game_time_speed)
        settings.YEAR += 1
