from tile import Tile


class Move:
    def __init__(self, before: Tile, after: Tile, captures=tuple(), gets_crowned=False):
        self.before = before
        self.after = after
        self.captures = captures
        self.gets_crowned = gets_crowned

    def __repr__(self):
        return f'{self.before}-{self.after}' if not self.captures else f'{self.before}:{self.after}'

    def __add__(self, other):
        return Move(self.before, other.after, self.captures + other.captures, other.gets_crowned)

    def __eq__(self, other):
        return self.before == other.before and self.after == other.after and \
               self.captures == other.captures and self.gets_crowned == other.gets_crowned
