from board import Board
from position import Position
from tile import Tile
from move import Move


def test_position():
    board = Board()
    board.set_initial_position(Position(board, '18,24,27,28', '12,16,20,K22,K25,K29'))

    G3 = Tile.from_string('G3')
    F4 = Tile.from_string('F4')
    F2 = Tile.from_string('F2')
    G5 = Tile.from_string('G5')
    G1 = Tile.from_string('G1')

    assert(str(board.current_position[G3])) == 'white man on G3'
    assert(len(board.current_position.all_pieces())) == 10
    board.current_position.move_piece(Move(G3, F4))
    assert (str(board.current_position[F4])) == 'white man on F4'
    assert (board.current_position[G3]) is None
    board.current_position.move_piece(Move(G5, G1, captures=(F4, F2), gets_crowned=True))
    assert (str(board.current_position[G1])) == 'black king on G1'
    assert (board.current_position[G5]) is None
    assert (board.current_position[F4]) is None
    assert (board.current_position[F2]) is None
