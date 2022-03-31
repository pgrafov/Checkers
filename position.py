from typing import Optional

from notation import parse_pieces, parse_position
from tile import Tile
from piece import Piece
from constants import WHITES_INITIAL_POSITION, BLACKS_INITIAL_POSITION

WHITES_TURN = 'W'
BLACKS_TURN = 'B'


class Position:
    def __init__(self, board, whites_str: str = WHITES_INITIAL_POSITION, blacks_str: str = BLACKS_INITIAL_POSITION,
                 notation: Optional[str] = None, turn: str = WHITES_TURN):
        if notation:
            whites_str, blacks_str, turn = parse_position(notation)
        self.whites = parse_pieces(whites_str, board, False)
        self.blacks = parse_pieces(blacks_str, board, True)
        self.turn = turn
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

        self.turn = WHITES_TURN if self.turn == BLACKS_TURN else BLACKS_TURN