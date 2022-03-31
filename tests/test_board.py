from board import Board
from position import Position


def test_board():
    board = Board()
    tile_00 = board.get(0, 0)
    tile_a1 = board['A1']
    tile_12 = board.get(1, 2)
    tile_b3 = board['B3']
    assert (tile_b3 == tile_12)
    assert (tile_a1 == tile_00)
    position = Position(board)
    board.set_initial_position(position)
    assert board.current_position == position