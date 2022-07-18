import asyncio
import random

import settings
from curses_tools import draw_frame, get_frame_size
from animations.obstacles import Obstacle, show_obstacles


async def fly_garbage(canvas, column, garbage_frame: str, speed: float):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_size_row, frame_size_column = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, frame_size_row, frame_size_column)

    settings.OBSTACLES.append(obstacle)

    if settings.DEBUG:
        settings.COROUTINES.append(show_obstacles(canvas, settings.OBSTACLES))

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        obstacle.row = row
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

    settings.OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(
    canvas, frames: list[str], screen_width: int, delay: int
):

    while True:
        column = random.randint(1, screen_width)
        frame = random.choice(frames)
        settings.COROUTINES.append(
            fly_garbage(
                canvas, column=column, garbage_frame=frame, speed=settings.GARBAGE_SPEED
            )
        )
        for _ in range(delay):
            await asyncio.sleep(0)
