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


def test_referee():
    board = Board()
    board.set_initial_position(Position(board, 'D4,F2,G3,H2,KD6,KE5', 'G5,H4,H6,F8,KA1,KB2,KC3'))
    referee = Referee(board)
    A1 = Tile.from_string('A1')
    B2 = Tile.from_string('B2')
    B8 = Tile.from_string('B8')
    C3 = Tile.from_string('C3')
    C7 = Tile.from_string('C7')
    D4 = Tile.from_string('D4')
    D6 = Tile.from_string('D6')
    E5 = Tile.from_string('E5')
    F2 = Tile.from_string('F2')
    F6 = Tile.from_string('F6')
    G1 = Tile.from_string('G1')
    G3 = Tile.from_string('G3')
    G5 = Tile.from_string('G5')
    G7 = Tile.from_string('G7')
    H8 = Tile.from_string('H8')
    moves = []
    assert ', '.join(str(m) for m in referee.get_all_moves(D6, board.current_position[D6])) == \
           'D6-C7, D6-B8, D6-E7, D6-C5, D6-B4, D6-A3'
    assert ', '.join(str(m) for m in referee.get_all_moves(E5, board.current_position[E5])) == \
           'E5-F6, E5-G7, E5-H8, E5-F4'
    assert ', '.join(str(m) for m in referee.get_all_moves(F2, board.current_position[F2])) == 'F2-E3'
    assert referee.get_all_pieces_that_can_move() == {board.current_position[i] for i in [D4, D6, E5, F2, G3]}
    move_piece(board, Move(E5, F6), moves)
    assert ', '.join(str(m) for m in referee.get_all_non_capturing_moves(C3, board.current_position[C3])) == \
           'C3-B4, C3-A5, C3-D2, C3-E1'
    moves = referee.get_all_capturing_moves(C3, board.current_position[C3])
    assert Move(C3, C7, (D4, D6)) in moves
    assert Move(C3, B8, (D4, D6)) in moves
    assert Move(C3, G7, (D4, F6)) in moves
    assert Move(C3, H8, (D4, F6)) in moves
    moves2 = referee.get_all_moves(C3, board.current_position[C3])
    assert (moves2 == moves)
    assert (referee.get_all_moves(A1, board.current_position[A1]) == [])
    assert (referee.get_all_moves(A1, board.current_position[B2]) == [])
    moves = referee.get_all_moves(G5, board.current_position[G5])
    assert (len(moves) == 1)
    assert moves[0] == Move(G5, G1, (F6, D6, D4, F2), True)

    board.set_initial_position(Position(board, 'KG7', 'KA1,KB2,KD4'))
    moves = referee.get_all_moves(G7, board.current_position[G7])
    assert (len(moves) == 1)
    assert moves[0] == Move(G7, C3, (D4, ))
    moves2 = referee.get_all_possible_moves()
    assert (moves2 == moves)
    assert referee.get_all_pieces_that_can_move() == {board.current_position[G7]}

    board.set_initial_position(Position(board, 'KA1,F2,KG1', 'KD4'))
    assert referee.get_all_pieces_that_can_move() == {board.current_position[A1]}