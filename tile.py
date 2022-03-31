from constants import BOARD_SIZE, LETTERS

VECTOR_TOP_LEFT = (-1, -1)
VECTOR_TOP_RIGHT = (+1, -1)
VECTOR_BOTTOM_LEFT = (-1, +1)
VECTOR_BOTTOM_RIGHT = (+1, +1)
X2 = lambda x: tuple(i*2 for i in x)
MINUS = lambda x: tuple(-i for i in x)

VECTORS_WHITE = [VECTOR_TOP_LEFT, VECTOR_TOP_RIGHT]
VECTORS_BLACK = [VECTOR_BOTTOM_RIGHT, VECTOR_BOTTOM_LEFT]

VECTORS = VECTORS_BLACK + VECTORS_WHITE


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = LETTERS[x] + str(BOARD_SIZE - y)
        self.black = (y % 2 != x % 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return self.name

    def __add__(self, vctr: tuple[int, int]):
        return Tile(self.x + vctr[0], self.y + vctr[1]) if Tile.is_valid(self.x + vctr[0], self.y + vctr[1]) else None

    @classmethod
    def is_valid(cls, new_x, new_y):
        return 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE

    @classmethod
    def from_string(cls, string: str):
        if not string.isdigit():
            return Tile(LETTERS.index(string[0]), BOARD_SIZE - int(string[1:]))
        else:
            x = (int(string) - 1) * 2 % BOARD_SIZE
            y = (int(string) - 1) * 2 // BOARD_SIZE
            if y % 2 == x % 2:
                x += 1
            return Tile(x, y)

    @property
    def number(self):
        return str((BOARD_SIZE * self.y + self.x) // 2 + 1)

    def top_left(self):
        tile = self
        while tile := tile + VECTOR_TOP_LEFT:
            yield tile

    def top_right(self):
        tile = self
        while tile := tile + VECTOR_TOP_RIGHT:
            yield tile

    def bottom_left(self):
        tile = self
        while tile := tile + VECTOR_BOTTOM_LEFT:
            yield tile

    def bottom_right(self):
        tile = self
        while tile := tile + VECTOR_BOTTOM_RIGHT:
            yield tile
