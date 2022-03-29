from constants import BOARD_SIZE
from tile import Tile


class Board:
    def __init__(self):
        self.tiles = {}
        self.positions = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                new_tile = Tile(i, BOARD_SIZE - (j + 1))
                self.tiles[new_tile.name] = new_tile

    def __getitem__(self, tile_name: str) -> Tile:
        return self.tiles[tile_name]

    def get(self, x, y) -> Tile:
        return list(self.tiles.values())[x * BOARD_SIZE + y]

    def set_initial_position(self, position):
        self.positions = [position]

    @property
    def current_position(self):
        return self.positions[-1] if self.positions else None
