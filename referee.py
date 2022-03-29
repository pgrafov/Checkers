import logging
import copy
from typing import Optional
from tile import VECTORS, VECTORS_BLACK, X2, MINUS, \
    VECTOR_TOP_LEFT, VECTOR_TOP_RIGHT, VECTOR_BOTTOM_LEFT, VECTOR_BOTTOM_RIGHT
from board import Board
from move import Move
from tile import Tile
from piece import Piece
from constants import BOARD_SIZE


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def gets_crowned(piece: Piece, tile: Tile) -> bool:
    return not piece.king and ((tile.y == 0 and not piece.black) or (tile.y == BOARD_SIZE - 1 and piece.black))


def move_piece(board: Board, move: Move, moves: list[Move]):
    LOGGER.info("Move: %s", move)
    moves.append(move)
    new_position = copy.copy(board.current_position)
    new_position.move_piece(move)
    board.positions.append(new_position)


class Referee:
    def __init__(self, board: Board):
        self.board = board

    def get_all_moves(self, tile: Tile, piece: Piece) -> list[Move]:
        capturing_moves = self.get_all_capturing_moves(tile, piece)
        if capturing_moves:
            return self.filter_out_capturing_moves(capturing_moves)
        return self.get_all_non_capturing_moves(tile, piece)

    def get_all_capturing_moves(self, tile: Tile, piece: Piece,
                                capturing_vector: Optional[tuple[int]] = None) -> list[Move]:
        if piece.king:
            return self.get_all_capturing_moves_for_king(tile, piece, capturing_vector)
        else:
            return self.get_all_capturing_moves_for_man(tile, piece, capturing_vector)

    def get_all_capturing_moves_for_man(self, tile: Tile, piece: Piece,
                                        capturing_vector: Optional[tuple[int]] = None) -> list[Move]:
        current_position = self.board.current_position
        moves = []
        for vector in VECTORS:
            if capturing_vector is not None and vector == MINUS(capturing_vector):
                continue
            if (tile + vector and tile + X2(vector) and
                    current_position[tile + vector] is not None and
                    current_position[tile + vector].black != piece.black and
                    current_position[tile + X2(vector)] is None):
                move = Move(tile, tile + X2(vector), captures=(tile + vector,),
                            gets_crowned=gets_crowned(piece, tile + X2(vector)))
                moves2 = self.get_all_capturing_moves_for_man(tile + X2(vector), piece, vector)
                if not moves2:
                    moves.append(move)
                else:
                    for move2 in moves2:
                        moves.append(move + move2)
        return moves

    def get_all_capturing_moves_for_king(self, tile: Tile, piece: Piece,
                                         capturing_vector: Optional[tuple[int]] = None) -> list[Move]:
        moves = []
        directions = {VECTOR_TOP_LEFT: list(tile.top_left()), VECTOR_TOP_RIGHT: list(tile.top_right()),
                      VECTOR_BOTTOM_RIGHT: list(tile.bottom_right()), VECTOR_BOTTOM_LEFT: list(tile.bottom_left())}
        for vector, direction in directions.items():
            if capturing_vector is not None and vector == MINUS(capturing_vector):
                continue
            for i in range(1, len(direction)):
                if (self.board.current_position[direction[i-1]] is not None
                        and self.board.current_position[direction[i-1]].black != piece.black
                        and self.board.current_position[direction[i]] is None):
                    move = Move(tile, direction[i], captures=(direction[i-1],))
                    moves2 = self.get_all_capturing_moves_for_king(direction[i], piece, vector)
                    if not moves2:
                        for j in range(i, len(direction)):
                            if self.board.current_position[direction[j]] is None:
                                moves.append(move + Move(tile, direction[j]))
                            else:
                                break
                    else:
                        for move2 in moves2:
                            moves.append(move + move2)
        return moves

    def get_all_non_capturing_moves(self, tile: Tile, piece: Piece) -> list[Move]:
        if piece.king:
            return self.get_all_non_capturing_moves_for_king(tile, piece)
        else:
            return self.get_all_non_capturing_moves_for_man(tile, piece)

    def get_all_non_capturing_moves_for_man(self, tile: Tile, piece: Piece) -> list[Move]:
        moves = []
        for vector in VECTORS:
            if tile + vector:
                if self.board.current_position[tile + vector] is None:
                    if (piece.black and vector in VECTORS_BLACK) or \
                            (not piece.black and vector not in VECTORS_BLACK):
                        moves.append(Move(tile, tile + vector, gets_crowned=gets_crowned(piece, tile + vector)))
        return moves

    def get_all_non_capturing_moves_for_king(self, tile: Tile, piece: Piece) -> list[Move]:
        moves = []
        top_left = list(tile.top_left())
        top_right = list(tile.top_right())
        bottom_right = list(tile.bottom_right())
        bottom_left = list(tile.bottom_left())
        directions = [top_left, top_right, bottom_left, bottom_right]
        for direction in directions:
            moves_direction = []
            include_direction = True
            for i, tile2 in enumerate(direction):
                if self.board.current_position[tile2] is None:
                    moves_direction.append(tile2)
                else:
                    if not(self.board.current_position[tile2].black == piece.black or
                           (self.board.current_position[tile2].black != piece.black and
                            (i == len(direction) - 1 or self.board.current_position[direction[i+1]] is not None))):
                        include_direction = False
                    break
            if include_direction:
                for tile3 in moves_direction:
                    moves.append(Move(tile, tile3))
        return moves

    def get_all_possible_moves(self) -> list[Move]:
        whites = self.board.current_position.whites
        blacks = self.board.current_position.blacks
        tiles = whites if len(self.board.positions) % 2 else blacks
        capturing_moves = []
        non_capturing_moves = []
        for tile, piece in tiles.items():
            capturing_moves += self.get_all_capturing_moves(tile, piece)
            if not capturing_moves:
                non_capturing_moves += self.get_all_non_capturing_moves(tile, piece)
        if capturing_moves:
            return self.filter_out_capturing_moves(capturing_moves)
        return non_capturing_moves

    def get_all_pieces_that_can_move(self) -> set[Piece]:
        return set([self.board.current_position[move.before] for move in self.get_all_possible_moves()])

    def filter_out_capturing_moves(self, moves: list[Move]) -> list[Move]:
        moves.sort(key=lambda m: len(m.captures), reverse=True)
        max_captures = moves[0].captures if moves else 0
        return [move for move in moves if move.captures == max_captures]

