import curses
import time

import settings
import global_vars
from animations import garbage, ship, stars, years


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
        stars.blink(canvas, row, column, symbol)
        for row, column, symbol in generated_stars
    ]
    ship_animation = ship.fly_ship(
        canvas,
        row=central_row,
        column=central_column,
    )
    garbage_animation = garbage.fill_orbit_with_garbage(
        canvas,
        garbage_speed=settings.GARBAGE_SPEED,
    )
    years_animation = years.go(
        canvas,
        game_time_speed=settings.GAME_TIME_SPEED,
    )

    global_vars.COROUTINES.extend(
        [
            *stars_animation,
            ship_animation,
            garbage_animation,
            years_animation,
        ]
    )

    while global_vars.COROUTINES:
        for coroutine in global_vars.COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                global_vars.COROUTINES.remove(coroutine)

        canvas.refresh()
        canvas.border()  # fix objects braking borders bug
        time.sleep(settings.TIC_TIMEOUT)


if __name__ == "__main__":
    global_vars.initialize()
    curses.update_lines_cols()
    curses.wrapper(draw)
