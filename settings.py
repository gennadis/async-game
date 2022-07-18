def initialize():
    """Initialize global variables."""
    global COROUTINES
    global OBSTACLES
    COROUTINES = []
    OBSTACLES = []


DEBUG = False

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
GARBAGE_DELAY = 10
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
