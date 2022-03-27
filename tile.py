from constants import BOARD_SIZE, LETTERS


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

    @classmethod
    def is_valid(cls, new_x, new_y):
        return 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE

    def top_left(self):
        new_x = self.x-1
        new_y = self.y-1
        return Tile(new_x, new_y) if Tile.is_valid(new_x, new_y) else None

    def top_right(self):
        new_x = self.x+1
        new_y = self.y-1
        return Tile(new_x, new_y) if Tile.is_valid(new_x, new_y) else None

    def bottom_left(self):
        new_x = self.x-1
        new_y = self.y+1
        return Tile(new_x, new_y) if Tile.is_valid(new_x, new_y) else None

    def bottom_right(self):
        new_x = self.x+1
        new_y = self.y+1
        return Tile(new_x, new_y) if Tile.is_valid(new_x, new_y) else None
