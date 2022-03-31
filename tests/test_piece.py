from piece import Piece
from tile import Tile


def test_piece():
    tile = Tile.from_string('C3')
    piece = Piece(tile, False, False)
    assert (str(piece) == 'white man on C3')
    assert(piece.x == tile.x and piece.y == tile.y)