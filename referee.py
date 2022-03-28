import logging
import copy
from typing import Optional
from board import Board, Position, Move, Piece, Tile


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def move_piece(board: Board, move: Move, moves: list[Move]):
    LOGGER.info("Move: %s", move)
    moves.append(move)
    new_position = copy.copy(board.current_position)
    new_position.move_piece(move)
    board.positions.append(new_position)


class Referee:

    def __init__(self, board: Board):
        self.board = board

    def make_capturing_move(self, start_tile: Tile, next_tile: Tile ) -> Optional[Move]:
        vector = (next_tile.x - start_tile.x, next_tile.y - start_tile.y)
        if Tile.is_valid(next_tile.x + vector[0], next_tile.y + vector[1]) and \
                self.board.current_position[Tile(next_tile.x + vector[0], next_tile.y + vector[1])] is None:
            return Move(start_tile, Tile(next_tile.x + vector[0], next_tile.y + vector[1]), captures=(next_tile,))
        return None

    def get_move(self, start_tile, next_tile):
        if self.board.current_position[next_tile]:
            if self.board.current_position[next_tile].black == self.board.current_position[start_tile].black:
                return None
            else:
                return self.make_capturing_move(start_tile, next_tile)

        return Move(start_tile, next_tile)

    def get_all_pieces_that_can_move(self):
        return set([self.board.current_position[move.before] for move in self.get_all_possible_moves()])

    def get_all_possible_moves(self) -> list[Move]:
        whites = self.board.current_position.whites
        blacks = self.board.current_position.blacks
        tiles = whites if len(self.board.positions) % 2 else blacks
        moves = []
        for tile, piece in tiles.items():
            if piece.king:
                neighbours = [tile.top_left(), tile.top_right(), tile.bottom_left(), tile.bottom_right()]
            elif not piece.black:
                neighbours = [tile.top_left(), tile.top_right()]
            else:
                neighbours = [tile.bottom_left(), tile.bottom_right()]
            neighbours = [neighbour for neighbour in neighbours if not neighbour is None]
            for neighbour in neighbours:
                move = self.get_move(tile, neighbour)
                if move:
                    moves.append(move)
        moves.sort(key=lambda m: len(m.captures), reverse=True)
        max_captures = moves[0].captures if moves else 0
        return [move for move in moves if move.captures == max_captures]


if __name__ == "__main__":
    board = Board()
    moves = []
    position = Position(board)
    board.set_initial_position(position)
    ref = Referee(board)
    for move in ref.get_all_possible_moves():
        print (move)
    move_piece(board, board.current_position[move.before], move.after, moves)
    print ('============================')
    for move in ref.get_all_possible_moves():
        print (move)