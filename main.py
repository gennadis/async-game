import curses
import time

import settings
from animations import garbage, gun, ship, stars


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    SCREEN_HEIGHT, SCREEN_WIDTH = curses.window.getmaxyx(canvas)
    # window.getmaxyx() returns a tuple (y, x) of the height and width of the window.
    # https://docs.python.org/3/library/curses.html#curses.window.getmaxyx

    central_row, central_column = SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2

    generated_stars = stars.generate(
        screen_height=SCREEN_HEIGHT,
        screen_width=SCREEN_WIDTH,
        total_stars=settings.TOTAL_STARS,
        border_offset=settings.BORDER_OFFSET,
        symbols=settings.STAR_SYMBOLS,
    )
    stars_animation = [
        stars.blink(canvas, row, column, symbol)
        for row, column, symbol in generated_stars
    ]

    fire_animation = gun.fire(
        canvas,
        row=central_row,
        column=central_column,
        screen_height=SCREEN_HEIGHT,
        screen_width=SCREEN_WIDTH,
    )

    ship_frames = ship.load_frames(settings.SHIP_FRAMES)
    ship_animation = ship.fly_ship(
        canvas,
        row=central_row,
        column=central_column,
        frames=ship_frames,
        screen_height=SCREEN_HEIGHT,
        screen_width=SCREEN_WIDTH,
    )
    garbage_frames = garbage.load_frames(settings.GARBAGE_FRAMES)
    garbage_animation = garbage.fill_orbit_with_garbage(
        canvas,
        frames=garbage_frames,
        screen_width=SCREEN_WIDTH,
        delay=settings.GARBAGE_DELAY,
    )

    settings.COROUTINES.extend(
        [*stars_animation, fire_animation, ship_animation, garbage_animation]
    )

    while settings.COROUTINES:
        for coroutine in settings.COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                settings.COROUTINES.remove(coroutine)

        canvas.refresh()
        time.sleep(settings.TIC_TIMEOUT)


if __name__ == "__main__":
    settings.initialize()
    curses.update_lines_cols()
    curses.wrapper(draw)
