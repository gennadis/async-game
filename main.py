import curses
import random
import time

import global_vars
import settings
from animations import garbage, ship, stars, years
from utils import load_frames


def draw(canvas):
    canvas.nodelay(True)
    curses.curs_set(False)

    # window.getmaxyx() returns a tuple (y, x) of the height and width of the window.
    # https://docs.python.org/3/library/curses.html#curses.window.getmaxyx
    screen_height, screen_width = canvas.getmaxyx()
    central_row, central_column = screen_height // 2, screen_width // 2

    generated_stars = stars.generate(
        canvas,
        total_stars=settings.TOTAL_STARS,
        border_offset=settings.BORDER_OFFSET,
        symbols=settings.STAR_SYMBOLS,
    )
    stars_animation = [
        stars.blink(
            canvas,
            row=row,
            column=column,
            symbol=symbol,
            offset_tics=random.randint(1, settings.BLINK_OFFSET_MAX),
        )
        for row, column, symbol in generated_stars
    ]
    ship_animation = ship.fly_ship(
        canvas,
        row=central_row,
        column=central_column,
    )
    garbage_frames = load_frames(settings.GARBAGE_FRAMES)
    garbage_animation = garbage.fill_orbit_with_garbage(
        canvas,
        garbage_frames=garbage_frames,
        garbage_speed=settings.GARBAGE_SPEED,
    )
    years_animation = years.go(
        canvas,
        game_time_speed=settings.GAME_TIME_SPEED,
    )

    global_vars.coroutines.extend(
        [
            *stars_animation,
            ship_animation,
            garbage_animation,
            years_animation,
        ]
    )

    while global_vars.coroutines:
        for coroutine in global_vars.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                global_vars.coroutines.remove(coroutine)

        canvas.refresh()
        canvas.border()  # fix objects braking borders bug
        time.sleep(settings.TIC_TIMEOUT)


if __name__ == "__main__":
    global_vars.initialize()
    curses.update_lines_cols()
    curses.wrapper(draw)
