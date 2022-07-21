import random
from typing import Coroutine, Optional

import settings
import global_vars
from animations.explosion import explode
from animations.obstacles import Obstacle, show_obstacles
from curses_tools import draw_frame, get_frame_size
from utils import load_frames, sleep


async def fly_garbage(
    canvas, column: int, garbage_frame: str, speed: float
) -> Coroutine:
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    screen_height, screen_width = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, screen_width - 1)
    row = 0

    frame_size_row, frame_size_column = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, frame_size_row, frame_size_column)

    global_vars.OBSTACLES.append(obstacle)

    if settings.DEBUG:
        global_vars.COROUTINES.append(show_obstacles(canvas, global_vars.OBSTACLES))

    while row < screen_height:
        draw_frame(canvas, row, column, garbage_frame)
        obstacle.row = row
        await sleep(1)
        draw_frame(canvas, row, column, garbage_frame, negative=True)

        if obstacle in global_vars.OBSTACLES_IN_LAST_COLLISIONS:
            global_vars.OBSTACLES_IN_LAST_COLLISIONS.remove(obstacle)
            global_vars.OBSTACLES.remove(obstacle)
            await explode(
                canvas,
                center_row=row + (frame_size_row / 2),
                center_column=column + (frame_size_column / 2),
            )
            return

        row += speed

    global_vars.OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(canvas, garbage_speed: int) -> Coroutine:
    _, screen_width = canvas.getmaxyx()
    garbage_frames = load_frames(settings.GARBAGE_FRAMES)

    while True:
        column = random.randint(1, screen_width)
        frame = random.choice(garbage_frames)
        delay = get_garbage_delay_tics(global_vars.YEAR)

        if delay:
            global_vars.COROUTINES.append(
                fly_garbage(
                    canvas,
                    column=column,
                    garbage_frame=frame,
                    speed=garbage_speed,
                )
            )
            await sleep(tic=delay)
        else:
            await sleep(1)


def get_garbage_delay_tics(year) -> Optional[int]:
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2
