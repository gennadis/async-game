import curses
import time
from animations import gun, stars


TIC_TIMEOUT = 0.1
BORDER_OFFSET = 3
TOTAL_STARS = 200
STAR_SYMBOLS = "+*.:"


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    screen_height, screen_width = curses.window.getmaxyx(canvas)

    generated_stars = stars.generate(
        total_stars=TOTAL_STARS,
        screen_height=screen_height,
        screen_width=screen_width,
        border_offset=BORDER_OFFSET,
        symbols=STAR_SYMBOLS,
    )

    stars_animation = [
        stars.blink(canvas, row, column, symbol)
        for row, column, symbol in generated_stars
    ]
    fire_animation = gun.fire(
        canvas,
        start_row=screen_height / 2,
        start_column=screen_width / 2,
        screen_height=screen_height,
        screen_width=screen_width,
        rows_speed=-0.3,
        columns_speed=0,
    )

    coroutines = [*stars_animation, fire_animation]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)

        if len(coroutines) == 0:
            break

        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
