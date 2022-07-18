import asyncio
import random

import settings
from animations.explosion import explode
from animations.obstacles import Obstacle, show_obstacles
from curses_tools import draw_frame, get_frame_size
from utils import load_frames


async def fly_garbage(canvas, column, garbage_frame: str, speed: float):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    screen_height, screen_width = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, screen_width - 1)

    row = 0

    frame_size_row, frame_size_column = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, frame_size_row, frame_size_column)

    settings.OBSTACLES.append(obstacle)

    if settings.DEBUG:
        settings.COROUTINES.append(show_obstacles(canvas, settings.OBSTACLES))

    while row < screen_height:
        draw_frame(canvas, row, column, garbage_frame)
        obstacle.row = row
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)

        if obstacle in settings.OBSTACLES_IN_LAST_COLLISIONS:
            settings.OBSTACLES_IN_LAST_COLLISIONS.remove(obstacle)
            settings.OBSTACLES.remove(obstacle)
            await explode(
                canvas,
                center_row=row + (frame_size_row / 2),
                center_column=column + (frame_size_column / 2),
            )
            return

        row += speed

    settings.OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(canvas, delay: int):
    _, screen_width = canvas.getmaxyx()
    garbage_frames = load_frames(settings.GARBAGE_FRAMES)
    while True:
        column = random.randint(1, screen_width)
        frame = random.choice(garbage_frames)
        settings.COROUTINES.append(
            fly_garbage(
                canvas, column=column, garbage_frame=frame, speed=settings.GARBAGE_SPEED
            )
        )
        for _ in range(delay):
            await asyncio.sleep(0)
