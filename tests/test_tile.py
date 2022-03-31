from tile import Tile


def test_tile():
    tile = Tile.from_string('A1')
    assert (tile.number == '29')
    tile = Tile.from_string('G1')
    assert (tile.number == '32')