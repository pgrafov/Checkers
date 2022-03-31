from move import Move
from tile import Tile


def test_move():
    move1 = Move(Tile.from_string('C3'), Tile.from_string('E5'), captures=(Tile.from_string('D4'),))
    move2 = Move(Tile.from_string('E5'), Tile.from_string('C7'), captures=(Tile.from_string('D6'),))
    move3 = Move(Tile.from_string('C7'), Tile.from_string('A5'), captures=(Tile.from_string('B6'),))
    move4 = Move(Tile.from_string('A5'), Tile.from_string('C3'), captures=(Tile.from_string('B4'),))

    assert (move1 + move2 + move3 + move4) == Move(Tile.from_string('C3'), Tile.from_string('C3'),
                                                   captures=(Tile.from_string('D4'), Tile.from_string('D6'),
                                                             Tile.from_string('B6'), Tile.from_string('B4')))
    assert str(move1 + move2 + move3 + move4) == 'C3:C3'
    assert repr(move1 + move2 + move3 + move4) == 'Move(C3, C3, (D4, D6, B6, B4), False)'
