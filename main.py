import curses
import time

from animations import gun, ship, stars, garbage

TIC_TIMEOUT = 0.1
coroutines = []


def draw(canvas):
    canvas.border()
    canvas.nodelay(True)
    curses.curs_set(False)

    screen_height, screen_width = curses.window.getmaxyx(canvas)
    # window.getmaxyx() returns a tuple (y, x) of the height and width of the window.
    # https://docs.python.org/3/library/curses.html#curses.window.getmaxyx

    central_row, central_column = screen_height // 2, screen_width // 2

    generated_stars = stars.generate(
        screen_height=screen_height,
        screen_width=screen_width,
    )
    stars_animation = [
        stars.blink(canvas, row, column, symbol)
        for row, column, symbol in generated_stars
    ]

    fire_animation = gun.fire(
        canvas,
        row=central_row,
        column=central_column,
        screen_height=screen_height,
        screen_width=screen_width,
    )

    ship_frames = ship.load_frames()
    ship_animation = ship.fly_ship(
        canvas,
        row=central_row,
        column=central_column,
        frames=ship_frames,
        screen_height=screen_height,
        screen_width=screen_width,
    )
    garbage_frames = garbage.load_frames()
    garbage_animation = garbage.fill_orbit_with_garbage(
        canvas,
        frames=garbage_frames,
        screen_width=screen_width,
    )

    coroutines.extend(
        [*stars_animation, fire_animation, ship_animation, garbage_animation]
    )

    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
