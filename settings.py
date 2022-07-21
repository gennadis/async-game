DEBUG = False
GAME_TIME_SPEED = 10  # The bigger the slower
TIC_TIMEOUT = 0.1

# Spaceship
SHIP_FRAMES = [
    "animations/sprites/ship_frame_1.txt",
    "animations/sprites/ship_frame_2.txt",
]

# Stars
BORDER_OFFSET = 1
TOTAL_STARS = 200
STAR_SYMBOLS = "+*.:"

# Garbage
GARBAGE_SPEED = 0.5
GARBAGE_FRAMES = [
    "animations/sprites/duck.txt",
    "animations/sprites/lamp.txt",
    "animations/sprites/hubble.txt",
    "animations/sprites/trash_small.txt",
    "animations/sprites/trash_large.txt",
    "animations/sprites/trash_huge.txt",
]

# Spaceship gun
FIRE_ROW_SPEED = -1
FIRE_COLUMN_SPEED = 0

# Curses key bindings
SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258

# Gameover
GAMEOVER_FRAME = ["animations/sprites/gameover.txt"]

# Explosion
EXPLOSION_FRAMES = [
    "animations/sprites/explosion_1.txt",
    "animations/sprites/explosion_2.txt",
    "animations/sprites/explosion_3.txt",
    "animations/sprites/explosion_4.txt",
]

# Events by years
EVENTS = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: "ISS start building",
    2011: "Messenger launch to Mercury",
    2020: "Take the plasma gun! Shoot the garbage!",
}
