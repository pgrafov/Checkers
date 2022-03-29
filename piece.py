from tile import Tile

class Piece:
    def __init__(self, position: Tile, black: bool, king: bool = False):
        self.position = position
        self.king = king
        self.black = black

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def __repr__(self):
        return f'{"black" if self.black else "white"} {"king" if self.king else "piece"} on {self.position}'