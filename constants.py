from itertools import cycle
BOARD_SIZE = 8

LETTERS = 'ABCDEFGH'
WHITES_INITIAL_POSITION = 'a1, a3, b2, c1, c3, d2, e1, e3, f2, g1, g3, h2'
BLACKS_INITIAL_POSITION = 'a7, b6, b8, c7, d6, d8, e7, f6, f8, g7, h6, h8'

COLOR_WHITE = 255, 255, 255
COLOR_BLACK = 255, 0, 0
COLOR_GREY = 128, 128, 128

PIECE_PADDING = 15
PIECE_OUTLINE = 2

BOARD_WIDTH = 640
TEXTBOX_WIDTH = 260

SQUARE_SIZE = BOARD_WIDTH // BOARD_SIZE
CROWN_SIZE = 19

CROWN_IMG = "assets/crown.gif"
CHECKERS_IMG = "assets/checkers.png"
BOUNCE = cycle([0, 1, 2, 4, 5, 4, 3, 2, 1])
FPS = 30

INITIAL_TEXT = "<p>Welcome!</p>"
