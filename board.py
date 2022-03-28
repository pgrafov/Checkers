from constants import BOARD_SIZE, WHITES_INITIAL_POSITION, BLACKS_INITIAL_POSITION
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


class Piece:
    def __init__(self, position: Tile, black: bool, king: bool = False):
        self.position = position
        self.king = king
        self.black = black

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def __repr__(self):
        return f'{"black" if self.black else "white"} {"king" if self.king else "piece"} on {self.position}'


class Move:
    def __init__(self, before, after, captures=tuple(), gets_crowned=False):
        self.before = before
        self.after = after
        self.captures = captures
        self.gets_crowned = gets_crowned

    def __repr__(self):
        return f'{self.before}-{self.after}' if not self.captures else f'{self.before}:{self.after}'

    def __add__(self, other):
        return Move(self.before, other.after, self.captures + other.captures)

    def __eq__(self, other):
        return self.before == other.before and self.after == other.after


class Position:
    def __init__(self, board, whites_str: str = WHITES_INITIAL_POSITION, blacks_str: str = BLACKS_INITIAL_POSITION):
        self.whites = {board[tile_name.strip().upper()]: Piece(board[tile_name.strip().upper()], False)
                       for tile_name in whites_str.split(',')}
        self.blacks = {board[tile_name.strip().upper()]: Piece(board[tile_name.strip().upper()], True)
                       for tile_name in blacks_str.split(',')}
        self.pieces = self.blacks | self.whites

    def __getitem__(self, tile: Tile) -> Piece:
        return self.pieces.get(tile)

    def all_pieces(self):
        return self.pieces.values()

    def move_piece(self, move):
        piece = self.pieces[move.before]
        new_tile = move.after
        old_position = piece.position
        my_dict = self.blacks if piece.black else self.whites
        opponent_dict = self.whites if piece.black else self.blacks
        del my_dict[old_position]
        del self.pieces[old_position]

        piece.position = new_tile
        if move.gets_crowned:
            piece.king = True
        my_dict[piece.position] = piece
        self.pieces[piece.position] = piece

        for position in move.captures:
            del opponent_dict[position]
            del self.pieces[position]
