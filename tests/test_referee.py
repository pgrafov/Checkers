from board import Board
from position import Position
from tile import Tile
from piece import Piece
from move import Move
from referee import gets_crowned, move_piece, Referee


def test_get_crowned():
    piece = Piece(Tile.from_string('G7'), False, False)
    tile = Tile.from_string('H8')
    assert (gets_crowned(piece, tile)) is True


def test_move_piece():
    board = Board()
    board.set_initial_position(Position(board, '18,24,27,28,K10,K15', '12,16,20,K22,K25,K29'))
    G3 = Tile.from_string('G3')
    F4 = Tile.from_string('F4')
    moves = []
    move_piece(board, Move(G3, F4), moves)
    assert (len(moves) == 1)
    assert board.current_position[G3] is None
    assert str(board.current_position[F4]) == 'white man on F4'

def test_refereree():
    board = Board()
    board.set_initial_position(Position(board, '18,24,27,28,K10,K15', '12,16,20,K22,K25,K29'))
    referee = Referee(board)
    # to be continued
