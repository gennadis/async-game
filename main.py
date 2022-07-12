import curses
import time

from animations import gun, ship, stars

TIC_TIMEOUT = 0.1


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

    ship_frame_1, ship_frame_2 = ship.load_frames()
    ship_animation = ship.fly_ship(
        canvas,
        row=central_row,
        column=central_column,
        frame_1=ship_frame_1,
        frame_2=ship_frame_2,
        screen_height=screen_height,
        screen_width=screen_width,
    )

    coroutines = [*stars_animation, fire_animation, ship_animation]

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
