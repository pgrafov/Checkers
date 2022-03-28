import logging
import copy
from tile import VECTORS, VECTORS_BLACK, X2, MINUS
from board import Board, Position, Move
from constants import BOARD_SIZE


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def gets_crowned(piece, tile):
    return (tile.y == 0 and not piece.black) or (tile.y == BOARD_SIZE - 1 and piece.black)

def move_piece(board: Board, move: Move, moves: list[Move]):
    LOGGER.info("Move: %s", move)
    moves.append(move)
    new_position = copy.copy(board.current_position)
    new_position.move_piece(move)
    board.positions.append(new_position)


class Referee:

    def __init__(self, board: Board):
        self.board = board

    def get_all_moves_starting_at(self, tile, piece):
        capturing_moves = self.get_all_capturing_moves_starting_at(tile, piece)
        if capturing_moves:
            return self.filter_out_capturing_moves(capturing_moves)
        return self.get_all_non_capturing_moves_starting_at(tile, piece)

    def get_all_capturing_moves_starting_at(self, tile, piece, capturing_vector=None):
        current_position = self.board.current_position
        moves = []
        if not piece.king:
            for vector in VECTORS:
                if capturing_vector is not None and vector == MINUS(capturing_vector):
                    continue
                if (tile + vector and tile + X2(vector) and
                        current_position[tile + vector] is not None and
                        current_position[tile + vector].black != piece.black and
                        current_position[tile + X2(vector)] is None):
                    move = Move(tile, tile + X2(vector), captures=(tile + vector,),
                                gets_crowned=gets_crowned(piece, tile + X2(vector)))
                    moves2 = self.get_all_capturing_moves_starting_at(tile + X2(vector), piece, vector)
                    if not moves2:
                        moves.append(move)
                    else:
                        for move2 in moves2:
                            moves.append(move + move2)
        else:
            raise NotImplementedError
        return moves

    def get_all_non_capturing_moves_starting_at(self, tile, piece):
        moves = []
        if not piece.king:
            for vector in VECTORS:
                if tile + vector:
                    if self.board.current_position[tile + vector] is None:
                        if (piece.black and vector in VECTORS_BLACK) or \
                                (not piece.black and vector not in VECTORS_BLACK):
                            moves.append(Move(tile, tile + vector, gets_crowned=gets_crowned(piece, tile + vector)))
        else:
            raise NotImplementedError
        return moves

    def get_all_possible_moves(self) -> list[Move]:
        whites = self.board.current_position.whites
        blacks = self.board.current_position.blacks
        tiles = whites if len(self.board.positions) % 2 else blacks
        capturing_moves = []
        non_capturing_moves = []
        for tile, piece in tiles.items():
            capturing_moves += self.get_all_capturing_moves_starting_at(tile, piece)
            if not capturing_moves:
                non_capturing_moves += self.get_all_non_capturing_moves_starting_at(tile, piece)
        if capturing_moves:
            return self.filter_out_capturing_moves(capturing_moves)
        return non_capturing_moves

    def get_all_pieces_that_can_move(self):
        return set([self.board.current_position[move.before] for move in self.get_all_possible_moves()])

    def filter_out_capturing_moves(self, moves):
        moves.sort(key=lambda m: len(m.captures), reverse=True)
        max_captures = moves[0].captures if moves else 0
        return [move for move in moves if move.captures == max_captures]
